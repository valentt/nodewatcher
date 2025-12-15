from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from leaflet import admin as leaflet_admin

from nodewatcher.core import models as core_models

from . import models


class SSIDInline(admin.TabularInline):
    """
    Inline admin for SSIDs within a Project.
    """
    model = models.SSID
    extra = 1
    fields = ('essid', 'bssid', 'purpose', 'default')


class SSIDAdmin(admin.ModelAdmin):
    """
    Standalone SSID admin for managing network identities.
    """
    list_display = ('essid', 'bssid', 'project', 'purpose', 'default')
    list_filter = ('project', 'purpose', 'default')
    search_fields = ('essid', 'bssid', 'project__name')
    list_editable = ('default',)


class ProjectAdmin(leaflet_admin.LeafletGeoAdmin):
    """
    Enhanced admin for managing network projects.
    """
    list_display = ('name', 'description_short', 'node_count', 'ip_pools_display', 'is_default')
    list_filter = ('is_default',)
    search_fields = ('name', 'description')
    list_editable = ('is_default',)
    inlines = [SSIDInline]
    filter_horizontal = ('ip_pools',)

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'is_default'),
            'description': _('Basic project information. Only one project can be set as default.')
        }),
        (_('Location'), {
            'fields': ('location',),
            'description': _('Geographic center point of the network. Used for map display.'),
            'classes': ('collapse',),
        }),
        (_('IP Address Allocation'), {
            'fields': ('ip_pools', 'default_ip_pool'),
            'description': _('IP pools available for this project. The default pool will be used for automatic allocation.')
        }),
    )

    def get_queryset(self, request):
        """Annotate queryset with node counts for efficiency."""
        qs = super(ProjectAdmin, self).get_queryset(request)
        # We'll count nodes in a separate method since it uses registry
        return qs

    def description_short(self, obj):
        """Display truncated description."""
        if obj.description:
            return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
        return '-'
    description_short.short_description = _('Description')

    def node_count(self, obj):
        """Count nodes in this project."""
        count = core_models.Node.objects.regpoint('config').registry_filter(
            core_project__project=obj
        ).count()
        if count > 0:
            return format_html(
                '<a href="../../../core/node/?config__core_project__project__id__exact={}">{} nodes</a>',
                obj.pk, count
            )
        return '0 nodes'
    node_count.short_description = _('Nodes')

    def ip_pools_display(self, obj):
        """Display IP pools as badges."""
        pools = obj.ip_pools.all()
        if not pools:
            return '-'
        return format_html(
            ' '.join([
                '<span style="background:#6366f1;color:white;padding:2px 8px;border-radius:4px;margin-right:4px;font-size:11px;">{}</span>'.format(
                    pool.description or str(pool)
                ) for pool in pools[:3]
            ]) + (' +{} more'.format(pools.count() - 3) if pools.count() > 3 else '')
        )
    ip_pools_display.short_description = _('IP Pools')

    def get_nodes_entry(self, project, node):
        return {
            'node': node,
        }

    def get_nodes(self, object_id):
        project = models.Project.objects.get(pk=object_id)
        return (self.get_nodes_entry(project, node) for node in core_models.Node.objects.regpoint('config').registry_filter(core_project__project=project))

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['nodes'] = self.get_nodes(object_id)
        return super(ProjectAdmin, self).change_view(request, object_id, form_url, extra_context)


admin.site.register(models.SSID, SSIDAdmin)
admin.site.register(models.Project, ProjectAdmin)
