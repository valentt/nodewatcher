from django import db, dispatch
from django.conf import settings
from django.db import models as django_models
from django.db.models import signals as models_signals
from django.contrib.auth import models as auth_models
from django.template import loader
from django.utils.translation import gettext_lazy as _

from phonenumber_field import modelfields as phonenumber_fields
from django_countries import fields as country_fields

from nodewatcher.modules.administration.projects import models as projects_models

from . import fields as account_fields


ATTRIBUTION_CHOICES = (
    ('name', _("Use my full name")),
    ('username', _("Use my username")),
    ('nothing', _("Hide me")),
)


class UserProfileAndSettings(django_models.Model):
    """
    This class represents an user profile and settings.
    """

    user = django_models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=django_models.CASCADE, editable=False, primary_key=True, related_name='profile')

    # Fields can be null in the model (so that we can automatically create the profile
    # object as needed), but they are still required when edited through forms.
    phone_number = phonenumber_fields.PhoneNumberField(_('phone number'), help_text=_('Please enter your phone number in international format (e.g. +38651654321) for use in emergency. It will be visible only to network administrators.'), null=True)
    country = country_fields.CountryField(blank=True, help_text=_('Where are you from? It will be public.'))
    language = account_fields.LanguageField(help_text=_('Choose the language you wish this site to be in.'))
    default_project = django_models.ForeignKey(projects_models.Project, on_delete=django_models.SET_NULL, default=projects_models.project_default, null=True, verbose_name=_('default project'))
    attribution = django_models.CharField(_('attribution'), max_length=8, choices=ATTRIBUTION_CHOICES, default=ATTRIBUTION_CHOICES[0][0], help_text=_('What to use when we want to give you public attribution for your participation and contribution?'))

    # AccountRegistrationForm and AccountChangeForm uses this.
    fieldsets = (
        (_('Additional personal info'), {
            'fields': ('phone_number', 'country'),
        }),
        (_('Settings'), {
            'fields': ('language', 'default_project'),
        }),
        (_('Privacy'), {
            'fields': ('attribution',),
        }),
    )

    class Meta:
        verbose_name = _('user profile and settings')
        verbose_name_plural = _('users profiles and settings')

    def __str__(self):
        return u"profile and settings for %s" % (self.user)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('AccountsComponent:user_account',)


@dispatch.receiver(models_signals.post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid='create_profile_and_settings')
def create_profile_and_settings(sender, instance, created, **kwargs):
    if not created:
        return

    try:
        # We try to create profile and settings object so that it always exist.
        UserProfileAndSettings.objects.create(user=instance)
    except db.IntegrityError:
        pass


@dispatch.receiver(models_signals.post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid='assign_default_permissions')
def assign_default_permissions(sender, instance, created, **kwargs):
    if not created:
        return

    add_node_permission = auth_models.Permission.objects.get_by_natural_key(codename='add_node', app_label='core', model='node')
    instance.user_permissions.add(add_node_permission)


# NOTE: The old django-registration monkey-patching code was removed as
# django-registration 3.x no longer has RegistrationProfile model.
# Activation email customization should be done through the new API
# (signal handlers or view subclassing) if needed.
