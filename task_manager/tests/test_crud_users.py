import json
import os

from django.urls import reverse_lazy
from django.test import TestCase, override_settings

from task_manager.users.models import User


FIXTURES_DIR_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'fixtures'
)
TESTUSER = json.load(open(os.path.join(FIXTURES_DIR_PATH, 'user.json')))
USER_EDIT = json.load(open(os.path.join(FIXTURES_DIR_PATH, 'user_edit.json')))


@override_settings(LANGUAGE_CODE='en')
class CRUDTest(TestCase):
    def test_user_create(self):
        response = self.client.get(reverse_lazy('create_user'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse_lazy('create_user'),
            TESTUSER
        )
        self.assertRedirects(response, reverse_lazy('login'))
        user = User.objects.latest('date_joined')
        self.assertEqual(user.username, TESTUSER.get('username'))

    def test_user_read(self):
        User.objects.create_user(TESTUSER)
        response = self.client.get(reverse_lazy('users'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, TESTUSER.get('username'))
        self.assertContains(response, TESTUSER.get('first_name'))
        self.assertContains(response, TESTUSER.get('last_name'))

    def test_user_update(self):
        user = User.objects.create_user(TESTUSER)
        self.client.force_login(user=user)
        response = self.client.post(
            reverse_lazy(
                'update_user',
                kwargs={'pk': user.id}
            ), USER_EDIT
        )
        self.assertRedirects(response, reverse_lazy('users'))
        user = User.objects.get(pk=user.id)
        self.assertEqual(user.first_name, USER_EDIT.get('first_name'))
        self.assertEqual(user.last_name, USER_EDIT.get('last_name'))

    def test_user_delete(self):
        user = User.objects.create_user(TESTUSER)
        self.client.force_login(user=user)
        self.client.post(
            reverse_lazy(
                'delete_user',
                kwargs={'pk': user.id}
            )
        )
        self.assertNotIn(user, User.objects.all())
