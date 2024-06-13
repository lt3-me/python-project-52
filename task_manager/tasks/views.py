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


# Create your views here.
class TasksView(LoginCheckMixin, FilterView):
    template_name = 'tasks/index.html'
    model = Task
    filterset_class = TaskFilter
    context_object_name = 'tasks'
    extra_context = {
        'title': _('Tasks'),
        'button_text': _('Show')
    }


class DetailTaskView(LoginCheckMixin, DetailView):
    template_name = 'tasks/detail.html'
    model = Task
    context_object_name = 'task'
    extra_context = {
        'title': _('Task preview')
    }


class CreateTaskView(
        LoginCheckMixin,
        SuccessMessageMixin,
        CreateView):
    form_class = TaskForm
    model = Task
    template_name = 'form.html'
    success_url = reverse_lazy('tasks')
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
        LoginCheckMixin,
        SuccessMessageMixin,
        AccessOnlyByCreatorMixin,
        UpdateView):
    pass


class DeleteTaskView(
        LoginCheckMixin,
        SuccessMessageMixin,
        AccessOnlyByCreatorMixin,
        DeleteView):
    pass
