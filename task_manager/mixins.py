from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect


class LoginCheckMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')
    login_fail_message = _('You are not logged in! Please log in.')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.login_fail_message)
            return redirect(self.login_url)

        return super().dispatch(request, *args, **kwargs)


class UserCheckMixin(UserPassesTestMixin):
    permission_message = None
    permission_url = None

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.permission_message)
        return redirect(self.permission_url)
