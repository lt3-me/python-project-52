from django.db import models


# Create your models here.
class Label(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        blank=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'labels'
        app_label = 'labels'
