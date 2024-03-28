from django.shortcuts import render
from django.views import View
from . import models


class UsersView(View):

    def get(self, request, *args, **kwargs):
        users = models.User.objects.all()
        return render(request, 'users/index.html', context={
            'users': users})
