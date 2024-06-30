from django.urls import reverse_lazy
from task_manager.tests.base import BaseTestCase
from django.utils.translation import gettext_lazy as _

from task_manager.users.models import User
from task_manager.tasks.models import Task


class DeleteProtectionTest(BaseTestCase):
    fixtures = ['db_tasks.json']

    def test_delete_task_of_another_user(self):
        new_user = User.objects.create_user('test_username')
        self.client.force_login(user=new_user)
        task_id = Task.objects.first().id
        response = self.client.post(
            reverse_lazy(
                'delete_task',
                kwargs={'pk': task_id}
            ), follow=True
        )
        self.assertRedirects(response, reverse_lazy('tasks'))
        self.assertContains(
            response,
            _('Task can be deleted only by the creator.'))
        self.assertTrue(Task.objects.filter(id=task_id).exists())
