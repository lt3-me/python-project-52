from django.db import models
from task_manager.users.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


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
        related_name='tasks',
        blank=False
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='created_tasks',
        blank=False
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='executed_tasks',
        blank=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    labels = models.ManyToManyField(
        Label,
        through='TaskLabelManyToMany',
        through_fields=('task', 'label'),
        related_name='tasks',
        blank=True
    )

    def __str__(self):
        return self.name


class TaskLabelManyToMany(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
