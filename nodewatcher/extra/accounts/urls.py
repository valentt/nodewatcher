from django.urls import re_path, reverse_lazy
from django.contrib.auth import views as auth_views
from django.views import generic

from . import decorators, forms, views

# We pass redirect targets as a lazy unicode string as we are backreferencing. We wrap views with custom decorators to
# force anonymous and authenticated access to them (it is strange to try to register a new account while still logged
# in with another account). We redirect the user away and tell the user what has happened with messages. Some views
# use those decorators already so they are not used here. `logout_redirect` does not require authenticated access on
# purpose. We use login and logout signals to give messages to the user explaining what has happened with login
# and logout. We do not assume the user understands what is happening behind the scenes.


# Custom class-based views with decorators applied
class PasswordChangeView(auth_views.PasswordChangeView):
    form_class = forms.PasswordChangeForm
    success_url = reverse_lazy('AccountsComponent:auth_password_change_done')


class PasswordResetView(auth_views.PasswordResetView):
    form_class = forms.PasswordResetForm
    email_template_name = 'registration/password_reset_email.txt'
    success_url = reverse_lazy('AccountsComponent:auth_password_reset_done')


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    form_class = forms.SetPasswordForm
    success_url = reverse_lazy('AccountsComponent:auth_password_reset_complete')


urlpatterns = [
    # Based on "registration.backends.model_activation.urls".
    re_path(
        r'^activate/complete/$',
        decorators.anonymous_required(function=generic.TemplateView.as_view(template_name='registration/activation_complete.html')),
        name='registration_activation_complete',
    ),
    re_path(
        r'^activate/(?P<activation_key>\w+)/$',
        decorators.anonymous_required(function=views.ActivationView.as_view()),
        name='registration_activate',
    ),
    re_path(
        r'^register/$',
        decorators.anonymous_required(function=views.RegistrationView.as_view()),
        name='registration_register',
    ),
    re_path(
        r'^register/complete/$',
        decorators.anonymous_required(function=generic.TemplateView.as_view(template_name='registration/registration_complete.html')),
        name='registration_complete',
    ),
    re_path(
        r'^register/closed/$',
        decorators.anonymous_required(function=generic.TemplateView.as_view(template_name='registration/registration_closed.html')),
        name='registration_disallowed',
    ),

    # Based on "registration.auth_urls".
    re_path(
        r'^login/$',
        views.login,
        name='auth_login',
    ),
    re_path(
        r'^logout/$',
        views.logout_redirect,
        name='auth_logout',
    ),
    re_path(
        r'^password/change/$',
        decorators.authenticated_required(function=PasswordChangeView.as_view()),
        name='auth_password_change',
    ),
    re_path(
        r'^password/change/complete/$',
        decorators.authenticated_required(function=auth_views.PasswordChangeDoneView.as_view()),
        name='auth_password_change_done',
    ),
    re_path(
        r'^password/reset/$',
        decorators.anonymous_required(function=PasswordResetView.as_view()),
        name='auth_password_reset',
    ),
    re_path(
        r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$',
        decorators.anonymous_required(function=PasswordResetConfirmView.as_view()),
        name='auth_password_reset_confirm',
    ),
    re_path(
        r'^password/reset/complete/$',
        decorators.anonymous_required(function=auth_views.PasswordResetCompleteView.as_view()),
        name='auth_password_reset_complete',
    ),
    re_path(
        r'^password/reset/done/$',
        decorators.anonymous_required(function=auth_views.PasswordResetDoneView.as_view()),
        name='auth_password_reset_done',
    ),

    re_path(
        r'^email/change/complete/$',
        decorators.anonymous_required(function=generic.TemplateView.as_view(template_name='registration/email_change_complete.html')),
        name='email_change_complete',
    ),
    re_path(
        r'^$',
        views.account,
        name='user_account',
    ),
]
