from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Status
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from task_manager.mixins import LoginCheckMixin, DeleteProtectionMessageMixin
from django.contrib.messages.views import SuccessMessageMixin


class StatusesView(LoginCheckMixin, ListView):
    template_name = 'statuses/index.html'
    model = Status
    context_object_name = 'statuses'
    extra_context = {
        'title': _('Statuses')
    }


class StatusFormBaseView(LoginCheckMixin, SuccessMessageMixin):
    fields = ('name',)
    model = Status
    template_name = 'form.html'
    success_url = reverse_lazy('statuses')


class CreateStatusView(StatusFormBaseView, CreateView):
    success_message = _('Status has been created successfully.')
    extra_context = {
        'title': _('Create status'),
        'button_text': _('Create')
    }

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['name'].label = _('Name')
        return form


class UpdateStatusView(StatusFormBaseView, UpdateView):
    success_message = _('Status has been edited successfully.')
    extra_context = {
        'title': _('Edit status'),
        'button_text': _('Edit')
    }


class DeleteStatusView(
        LoginCheckMixin,
        SuccessMessageMixin,
        DeleteProtectionMessageMixin,
        DeleteView):
    template_name = 'delete.html'
    model = Status
    protected_url = success_url = reverse_lazy('statuses')
    success_message = _('Status has been successfully deleted.')
    protected_message = _(
            'You cannot delete a status which is currently being used.')
    extra_context = {
        'title': _('Delete status'),
        'button_text': _('Yes, delete'),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deleted_name'] = self.object.name
        return context
