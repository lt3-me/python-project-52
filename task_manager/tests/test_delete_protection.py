import json
import os

from django.urls import reverse_lazy
from django.test import TestCase
from django.utils.translation import override

from task_manager.users.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label

from .test_crud_tasks import create_task_object


FIXTURES_DIR_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'fixtures'
)
TESTUSER = json.load(open(os.path.join(FIXTURES_DIR_PATH, 'user.json')))
TASK = json.load(open(os.path.join(
    FIXTURES_DIR_PATH, 'task.json')))


class UserActiveTaskTest(TestCase):
    fixtures = ['task_manager/tests/fixtures/db.json']

    def setUp(self):
        self.user = User.objects.create_user(TESTUSER)
        self.task = create_task_object(TASK, self.user)

    @override('en')
    def test_delete_task_creator(self):
        self.client.force_login(user=self.user)
        response = self.client.post(
            reverse_lazy(
                'delete_user',
                kwargs={'pk': self.user.id}
            ), follow=True
        )
        self.assertRedirects(response, reverse_lazy('users'))
        self.assertContains(
            response,
            'You cannot delete a user who is currently being used.'
            )
        self.assertIn(self.user, User.objects.all())

    @override('en')
    def test_delete_task_executor(self):
        self.client.force_login(user=self.task.executor)
        response = self.client.post(
            reverse_lazy(
                'delete_user',
                kwargs={'pk': self.task.executor.id}
            ), follow=True
        )
        self.assertRedirects(response, reverse_lazy('users'))
        self.assertContains(
            response,
            'You cannot delete a user who is currently being used.'
            )
        self.assertIn(self.task.executor, User.objects.all())

    @override('en')
    def test_delete_status_related_to_task(self):
        self.client.force_login(user=self.user)
        response = self.client.post(
            reverse_lazy(
                'delete_status',
                kwargs={'pk': self.task.status.id}
            ), follow=True
        )
        self.assertRedirects(response, reverse_lazy('statuses'))
        self.assertContains(
            response,
            'You cannot delete a status which is currently being used.'
            )
        self.assertIn(self.task.status, Status.objects.all())

    @override('en')
    def test_delete_label_related_to_task(self):
        self.client.force_login(user=self.user)
        task_label = self.task.labels.all()[0]
        response = self.client.post(
            reverse_lazy(
                'delete_label',
                kwargs={'pk': task_label.id}
            ), follow=True
        )
        self.assertRedirects(response, reverse_lazy('labels'))
        self.assertContains(
            response,
            'You cannot delete a label which is currently being used.'
            )
        self.assertIn(task_label, Label.objects.all())
