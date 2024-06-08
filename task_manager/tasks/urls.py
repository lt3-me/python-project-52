from django.urls import path
from .views import TasksView, CreateTaskView

urlpatterns = [
    path('', TasksView.as_view(), name='tasks'),
    path('create/', CreateTaskView.as_view(), name='create_task'),
]
