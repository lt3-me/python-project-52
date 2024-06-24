from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Label
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from task_manager.mixins import LoginCheckMixin, DeleteProtectionMessageMixin
from django.contrib.messages.views import SuccessMessageMixin


class LabelsView(LoginCheckMixin, ListView):
    template_name = 'labels/index.html'
    model = Label
    context_object_name = 'labels'
    extra_context = {
        'title': _('Labels')
    }


class LabelFormBaseView(LoginCheckMixin, SuccessMessageMixin):
    model = Label
    fields = ('name',)
    template_name = 'form.html'
    success_url = reverse_lazy('labels')
    extra_context = {}

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['name'].label = _('Name')
        return form


class CreateLabelView(LabelFormBaseView, CreateView):
    success_message = _('Label has been created successfully.')
    extra_context = {
        'title': _('Create label'),
        'button_text': _('Create')
    }


class UpdateLabelView(LabelFormBaseView, UpdateView):
    success_message = _('Label has been edited successfully.')
    extra_context = {
        'title': _('Edit label'),
        'button_text': _('Edit')
    }


class DeleteLabelView(
        LoginCheckMixin,
        SuccessMessageMixin,
        DeleteProtectionMessageMixin,
        DeleteView):
    template_name = 'delete.html'
    model = Label
    success_message = _('Label has been successfully deleted.')
    protected_message = _(
        'You cannot delete a label which is currently being used.')
    protected_url = success_url = reverse_lazy('labels')
    extra_context = {
        'title': _('Delete label'),
        'button_text': _('Yes, delete'),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deleted_name'] = self.object.name
        return context
