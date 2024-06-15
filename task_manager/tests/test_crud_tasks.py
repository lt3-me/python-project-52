import json
import os

from django.urls import reverse_lazy
from django.test import TestCase
from django.utils.translation import override

from task_manager.users.models import User
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

FIXTURES_DIR_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'fixtures'
)
TESTUSER = json.load(open(os.path.join(FIXTURES_DIR_PATH, 'user.json')))
USER_EDIT = json.load(open(os.path.join(FIXTURES_DIR_PATH, 'user_edit.json')))


class CRUDTest(TestCase):
    def test_user_create(self):
        pass

    def test_user_read(self):
        pass

    @override('en')
    def test_user_update(self):
        pass

    @override('en')
    def test_user_delete(self):
        pass
