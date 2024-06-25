from django.urls import reverse_lazy
from task_manager.tests.base import BaseTestCase

from task_manager.users.models import User
from task_manager.labels.models import Label


class CRUDTest(BaseTestCase):
    def setUp(self):
        user = User.objects.create_user('test_username')
        self.client.force_login(user=user)
        self.label = self.load_fixture('label.json')

    def test_label_create(self):
        response = self.client.get(reverse_lazy('create_status'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse_lazy('create_label'), self.label
        )
        self.assertRedirects(response, reverse_lazy('labels'))
        last_created = Label.objects.latest('created_at')
        self.assertEqual(last_created.name, self.label.get('name'))

    def test_label_read(self):
        Label.objects.create(**self.label)
        response = self.client.get(reverse_lazy('labels'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.label.get('name'))

    def test_label_update(self):
        label_edit = self.load_fixture('label_edit.json')
        label = Label.objects.create(**self.label)
        response = self.client.post(
            reverse_lazy(
                'update_label',
                kwargs={'pk': label.id}
            ), label_edit
        )
        self.assertRedirects(response, reverse_lazy('labels'))
        label = Label.objects.get(pk=label.id)
        self.assertEqual(label.name, label_edit.get('name'))

    def test_label_delete(self):
        label = Label.objects.create(**self.label)
        response = self.client.post(
            reverse_lazy(
                'delete_label',
                kwargs={'pk': label.id}
            )
        )
        self.assertRedirects(response, reverse_lazy('labels'))
        self.assertNotIn(label, Label.objects.all())
