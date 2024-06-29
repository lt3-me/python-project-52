from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.tests.base import BaseTestCase
from task_manager.users.models import User
from task_manager.tasks.models import Task


class UserProtectionTest(BaseTestCase):
    fixtures = ['task_manager/tests/fixtures/db_tasks.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.another_user = User.objects.get(pk=2)
        self.client.force_login(user=self.user)

    def test_delete_another_user(self):
        response = self.client.post(
            reverse_lazy(
                'delete_user',
                kwargs={'pk': self.another_user.id}
            ), follow=True
        )
        self.assertRedirects(response, reverse_lazy('users'))
        self.assertContains(response,
                            _('You have no permission to delete another user.'))
        self.assertIn(self.another_user, User.objects.all())

    def test_update_another_user(self):
        response = self.client.post(
            reverse_lazy(
                'update_user',
                kwargs={'pk': self.another_user.id}
            ), {}, follow=True
        )
        self.assertRedirects(response, reverse_lazy('users'))
        self.assertContains(response,
                            _('You have no permission to edit another user.'))
        same_other_user = User.objects.get(pk=self.another_user.id)
        self.assertEqual(self.another_user, same_other_user)


class ActiveTaskProtectionTest(BaseTestCase):
    fixtures = ['task_manager/tests/fixtures/db_tasks.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.task = Task.objects.get(pk=1)

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
            _('You cannot delete a user who is currently being used.'))
        self.assertIn(self.user, User.objects.all())

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
            _('You cannot delete a user who is currently being used.'))
        self.assertIn(self.task.executor, User.objects.all())
