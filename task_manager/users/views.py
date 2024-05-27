from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from task_manager.users.models import User
from task_manager.users.forms import UserDataForm
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy


class UsersView(ListView):
    template_name = 'users/index.html'
    model = User
    context_object_name = 'users'
    extra_context = {
        'title': _('Users')
    }


class CreateUserView(SuccessMessageMixin, CreateView):
    template_name = 'form.html'
    model = User
    form_class = UserDataForm
    success_url = reverse_lazy('login')
    success_message = _('You have been signed up successfully.')
    extra_context = {
        'title': _('Sign Up'),
        'button_text': _('Sign Me Up'),
    }


class UpdateUserView(UpdateView):
    template_name = 'form.html'
    model = User
    form_class = UserDataForm
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('users')
    success_message = _('User has been successfully updated.')
    permission_message = _('You have no permission to edit another user.')
    permission_url = reverse_lazy('users')
    extra_context = {
        'title': _('Edit User Info'),
        'button_text': _('Update'),
    }


class DeleteUserView(DeleteView):
    pass
