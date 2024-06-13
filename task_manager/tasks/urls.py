from django.urls import path
from .views import TasksView, DetailTaskView, CreateTaskView, \
                    UpdateTaskView, DeleteTaskView


urlpatterns = [
    path('', TasksView.as_view(), name='tasks'),
    path('create/', CreateTaskView.as_view(), name='create_task'),
    path('<int:pk>/', DetailTaskView.as_view(), name='task_detail'),
    path('<int:pk>/update/', UpdateTaskView.as_view(), name='update_task'),
    path('<int:pk>/delete/', DeleteTaskView.as_view(), name='delete_task'),
]
