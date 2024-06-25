from django.urls import reverse_lazy
from django.test import override_settings

from task_manager.tests.base import BaseTestCase
from task_manager.users.models import User
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status


@override_settings(LANGUAGE_CODE='en')
class ActiveTaskProtectionTest(BaseTestCase):
    fixtures = ['task_manager/tests/fixtures/db_tasks.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.task = Task.objects.get(pk=1)

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
            'You cannot delete a status which is currently being used.')
        self.assertIn(self.task.status, Status.objects.all())
