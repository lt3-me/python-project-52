from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Status
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

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['name'].label = _('Name')
        return form


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
    template_name = 'delete.html'
    model = Status
    success_url = reverse_lazy('statuses')
    success_message = _('Status has been successfully deleted')
    extra_context = {
        'title': _('Delete status'),
        'button_text': _('Yes, delete'),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deleted_name'] = self.object.name
        return context
