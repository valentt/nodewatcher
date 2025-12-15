from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from guardian import admin as guardian_admin

from . import models


class IpPoolAdmin(guardian_admin.GuardedModelAdmin):
    """
    Enhanced IP Pool admin with better display and management.
    """
    list_display = ('description', 'network_display', 'family_display', 'status_badge', 'prefix_config', 'projects_display')
    list_filter = ('family', 'status')
    search_fields = ('description', 'network')
    ordering = ('description',)
    readonly_fields = ('status', 'ip_subnet', 'held_from')

    fieldsets = (
        (None, {
            'fields': ('description', 'family', 'network', 'prefix_length'),
            'description': _('Basic pool configuration. Network and prefix define the available address space.')
        }),
        (_('Allocation Settings'), {
            'fields': ('prefix_length_default', 'prefix_length_minimum', 'prefix_length_maximum'),
            'description': _('Configure how subnets are allocated from this pool.')
        }),
        (_('Status'), {
            'fields': ('status', 'ip_subnet', 'held_from'),
            'classes': ('collapse',),
            'description': _('Read-only status information.')
        }),
    )

    def get_queryset(self, request):
        qs = super(IpPoolAdmin, self).get_queryset(request)
        # Hide non-top-level pools.
        qs = qs.filter(parent=None)
        return qs.prefetch_related('projects')

    def network_display(self, obj):
        """Display network in CIDR notation."""
        return format_html(
            '<code style="background:#1e293b;color:#e2e8f0;padding:2px 8px;border-radius:4px;">{}/{}</code>',
            obj.network, obj.prefix_length
        )
    network_display.short_description = _('Network')
    network_display.admin_order_field = 'network'

    def family_display(self, obj):
        """Display IP family as badge."""
        colors = {'ipv4': '#10b981', 'ipv6': '#6366f1'}
        family_str = obj.family_as_string()
        color = colors.get(obj.family, '#64748b')
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:4px;font-size:11px;text-transform:uppercase;">{}</span>',
            color, family_str
        )
    family_display.short_description = _('Family')
    family_display.admin_order_field = 'family'

    def status_badge(self, obj):
        """Display status as colored badge."""
        status_colors = {
            models.IpPoolStatus.Free: ('#10b981', 'Free'),
            models.IpPoolStatus.Full: ('#ef4444', 'Full'),
            models.IpPoolStatus.Partial: ('#f59e0b', 'Partial'),
            models.IpPoolStatus.HeldDown: ('#64748b', 'Held'),
        }
        color, label = status_colors.get(obj.status, ('#64748b', 'Unknown'))
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:4px;font-size:11px;">{}</span>',
            color, label
        )
    status_badge.short_description = _('Status')
    status_badge.admin_order_field = 'status'

    def prefix_config(self, obj):
        """Display prefix length configuration."""
        if obj.prefix_length_minimum and obj.prefix_length_maximum:
            return '/{} - /{} (default: /{})'.format(
                obj.prefix_length_minimum,
                obj.prefix_length_maximum,
                obj.prefix_length_default or '-'
            )
        return '-'
    prefix_config.short_description = _('Prefix Config')

    def projects_display(self, obj):
        """Display associated projects."""
        projects = obj.projects.all()
        if not projects:
            return '-'
        return ', '.join([p.name for p in projects[:3]]) + (' +{} more'.format(projects.count() - 3) if projects.count() > 3 else '')
    projects_display.short_description = _('Projects')


admin.site.register(models.IpPool, IpPoolAdmin)
