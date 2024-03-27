from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    full_name = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'
