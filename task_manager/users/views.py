from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from task_manager.users.models import User
from task_manager.users.forms import CreateUserForm
from django.utils.translation import gettext_lazy as _


class UsersView(ListView):
    template_name = 'users/index.html'
    model = User
    context_object_name = 'users'


class CreateUserView(CreateView):
    template_name = 'users/form.html'
    model = User
    form_class = CreateUserForm
    extra_context = {
        'title': _('Sign Up'),
        'button_text': _('Sign Me Up'),
    }
