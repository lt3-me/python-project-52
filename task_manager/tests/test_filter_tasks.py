import re

from django.urls import reverse_lazy
from django.test import TestCase

from task_manager.users.models import User
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class FilterTasksTest(TestCase):
    fixtures = ['task_manager/tests/fixtures/db_tasks.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.client.force_login(user=self.user)

    def test_filter_by_status(self):
        self.status = Status.objects.get(pk=2)
        response = self.client.get(
            reverse_lazy('tasks'),
            data={'status': self.status.id}
        )
        pattern = re.compile(f'<tr>.*?{self.status.name}.*?</tr>', re.DOTALL)
        status_count = len(pattern.findall(response.content.decode('utf-8')))
        amount_expected = len(self.status.tasks.all())
        self.assertEqual(status_count, amount_expected)

    def test_filter_by_executor(self):
        response = self.client.get(
            reverse_lazy('tasks'),
            data={'executor': self.user.id}
        )
        pattern = re.compile(f'<tr>.*?{self.user}.*?</tr>', re.DOTALL)
        status_count = len(pattern.findall(response.content.decode('utf-8')))
        amount_expected = len(self.user.executed_tasks.all())
        self.assertEqual(status_count, amount_expected)

    def test_filter_by_label(self):
        self.label = Label.objects.get(pk=2)
        response = self.client.get(
            reverse_lazy('tasks'),
            data={'labels': self.label.id}
        )
        pattern = re.compile('<tr>.*?<td.*?</tr>', re.DOTALL)
        status_count = len(pattern.findall(response.content.decode('utf-8')))
        amount_expected = len(self.label.tasks.all())
        self.assertEqual(status_count, amount_expected)
        for labeled_task in self.label.tasks.all():
            self.assertContains(response, labeled_task.name)

    def test_show_only_your_own(self):
        response = self.client.get(
            reverse_lazy('tasks'),
            data={'current_user_tasks': 'on'}
        )
        pattern = re.compile(f'<tr>.*?{self.user}.*?</tr>', re.DOTALL)
        status_count = len(pattern.findall(response.content.decode('utf-8')))
        amount_expected = len(self.user.created_tasks.all())
        self.assertEqual(status_count, amount_expected)

    def test_complex_filter(self):
        self.task = Task.objects.get(pk=5)
        self.assertEqual(self.task.creator.id, self.user.id)
        response = self.client.get(
            reverse_lazy('tasks'),
            data={
                'status': self.task.status.id,
                'executor': self.task.executor.id,
                'labels': self.task.labels.first().id,
                'current_user_tasks': 'on'}
        )
        pattern = re.compile(
            f'<tr>.*?{self.task.name}'
            f'.*?{self.task.status.name}'
            f'.*?{self.user}'
            f'.*?{self.task.executor}'
            r'.*?</tr>',
            re.DOTALL
        )
        self.assertRegex(response.content.decode('utf-8'), pattern)
