from django import forms
from django.utils.translation import gettext_lazy as _
from task_manager.users.models import User
from task_manager.statuses.models import Status
from .models import Task


class TaskForm(forms.ModelForm):
    name = forms.CharField(
        max_length=150,
        required=True,
        label=_("Name")
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'maxlength': 1000}),
        required=False,
        label=_('Description')
    )
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        label=_('Status')
    )
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label=_('Executor')
    )

    class Meta:
        model = Task
        fields = (
            'name',
            'description',
            'status',
            'executor'
        )
