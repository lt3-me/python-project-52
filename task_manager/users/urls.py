from django.urls import path
from task_manager.users import views

urlpatterns = [
    path('', views.UsersView.as_view(), name='users'),
    path('create/', views.CreateUserView.as_view(), name='create_user'),

]
