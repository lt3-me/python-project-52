from django.urls import reverse_lazy
from django.test import override_settings

from task_manager.tests.base import BaseTestCase
from task_manager.users.models import User


@override_settings(LANGUAGE_CODE='en')
class CRUDTest(BaseTestCase):
    def setUp(self):
        self.testuser = self.load_fixture('user.json')

    def test_user_create(self):
        response = self.client.get(reverse_lazy('create_user'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse_lazy('create_user'),
            self.testuser
        )
        self.assertRedirects(response, reverse_lazy('login'))
        user = User.objects.latest('date_joined')
        self.assertEqual(user.username, self.testuser.get('username'))

    def test_user_create_same_username(self):
        pass

    def test_user_read(self):
        User.objects.create_user(self.testuser)
        response = self.client.get(reverse_lazy('users'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.testuser.get('username'))
        self.assertContains(response, self.testuser.get('first_name'))
        self.assertContains(response, self.testuser.get('last_name'))

    def test_user_update(self):
        user_edit = self.load_fixture('user_edit.json')
        user = User.objects.create_user(self.testuser)
        self.client.force_login(user=user)
        response = self.client.post(
            reverse_lazy(
                'update_user',
                kwargs={'pk': user.id}
            ), user_edit
        )
        self.assertRedirects(response, reverse_lazy('users'))
        user = User.objects.get(pk=user.id)
        self.assertEqual(user.first_name, user_edit.get('first_name'))
        self.assertEqual(user.last_name, user_edit.get('last_name'))

    def test_user_delete(self):
        user = User.objects.create_user(self.testuser)
        self.client.force_login(user=user)
        self.client.post(
            reverse_lazy(
                'delete_user',
                kwargs={'pk': user.id}
            )
        )
        self.assertNotIn(user, User.objects.all())
