from django.urls import reverse_lazy
from django.test import override_settings

from task_manager.tests.base import BaseTestCase
from task_manager.users.models import User


@override_settings(LANGUAGE_CODE='en')
class CRUDTest(BaseTestCase):
    def test_user_create(self):
        testuser = self.load_fixture('user.json')
        response = self.client.get(reverse_lazy('create_user'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse_lazy('create_user'),
            testuser, follow=True
        )
        self.assertRedirects(response, reverse_lazy('login'))
        self.assertContains(
            response, 'You have been signed up successfully.')
        user = User.objects.latest('date_joined')
        self.assertEqual(user.username, testuser.get('username'))

    def test_user_create_same_username(self):
        testuser = self.load_fixture('user.json')
        User.objects.create_user(testuser['username'])
        response = self.client.post(
            reverse_lazy('create_user'),
            testuser, follow=True
        )
        self.assertContains(
            response, 'A user with that username already exists.')

    def test_user_invalid_username(self):
        testuser = self.load_fixture('user_invalid_username.json')
        response = self.client.post(
            reverse_lazy('create_user'),
            testuser, follow=True
        )
        self.assertContains(response, 'Required. 150 characters or fewer. \
Letters, digits and @/./+/-/_ only.')

    def test_user_invalid_password(self):
        testuser = self.load_fixture('user_invalid_password.json')
        response = self.client.post(
            reverse_lazy('create_user'),
            testuser, follow=True
        )
        self.assertContains(response, "This password is too short. \
It must contain at least 3 characters.")

    def test_user_password_does_not_match(self):
        testuser = self.load_fixture('user_wrong_password_confirm.json')
        response = self.client.post(
            reverse_lazy('create_user'),
            testuser, follow=True
        )
        self.assertIn(
            "The two password fields didn’t match.",
            response.content.decode('utf-8'))

    def test_user_read(self):
        user_data = self.load_fixture('user_create.json')
        User.objects.create_user(**user_data)
        response = self.client.get(reverse_lazy('users'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user_data.get('username'))
        self.assertContains(response, user_data.get('first_name'))
        self.assertContains(response, user_data.get('last_name'))

    def test_user_update(self):
        user_edit = self.load_fixture('user_edit.json')
        user = User.objects.create_user('testuser')
        self.client.force_login(user=user)
        response = self.client.post(
            reverse_lazy(
                'update_user',
                kwargs={'pk': user.id}
            ), user_edit, follow=True
        )
        self.assertRedirects(response, reverse_lazy('users'))
        self.assertContains(
            response, 'User has been successfully updated.')
        user = User.objects.get(pk=user.id)
        self.assertEqual(user.first_name, user_edit.get('first_name'))
        self.assertEqual(user.last_name, user_edit.get('last_name'))

    def test_user_update_username_exists(self):
        user_edit = self.load_fixture('user_edit.json')
        user = User.objects.create_user('testuser')
        User.objects.create_user(user_edit['username'])
        self.client.force_login(user=user)
        response = self.client.post(
            reverse_lazy(
                'update_user',
                kwargs={'pk': user.id}
            ), user_edit, follow=True
        )
        self.assertContains(
            response, "A user with that username already exists.")

    def test_user_update_with_null(self):
        user_edit = self.load_fixture('user_null_values.json')
        user = User.objects.create_user('testuser')
        self.client.force_login(user=user)
        response = self.client.post(
            reverse_lazy(
                'update_user',
                kwargs={'pk': user.id}
            ), user_edit, follow=True
        )
        self.assertContains(
            response,
            "This field is required.",
            count=3)

    def test_user_delete(self):
        user = User.objects.create_user('testuser')
        self.client.force_login(user=user)
        response = self.client.post(
            reverse_lazy(
                'delete_user',
                kwargs={'pk': user.id}
            ), follow=True
        )
        self.assertRedirects(response, reverse_lazy('users'))
        self.assertContains(
            response, "User has been successfully deleted")
        self.assertNotIn(user, User.objects.all())
