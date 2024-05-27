from django.urls import path
from .views import UsersView, CreateUserView  # , UpdateUserView, DeleteUserView

urlpatterns = [
    path('', UsersView.as_view(), name='users'),
    path('create/', CreateUserView.as_view(), name='create_user'),
    # path('<int:pk>/update/', UpdateUserView.as_view(), name='user_update'),
    # path('<int:pk>/delete/', DeleteUserView.as_view(), name='user_delete'),
]
