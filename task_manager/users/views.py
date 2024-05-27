from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from task_manager.users.models import User
from task_manager.users.forms import CreateUserForm
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy


class UsersView(ListView):
    template_name = 'users/index.html'
    model = User
    context_object_name = 'users'
    extra_context = {
        'title': _('Users')
    }


class CreateUserView(CreateView):
    template_name = 'form.html'
    model = User
    form_class = CreateUserForm
    success_url = reverse_lazy('login')
    success_message = _('You have been signed up successfully.')
    extra_context = {
        'title': _('Sign Up'),
        'button_text': _('Sign Me Up'),
    }


class UpdateUserView(UpdateView):
    pass


class DeleteUserView(DeleteView):
    pass
