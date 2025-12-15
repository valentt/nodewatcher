from django import shortcuts, template
from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth import models as auth_models, views as auth_views
from django.contrib.sites import shortcuts as sites_shortcuts
from django import urls as urlresolvers
from django.utils.translation import gettext_lazy as _

from django_registration.backends.activation import views as registration_views

from . import decorators, forms, utils


class RegistrationView(registration_views.RegistrationView):
    def get_form_class(self):
        """
        Returns the default form class used for user registration.

        It returns `nodewatcher.extra.accounts.forms.AccountRegistrationForm` form
        which contains fields for both user and user profile objects.
        """

        return utils.initial_accepts_request(self.request, forms.AccountRegistrationForm)

    def get_success_url(self, user):
        return ('AccountsComponent:registration_complete', (), {})


class ActivationView(registration_views.ActivationView):
    def get_success_url(self, user):
        return ('AccountsComponent:registration_activation_complete', (), {})


def user(request, username):
    """
    This view displays a public page for a given user.
    """

    user = shortcuts.get_object_or_404(auth_models.User, username=username)

    return shortcuts.render(request, 'users/user.html', {'profileuser': user})


def get_user_copy(user):
    if isinstance(user, auth_models.AnonymousUser):
        return auth_models.AnonymousUser()

    for backend in auth.get_backends():
        user_copy = backend.get_user(user.pk)
        if user_copy is not None:
            return user_copy

    assert False


@decorators.authenticated_required
def account(request):
    """
    View which displays `nodewatcher.extra.accounts.forms.AccountChangeForm` form for users to change their account.

    If the user changes their e-mail address her account is inactivated and they gets an activation e-mail.
    """

    assert request.user.is_authenticated

    if request.method == 'POST':
        stored_user = get_user_copy(request.user)

        form = forms.AccountChangeForm(request.POST, instance=[request.user, request.user.profile])

        if form.is_valid():
            objs = form.save()
            messages.success(request, _("Your account has been successfully updated."), fail_silently=True)

            # The last element is user profile object.
            # Note: Email change re-activation was removed as RegistrationProfile
            # is no longer available in modern django-registration.
            # TODO: Implement proper email verification if required.
            return shortcuts.redirect(objs[-1])
        else:
            # Restore user request object as it is changed by form.is_valid.
            request.user = stored_user
            if hasattr(request.user, '_profile_cache'):
                # Invalidates profile cache.
                delattr(request.user, '_profile_cache')
    else:
        form = forms.AccountChangeForm(instance=[request.user, request.user.profile])

    return shortcuts.render(request, 'users/account.html', {'form': form})


def logout_redirect(request, next_page=None, redirect_field_name=auth.REDIRECT_FIELD_NAME):
    """
    Logs out the user and redirects them to the log-in page or elsewhere, as specified.

    Logs out the user directly and redirects to the appropriate page.
    """

    auth.logout(request)

    if next_page is None:
        next_page = request.POST.get(redirect_field_name) or request.GET.get(redirect_field_name) or settings.LOGIN_URL

    return shortcuts.redirect(next_page)


class LoginView(auth_views.LoginView):
    """
    Login view that uses our custom authentication form.
    """

    authentication_form = forms.AuthenticationForm


@decorators.anonymous_required
def login(request, *args, **kwargs):
    """
    Displays the login form and handles the login action.

    A wrapper around Django's LoginView which uses our authentication form.
    """

    assert request.user.is_anonymous

    kwargs.setdefault('authentication_form', forms.AuthenticationForm)
    return LoginView.as_view(**kwargs)(request)
