from django.urls import reverse_lazy
from task_manager.tests.base import BaseTestCase

from task_manager.users.models import User
from task_manager.statuses.models import Status


class CRUDTest(BaseTestCase):
    def setUp(self):
        testuser = self.load_fixture('user.json')
        user = User.objects.create_user(testuser)
        self.client.force_login(user=user)
        self.status = self.load_fixture('status.json')

    def test_status_create(self):
        response = self.client.get(reverse_lazy('create_status'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse_lazy('create_status'), self.status
        )
        self.assertRedirects(response, reverse_lazy('statuses'))
        last_created = Status.objects.latest('created_at')
        self.assertEqual(last_created.name, self.status.get('name'))

    def test_status_read(self):
        Status.objects.create(**self.status)
        response = self.client.get(reverse_lazy('statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.status.get('name'))

    def test_status_update(self):
        status_edit = self.load_fixture('status_edit.json')
        status = Status.objects.create(**self.status)
        response = self.client.post(
            reverse_lazy(
                'update_status',
                kwargs={'pk': status.id}
            ), status_edit
        )
        self.assertRedirects(response, reverse_lazy('statuses'))
        status = Status.objects.get(pk=status.id)
        self.assertEqual(status.name, status_edit.get('name'))

    def test_status_delete(self):
        status = Status.objects.create(**self.status)
        response = self.client.post(
            reverse_lazy(
                'delete_status',
                kwargs={'pk': status.id}
            )
        )
        self.assertRedirects(response, reverse_lazy('statuses'))
        self.assertNotIn(status, Status.objects.all())
