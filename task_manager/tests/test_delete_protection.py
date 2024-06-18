import json
import os

from django.urls import reverse_lazy
from django.test import TestCase
from django.utils.translation import override

from task_manager.users.models import User
from task_manager.tasks.models import Task


FIXTURES_DIR_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'fixtures'
)
TESTUSER = json.load(open(os.path.join(FIXTURES_DIR_PATH, 'user.json')))


class UserActiveTaskTest(TestCase):
    def test_delete_task_creator(self):
        pass

    def test_delete_task_executor(self):
        pass

    def test_delete_status_related_to_task(self):
        pass

    def test_delete_label_related_to_task(self):
        pass
