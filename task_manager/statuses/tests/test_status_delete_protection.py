from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.tests.base import BaseTestCase
from task_manager.users.models import User
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status


class ActiveTaskProtectionTest(BaseTestCase):
    fixtures = ['db_tasks.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.task = Task.objects.get(pk=1)

    def test_delete_status_related_to_task(self):
        self.client.force_login(user=self.user)
        id = self.task.status.id
        response = self.client.post(
            reverse_lazy(
                'delete_status',
                kwargs={'pk': id}
            ), follow=True
        )
        self.assertRedirects(response, reverse_lazy('statuses'))
        self.assertContains(
            response,
            _('You cannot delete a status which is currently being used.'))
        self.assertTrue(Status.objects.filter(id=id).exists())
