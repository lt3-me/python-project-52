from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import ProtectedError


class LoginCheckMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')
    login_fail_message = _('You are not logged in! Please log in.')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.login_fail_message)
            return redirect(self.login_url)

        return super().dispatch(request, *args, **kwargs)


class UserPermissionCheckMixin(UserPassesTestMixin):
    permission_message = None
    permission_url = None

    def handle_no_permission(self):
        messages.error(self.request, self.permission_message)
        return redirect(self.permission_url)


class UserCheckMixin(UserPermissionCheckMixin):
    def test_func(self):
        return self.get_object() == self.request.user


class AccessOnlyByCreatorMixin(UserPermissionCheckMixin):
    def test_func(self):
        return self.get_object().creator == self.request.user


class DeleteProtectionMessageMixin:
    protected_message = None
    protected_url = None

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_message)
            return redirect(self.protected_url)
