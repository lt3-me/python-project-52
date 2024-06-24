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


class TaskBaseView(LoginCheckMixin):
    template_name = 'tasks/detail.html'
    model = Task
    context_object_name = 'task'


class TasksView(TaskBaseView, FilterView):
    filterset_class = TaskFilter
    extra_context = {
        'title': _('Tasks'),
        'button_text': _('Show')
    }


class DetailTaskView(TaskBaseView, DetailView):
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
        AccessOnlyByCreatorMixin,
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
    success_url = reverse_lazy('tasks')
    success_message = _('Task has been successfully deleted.')
    author_message = _('Task can be deleted only by the creator.')
    author_url = reverse_lazy('tasks')
    extra_context = {
        'title': _('Delete task'),
        'button_text': _('Yes, delete'),
    }
