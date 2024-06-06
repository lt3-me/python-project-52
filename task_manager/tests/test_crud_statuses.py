from django.urls import reverse_lazy
from django.test import TestCase

from task_manager.users.models import User
from task_manager.statuses.models import Status

STATUS_NAME = 'test_status'
UPDATED_NAME = 'updated_status'


class CRUDTest(TestCase):
    def test_not_logged_in(self):
        response = self.client.get(reverse_lazy('statuses'))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse_lazy('create_status'))
        self.assertEqual(response.status_code, 302)

    def test_status_create(self):
        user = User.objects.create_user(username='test', password='123')
        self.client.force_login(user=user)
        response = self.client.get(reverse_lazy('create_status'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse_lazy('create_status'), {'name': STATUS_NAME}
        )
        last_created = Status.objects.latest('created_at')
        self.assertEqual(last_created.name, STATUS_NAME)

    def test_status_read(self):
        user = User.objects.create_user(username='test', password='123')
        self.client.force_login(user=user)
        Status.objects.create(name=STATUS_NAME)
        response = self.client.get(reverse_lazy('statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, STATUS_NAME)

    def test_status_update(self):
        user = User.objects.create_user(username='test', password='123')
        self.client.force_login(user=user)
        status = Status.objects.create(name=STATUS_NAME)
        response = self.client.post(
            reverse_lazy(
                'update_status',
                kwargs={'pk': status.id}
            ), {'name': UPDATED_NAME}
        )
        self.assertRedirects(response, reverse_lazy('statuses'))
        status = Status.objects.get(pk=status.id)
        self.assertEqual(status.name, UPDATED_NAME)

    def test_status_delete(self):
        user = User.objects.create_user(username='test', password='123')
        self.client.force_login(user=user)
        status = Status.objects.create(name=STATUS_NAME)
        response = self.client.post(
            reverse_lazy(
                'delete_status',
                kwargs={'pk': status.id}
            )
        )
        self.assertRedirects(response, reverse_lazy('statuses'))
        self.assertNotIn(status, Status.objects.all())
