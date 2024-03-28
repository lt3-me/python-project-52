# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser


# class User(AbstractBaseUser):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=30, unique=True)
#     full_name = models.CharField(max_length=60)
#     created_at = models.DateTimeField(auto_now_add=True)

#     password = models.CharField(max_length=30)

#     def get_full_name(self):
#         return self.full_name

#     def get_short_name(self):
#         return self.name

#     def __str__(self):
#         return self.name

#     class Meta:
#         db_table = 'users'
#         app_label = 'task_manager'

#     USERNAME_FIELD = 'name'
