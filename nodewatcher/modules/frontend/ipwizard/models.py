# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from nodewatcher.core.allocation.ip import models as ip_models


@python_2_unicode_compatible
class Country(models.Model):
    """
    Country definition for IP allocation.
    """
    code = models.CharField(max_length=2, unique=True, help_text=_("ISO 3166-1 alpha-2 code"))
    name = models.CharField(max_length=100)
    flag_emoji = models.CharField(max_length=4, blank=True)
    ip_prefix = models.IntegerField(
        default=0,
        help_text=_("Added to region's first 2 postal digits to get second octet. E.g., 0 for HR, 100 for SI")
    )
    postal_digits = models.IntegerField(
        default=5,
        help_text=_("Number of digits in postal code (5 for HR, 4 for SI)")
    )

    class Meta:
        app_label = 'ipwizard'
        verbose_name_plural = 'Countries'
        ordering = ['name']

    def __str__(self):
        if self.flag_emoji:
            return "{} {}".format(self.flag_emoji, self.name)
        return self.name


@python_2_unicode_compatible
class Region(models.Model):
    """
    Region (county/province) for IP allocation.
    Maps postal code prefix to IP subnet.
    """
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='regions')
    name = models.CharField(max_length=100)
    postal_prefix = models.CharField(max_length=2, help_text=_("First 2 digits of postal code"))
    main_city = models.CharField(max_length=100)
    main_postal_code = models.CharField(max_length=10)
    population = models.IntegerField(default=0)

    class Meta:
        app_label = 'ipwizard'
        unique_together = ['country', 'postal_prefix']
        ordering = ['country', 'postal_prefix']

    def __str__(self):
        return "{} ({})".format(self.name, self.main_city)

    @property
    def ip_second_octet(self):
        """Calculate second octet of IP based on postal prefix and country offset."""
        return self.country.ip_prefix + int(self.postal_prefix)

    @property
    def ip_range(self):
        """Return the IP range for this region."""
        return "10.{}.0.0/16".format(self.ip_second_octet)

    @property
    def ip_network(self):
        """Return network address."""
        return "10.{}.0.0".format(self.ip_second_octet)

    @property
    def ip_gateway(self):
        """Return default gateway."""
        return "10.{}.0.1".format(self.ip_second_octet)


@python_2_unicode_compatible
class ProjectPoolSettings(models.Model):
    """
    Links an IP pool to a project with allocation settings.
    This is the through model for project-pool relationship with extra fields.
    """
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='pool_settings'
    )
    pool = models.ForeignKey(
        ip_models.IpPool,
        on_delete=models.CASCADE,
        related_name='project_settings'
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_("Region this pool was created from (if using simple mode)")
    )

    # Allocation settings for this project
    default_prefix = models.IntegerField(
        default=28,
        help_text=_("Default prefix length for user allocations (e.g., 28 = /28 = 14 clients)")
    )
    self_service_max_prefix = models.IntegerField(
        default=26,
        help_text=_("Largest allocation without sheriff approval (e.g., 26 = /26 = 62 clients)")
    )

    # Pool metadata
    name = models.CharField(max_length=100, blank=True, help_text=_("Custom name for this pool"))
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_pool_settings'
    )

    class Meta:
        app_label = 'ipwizard'
        unique_together = ['project', 'pool']
        verbose_name = 'Project Pool Settings'
        verbose_name_plural = 'Project Pool Settings'

    def __str__(self):
        return "{} - {}".format(self.project.name, self.pool)

    @property
    def pool_network(self):
        return self.pool.network

    @property
    def pool_prefix(self):
        return self.pool.prefix_length

    @property
    def display_name(self):
        if self.name:
            return self.name
        if self.region:
            return "{} Pool".format(self.region.main_city)
        return str(self.pool)

    def get_max_clients_for_prefix(self, prefix):
        """Calculate max clients for a given prefix."""
        return 2 ** (32 - prefix) - 2  # minus network and broadcast

    @property
    def default_clients(self):
        return self.get_max_clients_for_prefix(self.default_prefix)

    @property
    def self_service_max_clients(self):
        return self.get_max_clients_for_prefix(self.self_service_max_prefix)


@python_2_unicode_compatible
class UserAllocationRequest(models.Model):
    """
    Request from a user for IP allocation within a project pool.
    Requires sheriff approval if larger than self_service_max_prefix.
    """
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'

    STATUS_CHOICES = [
        (STATUS_PENDING, _('Pending')),
        (STATUS_APPROVED, _('Approved')),
        (STATUS_REJECTED, _('Rejected')),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ip_allocation_requests'
    )
    pool_settings = models.ForeignKey(
        ProjectPoolSettings,
        on_delete=models.CASCADE,
        related_name='allocation_requests'
    )

    # Request details
    requested_prefix = models.IntegerField()
    reason = models.TextField(blank=True)

    # Approval details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    allocated_pool = models.ForeignKey(
        ip_models.IpPool,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='allocation_requests',
        help_text=_("The actual allocated subnet from the pool")
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_allocations'
    )
    sheriff_comment = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = 'ipwizard'
        ordering = ['-created_at']

    def __str__(self):
        return "#{} - {} - /{}".format(self.pk, self.user, self.requested_prefix)

    @property
    def needs_approval(self):
        """Check if this request needs sheriff approval."""
        return self.requested_prefix < self.pool_settings.self_service_max_prefix

    @property
    def requested_clients(self):
        return 2 ** (32 - self.requested_prefix) - 2
