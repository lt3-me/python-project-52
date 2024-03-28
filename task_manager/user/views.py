from django.shortcuts import render
from django.views import View
from task_manager.user.models import User


class UsersView(View):

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(request, 'users/index.html', context={
            'users': users})
