from django.urls import path
from .views import TasksView, DetailTaskView, CreateTaskView, \
                    UpdateTaskView, DeleteTaskView


urlpatterns = [
    path('', TasksView.as_view(), name='tasks'),
    path('<int:pk>/', DetailTaskView.as_view(), name='task_detail'),
    path('create/', CreateTaskView.as_view(), name='create_task'),
]
