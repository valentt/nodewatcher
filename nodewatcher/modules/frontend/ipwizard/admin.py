from django.contrib import admin
from . import models


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'flag_emoji', 'ip_prefix', 'postal_digits']
    search_fields = ['code', 'name']
    ordering = ['name']


@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'postal_prefix', 'main_city', 'population', 'ip_range']
    list_filter = ['country']
    search_fields = ['name', 'main_city', 'postal_prefix']
    ordering = ['country', 'postal_prefix']


@admin.register(models.ProjectPoolSettings)
class ProjectPoolSettingsAdmin(admin.ModelAdmin):
    list_display = ['project', 'pool', 'region', 'default_prefix', 'self_service_max_prefix', 'created_at']
    list_filter = ['project', 'region__country']
    search_fields = ['project__name', 'name', 'pool__network']
    readonly_fields = ['created_at', 'created_by']
    ordering = ['project__name', 'pool__network']

    fieldsets = (
        ('Pool Assignment', {
            'fields': ('project', 'pool', 'region', 'name')
        }),
        ('Allocation Settings', {
            'fields': ('default_prefix', 'self_service_max_prefix')
        }),
        ('Metadata', {
            'fields': ('created_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )


@admin.register(models.UserAllocationRequest)
class UserAllocationRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'pool_settings', 'requested_prefix', 'status', 'created_at']
    list_filter = ['status', 'pool_settings__project']
    search_fields = ['user__username', 'reason']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    fieldsets = (
        ('Request', {
            'fields': ('user', 'pool_settings', 'requested_prefix', 'reason')
        }),
        ('Approval', {
            'fields': ('status', 'allocated_pool', 'approved_by', 'sheriff_comment', 'approved_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
