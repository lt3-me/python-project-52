from django.urls import reverse_lazy
from django.test import TestCase
from django.utils.translation import override

from task_manager.users.models import User
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class ActiveTaskProtectionTest(TestCase):
    fixtures = ['task_manager/tests/fixtures/db_tasks.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.task = Task.objects.get(pk=1)

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
            'You cannot delete a user who is currently being used.')
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
            'You cannot delete a user who is currently being used.')
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
            'You cannot delete a status which is currently being used.')
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
            'You cannot delete a label which is currently being used.')
        self.assertIn(task_label, Label.objects.all())


class UserProtectionTest(TestCase):
    fixtures = ['task_manager/tests/fixtures/db_tasks.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.another_user = User.objects.get(pk=2)
        self.client.force_login(user=self.user)

    @override('en')
    def test_delete_another_user(self):
        response = self.client.post(
            reverse_lazy(
                'delete_user',
                kwargs={'pk': self.another_user.id}
            ), follow=True
        )
        self.assertRedirects(response, reverse_lazy('users'))
        self.assertContains(response,
                            'You have no permission to delete another user.')
        self.assertIn(self.another_user, User.objects.all())

    @override('en')
    def test_update_another_user(self):
        response = self.client.post(
            reverse_lazy(
                'update_user',
                kwargs={'pk': self.another_user.id}
            ), {}, follow=True
        )
        self.assertRedirects(response, reverse_lazy('users'))
        self.assertContains(response,
                            'You have no permission to edit another user.')
        same_other_user = User.objects.get(pk=self.another_user.id)
        self.assertEqual(self.another_user, same_other_user)
