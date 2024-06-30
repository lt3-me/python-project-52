from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins import LoginCheckMixin
from task_manager.mixins import AccessOnlyByCreatorMixin

from .models import Task
from task_manager.users.models import User

from .forms import TaskForm
from .filters import TaskFilter


class TasksView(LoginCheckMixin, FilterView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tasks/index.html'
    filterset_class = TaskFilter
    extra_context = {
        'title': _('Tasks'),
        'button_text': _('Show')
    }


class DetailTaskView(LoginCheckMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'tasks/detail.html'
    extra_context = {
        'title': _('Task preview')
    }


class TaskFormBaseView(LoginCheckMixin, SuccessMessageMixin):
    form_class = TaskForm
    model = Task
    template_name = 'form.html'
    success_url = reverse_lazy('tasks')


class CreateTaskView(TaskFormBaseView, CreateView):
    success_message = _('Task has been created successfully.')
    extra_context = {
        'title': _('Create task'),
        'button_text': _('Create')
    }

    def form_valid(self, form):
        user = self.request.user
        form.instance.creator = User.objects.get(pk=user.pk)
        return super().form_valid(form)


class UpdateTaskView(
        TaskFormBaseView,
        UpdateView):
    success_message = _('Task has been edited successfully.')
    extra_context = {
        'title': _('Edit task'),
        'button_text': _('Edit'),
    }


class DeleteTaskView(
        LoginCheckMixin,
        SuccessMessageMixin,
        AccessOnlyByCreatorMixin,
        DeleteView):
    template_name = 'delete.html'
    model = Task
    success_message = _('Task has been successfully deleted.')
    permission_message = _('Task can be deleted only by the creator.')
    permission_url = success_url = reverse_lazy('tasks')
    extra_context = {
        'title': _('Delete task'),
        'button_text': _('Yes, delete'),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_label'] = self.object.name
        return context
