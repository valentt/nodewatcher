from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from guardian import admin as guardian_admin

from . import models


class NodeAdmin(guardian_admin.GuardedModelAdmin):
    """
    Enhanced Node admin with better display and filtering.
    """
    list_display = ('uuid_short', 'name_display', 'project_display', 'status_display', 'created', 'last_modified')
    list_filter = ('created',)
    search_fields = ('uuid',)
    readonly_fields = ('uuid',)
    date_hierarchy = 'created'

    fieldsets = (
        (None, {
            'fields': ('uuid',),
            'description': _('Node identifier. Use the node editor for configuration.')
        }),
    )

    def uuid_short(self, obj):
        """Display shortened UUID."""
        return str(obj.uuid)[:8] + '...'
    uuid_short.short_description = _('Node ID')

    def name_display(self, obj):
        """Try to get node name from registry."""
        try:
            config = obj.config.core.general()
            if config and config.name:
                return config.name
        except:
            pass
        return format_html('<span style="color:#64748b;font-style:italic;">unnamed</span>')
    name_display.short_description = _('Name')

    def project_display(self, obj):
        """Try to get project from registry."""
        try:
            config = obj.config.core.project()
            if config and config.project:
                return format_html(
                    '<a href="../administration/projects/project/{}/change/">{}</a>',
                    config.project.pk, config.project.name
                )
        except:
            pass
        return '-'
    project_display.short_description = _('Project')

    def status_display(self, obj):
        """Try to get node status."""
        try:
            # Try to get monitoring status
            monitor = obj.monitoring.core.general()
            if monitor:
                if hasattr(monitor, 'last_seen') and monitor.last_seen:
                    from django.utils import timezone
                    import datetime
                    age = timezone.now() - monitor.last_seen
                    if age < datetime.timedelta(minutes=10):
                        return format_html(
                            '<span style="background:#10b981;color:white;padding:2px 8px;border-radius:4px;font-size:11px;">Online</span>'
                        )
                    elif age < datetime.timedelta(hours=1):
                        return format_html(
                            '<span style="background:#f59e0b;color:white;padding:2px 8px;border-radius:4px;font-size:11px;">Warning</span>'
                        )
                    else:
                        return format_html(
                            '<span style="background:#ef4444;color:white;padding:2px 8px;border-radius:4px;font-size:11px;">Offline</span>'
                        )
        except:
            pass
        return format_html(
            '<span style="background:#64748b;color:white;padding:2px 8px;border-radius:4px;font-size:11px;">Unknown</span>'
        )
    status_display.short_description = _('Status')

    def last_modified(self, obj):
        """Show last modification time if available."""
        try:
            monitor = obj.monitoring.core.general()
            if monitor and hasattr(monitor, 'last_seen'):
                return monitor.last_seen
        except:
            pass
        return '-'
    last_modified.short_description = _('Last Seen')


admin.site.register(models.Node, NodeAdmin)
