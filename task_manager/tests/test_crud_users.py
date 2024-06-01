import json
import os

from django.urls import reverse_lazy
from django.test import TransactionTestCase
from django.utils.translation import override

from task_manager.users.models import User


FIXTURES_DIR_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'fixtures'
)
TESTUSER = json.load(open(os.path.join(FIXTURES_DIR_PATH, 'user.json')))
USER_EDIT = json.load(open(os.path.join(FIXTURES_DIR_PATH, 'user_edit.json')))


class CRUDTest(TransactionTestCase):
    def test_user_create(self):
        response = self.client.get(reverse_lazy('create_user'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse_lazy('create_user'),
            TESTUSER
        )
        self.assertRedirects(response, reverse_lazy('login'))
        user = User.objects.latest('created_at')
        self.assertEqual(user.username, TESTUSER.get('username'))

    def test_user_read(self):
        User.objects.create_user(TESTUSER)
        response = self.client.get(reverse_lazy('users'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, TESTUSER.get('username'))
        self.assertContains(response, TESTUSER.get('first_name'))
        self.assertContains(response, TESTUSER.get('last_name'))

    @override('en')
    def test_user_update(self):
        # Update while not logged in (not allowed)
        user = User.objects.create_user(TESTUSER)
        response = self.client.post(
            reverse_lazy(
                'update_user',
                kwargs={'pk': user.id}
            ), USER_EDIT, follow=True
        )
        self.assertRedirects(response, reverse_lazy('login'))
        self.assertContains(response,
                            'You are not logged in! Please log in.')
        # Logging in
        self.client.force_login(user=user)
        # Update another user (not allowed)
        other_user = User.objects.create_user(username='other', password='123')
        response = self.client.post(
            reverse_lazy(
                'update_user',
                kwargs={'pk': other_user.id}
            ), USER_EDIT, follow=True
        )
        self.assertRedirects(response, reverse_lazy('users'))
        self.assertContains(response,
                            'You have no permission to edit another user.')
        same_other_user = User.objects.get(pk=other_user.id)
        self.assertEqual(other_user, same_other_user)
        # Update while logged in
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

    @override('en')
    def test_user_delete(self):
        # Delete while not logged in (not allowed)
        user = User.objects.create_user(TESTUSER)
        response = self.client.post(
            reverse_lazy(
                'delete_user',
                kwargs={'pk': user.id}
            ), follow=True
        )
        self.assertRedirects(response, reverse_lazy('login'))
        self.assertContains(response,
                            'You are not logged in! Please log in.')
        self.assertIn(user, User.objects.all())
        # Logging in
        self.client.force_login(user=user)
        # Delete another user (not allowed)
        other_user = User.objects.create_user(username='other', password='123')
        response = self.client.post(
            reverse_lazy(
                'delete_user',
                kwargs={'pk': other_user.id}
            ), follow=True
        )
        self.assertRedirects(response, reverse_lazy('users'))
        self.assertContains(response,
                            'You have no permission to delete another user.')
        self.assertIn(other_user, User.objects.all())
        # Delete while logged in
        response = self.client.post(
            reverse_lazy(
                'delete_user',
                kwargs={'pk': user.id}
            )
        )
        self.assertNotIn(user, User.objects.all())
