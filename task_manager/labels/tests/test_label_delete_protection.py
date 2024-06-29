from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.tests.base import BaseTestCase
from task_manager.users.models import User
from task_manager.tasks.models import Task
from task_manager.labels.models import Label


class ActiveTaskProtectionTest(BaseTestCase):
    fixtures = ['task_manager/tests/fixtures/db_tasks.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.task = Task.objects.get(pk=1)

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
            _('You cannot delete a label which is currently being used.'))
        self.assertIn(task_label, Label.objects.all())
