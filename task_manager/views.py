from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'form.html'
    form_class = AuthenticationForm
    next_page = reverse_lazy('index')
    success_message = _('You have been logged in successfully.')
    extra_context = {
        'title': _('Login'),
        'button_text': _('Log Me In'),
    }


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')
    success_message = _('You have been logged out.')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('You have been logged out.'))
        return super().dispatch(request, *args, **kwargs)
