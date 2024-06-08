from django.db import models
from task_manager.users.models import User
from task_manager.statuses.models import Status


class Task(models.Model):
    name = models.CharField(
        max_length=150,
        blank=False,
        unique=True
    )
    description = models.TextField(
        max_length=1000,
        blank=True
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='statuses',
        blank=False
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='creator',
        blank=False
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='executor',
        blank=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tasks'
        app_label = 'tasks'
