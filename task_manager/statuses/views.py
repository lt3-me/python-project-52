from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Status
# from .forms import UserDataForm
# from task_manager.mixins import LoginCheckMixin, UserCheckMixin
# from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from task_manager.mixins import LoginCheckMixin
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.
class StatusesView(LoginCheckMixin, ListView):
    template_name = 'statuses/index.html'
    model = Status
    context_object_name = 'statuses'
    extra_context = {
        'title': _('Statuses')
    }


class CreateStatusView(
        LoginCheckMixin,
        SuccessMessageMixin,
        CreateView):
    fields = ('name',)
    model = Status
    template_name = 'form.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status has been created successfully.')
    extra_context = {
        'title': _('Create status'),
        'button_text': _('Create')
    }


class UpdateStatusView(
        LoginCheckMixin,
        SuccessMessageMixin,
        UpdateView):
    fields = ('name',)
    model = Status
    template_name = 'form.html'
    success_url = reverse_lazy('statuses')
    success_message = _('Status has been edited successfully.')
    extra_context = {
        'title': _('Edit status'),
        'button_text': _('Edit')
    }


class DeleteStatusView(
        LoginCheckMixin,
        SuccessMessageMixin,
        DeleteView):
    template_name = 'statuses/delete.html'
    model = Status
    success_url = reverse_lazy('statuses')
    success_message = _('Status has been successfully deleted')
    extra_context = {
        'title': _('Delete status'),
        'button_text': _('Yes, delete'),
    }
