import json
import os

from django.urls import reverse_lazy
from django.test import TestCase

from task_manager.users.models import User
from task_manager.statuses.models import Status

FIXTURES_DIR_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'fixtures'
)
TESTUSER = json.load(open(os.path.join(
    FIXTURES_DIR_PATH, 'user.json')))
STATUS = json.load(open(os.path.join(
    FIXTURES_DIR_PATH, 'status.json')))
STATUS_EDIT = json.load(open(os.path.join(
    FIXTURES_DIR_PATH, 'status_edit.json')))


class CRUDTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(TESTUSER)
        self.client.force_login(user=user)

    def test_status_create(self):
        response = self.client.get(reverse_lazy('create_status'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse_lazy('create_status'), STATUS
        )
        self.assertRedirects(response, reverse_lazy('statuses'))
        last_created = Status.objects.latest('created_at')
        self.assertEqual(last_created.name, STATUS.get('name'))

    def test_status_read(self):
        Status.objects.create(**STATUS)
        response = self.client.get(reverse_lazy('statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, STATUS.get('name'))

    def test_status_update(self):
        status = Status.objects.create(**STATUS)
        response = self.client.post(
            reverse_lazy(
                'update_status',
                kwargs={'pk': status.id}
            ), STATUS_EDIT
        )
        self.assertRedirects(response, reverse_lazy('statuses'))
        status = Status.objects.get(pk=status.id)
        self.assertEqual(status.name, STATUS_EDIT.get('name'))

    def test_status_delete(self):
        status = Status.objects.create(**STATUS)
        response = self.client.post(
            reverse_lazy(
                'delete_status',
                kwargs={'pk': status.id}
            )
        )
        self.assertRedirects(response, reverse_lazy('statuses'))
        self.assertNotIn(status, Status.objects.all())
