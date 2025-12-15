# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db import transaction

try:
    import ipaddress
except ImportError:
    # Python 2 backport
    import ipaddr as ipaddress

from nodewatcher.core.allocation.ip import models as ip_models
from nodewatcher.modules.administration.projects import models as project_models

from . import models


class WizardView(LoginRequiredMixin, TemplateView):
    """Main wizard view for assigning IP pools to projects."""
    template_name = 'ipwizard/wizard.html'

    def get_context_data(self, **kwargs):
        context = super(WizardView, self).get_context_data(**kwargs)
        context['countries'] = models.Country.objects.prefetch_related('regions').all()
        context['projects'] = project_models.Project.objects.all()

        # Existing pool assignments
        context['existing_pools'] = models.ProjectPoolSettings.objects.select_related(
            'project', 'pool', 'region'
        ).all()

        return context


class ProjectsAPIView(LoginRequiredMixin, View):
    """API endpoint for projects."""

    def get(self, request):
        projects = project_models.Project.objects.all()
        data = [{
            'id': p.id,
            'name': p.name,
            'description': p.description or '',
            'is_default': p.is_default,
            'pools_count': p.pool_settings.count(),
        } for p in projects]
        return JsonResponse({'projects': data})


class CountriesAPIView(LoginRequiredMixin, View):
    """API endpoint for countries."""

    def get(self, request):
        countries = models.Country.objects.all()
        data = [{
            'id': c.id,
            'code': c.code,
            'name': c.name,
            'flag': c.flag_emoji,
            'regions_count': c.regions.count(),
            'ip_prefix': c.ip_prefix,
        } for c in countries]
        return JsonResponse({'countries': data})


class RegionsAPIView(LoginRequiredMixin, View):
    """API endpoint for regions by country."""

    def get(self, request, country_id):
        regions = models.Region.objects.filter(country_id=country_id).order_by('-population')
        data = [{
            'id': r.id,
            'name': r.name,
            'postal_prefix': r.postal_prefix,
            'main_city': r.main_city,
            'main_postal_code': r.main_postal_code,
            'population': r.population,
            'ip_range': r.ip_range,
            'ip_network': r.ip_network,
            'ip_second_octet': r.ip_second_octet,
            'is_assigned': models.ProjectPoolSettings.objects.filter(region=r).exists(),
        } for r in regions]
        return JsonResponse({'regions': data})


class ValidatePoolView(LoginRequiredMixin, View):
    """Validate a pool configuration before assignment."""

    def get(self, request):
        network = request.GET.get('network', '')
        prefix = request.GET.get('prefix', '16')

        errors = []
        warnings = []

        try:
            # Parse the network
            if '/' in network:
                subnet = ipaddress.ip_network(str(network), strict=False)
            else:
                subnet = ipaddress.ip_network(str("{}/{}".format(network, prefix)), strict=False)

            # Validate it's in 10.0.0.0/8
            mesh_network = ipaddress.ip_network(u'10.0.0.0/8')
            if not subnet.subnet_of(mesh_network):
                errors.append("Pool must be within 10.0.0.0/8")

            # Check prefix range for top-level pools
            if subnet.prefixlen > 24:
                errors.append("Top-level pools must be /24 or larger")
            if subnet.prefixlen < 8:
                errors.append("Pool cannot be larger than /8")

            # Check if pool already exists
            existing = ip_models.IpPool.objects.filter(
                network=str(subnet.network_address),
                prefix_length=subnet.prefixlen,
                parent=None
            ).first()

            if existing:
                warnings.append("Pool already exists: {}".format(existing))

            if not errors:
                total_ips = subnet.num_addresses
                return JsonResponse({
                    'valid': True,
                    'network': str(subnet.network_address),
                    'prefix': subnet.prefixlen,
                    'broadcast': str(subnet.broadcast_address),
                    'total_ips': total_ips,
                    'existing_pool_id': existing.id if existing else None,
                    'warnings': warnings,
                })

        except ValueError as e:
            errors.append("Invalid format: {}".format(str(e)))

        return JsonResponse({
            'valid': False,
            'errors': errors,
            'warnings': warnings,
        })


class AssignPoolView(LoginRequiredMixin, View):
    """Assign an IP pool to a project."""

    def post(self, request):
        try:
            data = json.loads(request.body)
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        project_id = data.get('project_id')
        mode = data.get('mode', 'simple')

        # Pool configuration
        network = data.get('network')
        prefix = int(data.get('prefix', 16))
        region_id = data.get('region_id')
        pool_name = data.get('name', '')

        # Allocation settings
        default_prefix = int(data.get('default_prefix', 28))
        self_service_max_prefix = int(data.get('self_service_max_prefix', 26))

        # Validate project
        try:
            project = project_models.Project.objects.get(id=project_id)
        except project_models.Project.DoesNotExist:
            return JsonResponse({'error': 'Project not found'}, status=404)

        # Validate network
        try:
            if '/' in network:
                subnet = ipaddress.ip_network(str(network), strict=False)
                network = str(subnet.network_address)
                prefix = subnet.prefixlen
            else:
                subnet = ipaddress.ip_network(str("{}/{}".format(network, prefix)), strict=False)
        except ValueError as e:
            return JsonResponse({'error': 'Invalid network: {}'.format(str(e))}, status=400)

        # Get region if specified
        region = None
        if region_id:
            try:
                region = models.Region.objects.get(id=region_id)
            except models.Region.DoesNotExist:
                pass

        # Create description
        if pool_name:
            description = pool_name
        elif region:
            description = "{} Region Pool".format(region.main_city)
        else:
            description = "Pool {}/{}".format(network, prefix)

        with transaction.atomic():
            # Find or create the IpPool
            pool, created = ip_models.IpPool.objects.get_or_create(
                network=network,
                prefix_length=prefix,
                parent=None,
                defaults={
                    'family': 'ipv4',
                    'description': description,
                    'prefix_length_default': default_prefix,
                    'prefix_length_minimum': 24,
                    'prefix_length_maximum': 30,
                }
            )

            # Check if already assigned to this project
            existing_settings = models.ProjectPoolSettings.objects.filter(
                project=project,
                pool=pool
            ).first()

            if existing_settings:
                return JsonResponse({
                    'error': 'Pool already assigned to this project',
                    'existing_id': existing_settings.id,
                }, status=400)

            # Create ProjectPoolSettings
            pool_settings = models.ProjectPoolSettings.objects.create(
                project=project,
                pool=pool,
                region=region,
                name=pool_name,
                default_prefix=default_prefix,
                self_service_max_prefix=self_service_max_prefix,
                created_by=request.user,
            )

            # Also add to project's ip_pools if not already there
            if pool not in project.ip_pools.all():
                project.ip_pools.add(pool)

            return JsonResponse({
                'success': True,
                'pool_settings_id': pool_settings.id,
                'pool_id': pool.id,
                'created_new_pool': created,
                'message': 'Pool {}/{} assigned to {}'.format(network, prefix, project.name),
                'summary': {
                    'project': project.name,
                    'network': "{}/{}".format(network, prefix),
                    'total_ips': subnet.num_addresses,
                    'default_prefix': default_prefix,
                    'self_service_max_prefix': self_service_max_prefix,
                    'region': region.name if region else None,
                }
            })


class ProjectPoolsView(LoginRequiredMixin, View):
    """Get pools assigned to a project."""

    def get(self, request, project_id):
        try:
            project = project_models.Project.objects.get(id=project_id)
        except project_models.Project.DoesNotExist:
            return JsonResponse({'error': 'Project not found'}, status=404)

        pool_settings = models.ProjectPoolSettings.objects.filter(
            project=project
        ).select_related('pool', 'region')

        data = [{
            'id': ps.id,
            'pool_id': ps.pool.id,
            'network': ps.pool.network,
            'prefix': ps.pool.prefix_length,
            'name': ps.display_name,
            'region': ps.region.name if ps.region else None,
            'default_prefix': ps.default_prefix,
            'self_service_max_prefix': ps.self_service_max_prefix,
            'created_at': ps.created_at.isoformat(),
        } for ps in pool_settings]

        return JsonResponse({'pools': data})


class RemovePoolView(LoginRequiredMixin, View):
    """Remove a pool assignment from a project."""

    def post(self, request, pool_settings_id):
        try:
            pool_settings = models.ProjectPoolSettings.objects.get(id=pool_settings_id)
        except models.ProjectPoolSettings.DoesNotExist:
            return JsonResponse({'error': 'Pool settings not found'}, status=404)

        project_name = pool_settings.project.name
        pool_str = str(pool_settings.pool)

        # Remove the settings (pool itself is kept)
        pool_settings.delete()

        return JsonResponse({
            'success': True,
            'message': 'Pool {} removed from {}'.format(pool_str, project_name),
        })


class PoolListView(LoginRequiredMixin, TemplateView):
    """View all pool assignments."""
    template_name = 'ipwizard/pool_list.html'

    def get_context_data(self, **kwargs):
        context = super(PoolListView, self).get_context_data(**kwargs)
        context['pool_settings'] = models.ProjectPoolSettings.objects.select_related(
            'project', 'pool', 'region', 'created_by'
        ).order_by('project__name', 'pool__network')
        return context
