from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from . import models


class BuildChannelAdmin(admin.ModelAdmin):
    """
    Admin for firmware build channels.
    """
    list_display = ('name', 'description_short', 'builders_count', 'created', 'last_modified', 'default')
    list_filter = ('default',)
    search_fields = ('name', 'description')
    filter_horizontal = ('builders',)
    readonly_fields = ('uuid', 'created', 'last_modified')

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'default'),
        }),
        (_('Builders'), {
            'fields': ('builders',),
            'description': _('Select which builders can build firmware for this channel.')
        }),
        (_('Metadata'), {
            'fields': ('uuid', 'created', 'last_modified'),
            'classes': ('collapse',),
        }),
    )

    def description_short(self, obj):
        if obj.description:
            return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
        return '-'
    description_short.short_description = _('Description')

    def builders_count(self, obj):
        count = obj.builders.count()
        return '{} builder{}'.format(count, 's' if count != 1 else '')
    builders_count.short_description = _('Builders')


class BuilderAdmin(admin.ModelAdmin):
    """
    Admin for firmware builder hosts.
    """
    list_display = ('host', 'platform', 'architecture', 'version', 'channels_display')
    list_filter = ('platform', 'architecture', 'version')
    search_fields = ('host', 'platform', 'architecture')
    readonly_fields = ('uuid', 'platform', 'architecture', 'version', 'metadata')

    fieldsets = (
        (None, {
            'fields': ('host', 'private_key'),
            'description': _('SSH connection details for the builder.')
        }),
        (_('Builder Info'), {
            'fields': ('platform', 'architecture', 'version'),
            'description': _('Automatically detected from builder metadata.'),
            'classes': ('collapse',),
        }),
        (_('Metadata'), {
            'fields': ('uuid', 'metadata'),
            'classes': ('collapse',),
        }),
    )

    def channels_display(self, obj):
        channels = obj.channels.all()
        if not channels:
            return '-'
        return ', '.join([c.name for c in channels])
    channels_display.short_description = _('Channels')


class BuildVersionAdmin(admin.ModelAdmin):
    """
    Admin for build versions (read-only).
    """
    list_display = ('name', 'created', 'builders_count')
    search_fields = ('name',)
    readonly_fields = ('uuid', 'name', 'created')

    def builders_count(self, obj):
        return obj.builders.count()
    builders_count.short_description = _('Builders')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class BuildResultFileInline(admin.TabularInline):
    """
    Inline for build result files.
    """
    model = models.BuildResultFile
    extra = 0
    readonly_fields = ('uuid', 'file', 'checksum_md5', 'checksum_sha256', 'hidden')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


class BuildResultAdmin(admin.ModelAdmin):
    """
    Admin for viewing firmware build results (read-only).
    """
    list_display = ('uuid_short', 'node_display', 'user', 'status_badge', 'build_channel', 'builder', 'created', 'last_modified')
    list_filter = ('status', 'build_channel', 'builder', 'created')
    search_fields = ('uuid', 'user__username', 'node__pk')
    readonly_fields = ('uuid', 'user', 'node', 'config', 'build_channel', 'builder', 'build_log', 'created', 'last_modified', 'status')
    date_hierarchy = 'created'
    inlines = [BuildResultFileInline]

    fieldsets = (
        (None, {
            'fields': ('uuid', 'status', 'user', 'node'),
        }),
        (_('Build Configuration'), {
            'fields': ('build_channel', 'builder'),
        }),
        (_('Build Output'), {
            'fields': ('build_log',),
            'classes': ('collapse',),
        }),
        (_('Configuration'), {
            'fields': ('config',),
            'classes': ('collapse',),
        }),
        (_('Timestamps'), {
            'fields': ('created', 'last_modified'),
            'classes': ('collapse',),
        }),
    )

    def uuid_short(self, obj):
        return str(obj.uuid)[:8] + '...'
    uuid_short.short_description = _('Build ID')

    def node_display(self, obj):
        return format_html('<a href="../../../core/node/{}/change/">{}</a>', obj.node_id, str(obj.node_id)[:8] + '...')
    node_display.short_description = _('Node')

    def status_badge(self, obj):
        """Display status as colored badge."""
        status_colors = {
            models.BuildResult.PENDING: ('#64748b', 'Pending'),
            models.BuildResult.BUILDING: ('#6366f1', 'Building'),
            models.BuildResult.FAILED: ('#ef4444', 'Failed'),
            models.BuildResult.OK: ('#10b981', 'OK'),
        }
        color, label = status_colors.get(obj.status, ('#64748b', 'Unknown'))
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:4px;font-size:11px;">{}</span>',
            color, label
        )
    status_badge.short_description = _('Status')
    status_badge.admin_order_field = 'status'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        # Allow superusers to delete failed builds
        return request.user.is_superuser


class BuildResultFileAdmin(admin.ModelAdmin):
    """
    Admin for build result files (read-only).
    """
    list_display = ('filename', 'result_link', 'hidden', 'checksum_md5_short')
    list_filter = ('hidden',)
    search_fields = ('file', 'result__uuid')
    readonly_fields = ('uuid', 'result', 'file', 'hidden', 'checksum_md5', 'checksum_sha256')

    def filename(self, obj):
        if obj.file:
            return obj.file.name.split('/')[-1]
        return '-'
    filename.short_description = _('Filename')

    def result_link(self, obj):
        return format_html('<a href="../buildresult/{}/change/">{}</a>', obj.result_id, str(obj.result_id)[:8] + '...')
    result_link.short_description = _('Build Result')

    def checksum_md5_short(self, obj):
        return obj.checksum_md5[:16] + '...' if obj.checksum_md5 else '-'
    checksum_md5_short.short_description = _('MD5')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(models.BuildChannel, BuildChannelAdmin)
admin.site.register(models.Builder, BuilderAdmin)
admin.site.register(models.BuildVersion, BuildVersionAdmin)
admin.site.register(models.BuildResult, BuildResultAdmin)
admin.site.register(models.BuildResultFile, BuildResultFileAdmin)
