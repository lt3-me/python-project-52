import json
import os

from django.urls import reverse_lazy
from django.test import TestCase

from task_manager.users.models import User
from task_manager.labels.models import Label

FIXTURES_DIR_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'fixtures'
)
TESTUSER = json.load(open(os.path.join(
    FIXTURES_DIR_PATH, 'user.json')))
LABEL = json.load(open(os.path.join(
    FIXTURES_DIR_PATH, 'label.json')))
LABEL_EDIT = json.load(open(os.path.join(
    FIXTURES_DIR_PATH, 'label_edit.json')))


class CRUDTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(TESTUSER)
        self.client.force_login(user=user)

    def test_label_create(self):
        response = self.client.get(reverse_lazy('create_status'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse_lazy('create_label'), LABEL
        )
        self.assertRedirects(response, reverse_lazy('labels'))
        last_created = Label.objects.latest('created_at')
        self.assertEqual(last_created.name, LABEL.get('name'))

    def test_label_read(self):
        Label.objects.create(**LABEL)
        response = self.client.get(reverse_lazy('labels'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, LABEL.get('name'))

    def test_label_update(self):
        label = Label.objects.create(**LABEL)
        response = self.client.post(
            reverse_lazy(
                'update_label',
                kwargs={'pk': label.id}
            ), LABEL_EDIT
        )
        self.assertRedirects(response, reverse_lazy('labels'))
        label = Label.objects.get(pk=label.id)
        self.assertEqual(label.name, LABEL_EDIT.get('name'))

    def test_label_delete(self):
        label = Label.objects.create(**LABEL)
        response = self.client.post(
            reverse_lazy(
                'delete_label',
                kwargs={'pk': label.id}
            )
        )
        self.assertRedirects(response, reverse_lazy('labels'))
        self.assertNotIn(label, Label.objects.all())
