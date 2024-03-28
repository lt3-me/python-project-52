from django.urls import path
from task_manager.user import views

urlpatterns = [
    path('', views.UsersView.as_view(), name='users'),
]
