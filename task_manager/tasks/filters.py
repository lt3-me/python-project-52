from django_filters import FilterSet, BooleanFilter, ModelChoiceFilter
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Task
from task_manager.labels.models import Label


class TaskFilter(FilterSet):
    labels = ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_('Label')
    )

    current_user_tasks = BooleanFilter(
        label=_('Only my own tasks'),
        widget=forms.CheckboxInput,
        method='get_current_user_tasks',
    )

    def get_current_user_tasks(self, queryset, _, value):
        if value:
            user = self.request.user
            return queryset.filter(creator=user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor']
