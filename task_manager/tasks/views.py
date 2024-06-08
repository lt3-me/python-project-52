from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Task
from task_manager.users.models import User
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from task_manager.mixins import LoginCheckMixin
from django.contrib.messages.views import SuccessMessageMixin
from .forms import TaskForm


# Create your views here.
class TasksView(LoginCheckMixin, ListView):
    template_name = 'tasks/index.html'
    model = Task
    context_object_name = 'tasks'
    extra_context = {
        'title': _('Tasks')
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
