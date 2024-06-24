# Generated by Django 5.0.3 on 2024-06-24 05:24

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='label',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='label',
            name='name',
            field=models.CharField(default='', max_length=150, unique=True),
            preserve_default=False,
        ),
        migrations.AlterModelTable(
            name='label',
            table='labels',
        ),
    ]
