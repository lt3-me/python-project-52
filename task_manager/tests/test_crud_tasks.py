import json
import os

from django.urls import reverse_lazy
from django.test import TestCase

from task_manager.users.models import User
from task_manager.tasks.models import Task

FIXTURES_DIR_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'fixtures'
)
TASK = json.load(open(os.path.join(
    FIXTURES_DIR_PATH, 'task.json')))
TASK_EDIT = json.load(open(os.path.join(
    FIXTURES_DIR_PATH, 'task_edit.json')))


class CRUDTest(TestCase):
    fixtures = ['task_manager/tests/fixtures/db_tasks.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.task = Task.objects.get(pk=1)
        self.client.force_login(user=self.user)

    def test_task_create(self):
        response = self.client.get(reverse_lazy('create_task'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse_lazy('create_task'),
            TASK
        )
        self.assertRedirects(response, reverse_lazy('tasks'))
        last_created = Task.objects.latest('created_at')
        self.assertEqual(last_created.name, TASK.get('name'))
        self.assertEqual(last_created.creator.id, self.user.id)
        self.assertEqual(last_created.executor.id, TASK.get('executor'))
        self.assertEqual(last_created.status.id, TASK.get('status'))
        label_ids = list(map(lambda x: x.id, last_created.labels.all()))
        self.assertEqual(label_ids, TASK.get('labels'))

    def test_task_read(self):
        response = self.client.get(reverse_lazy('tasks'))
        self.assertEqual(response.status_code, 200)
        task_detail_url = reverse_lazy(
            "task_detail",
            kwargs={"pk": self.task.id})
        self.assertContains(response, f'\
<a href="{task_detail_url}">{self.task.name}</a>')
        response = self.client.get(task_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)
        self.assertContains(response, self.task.description)
        self.assertContains(response, self.task.status.name)
        self.assertContains(response, self.task.creator.get_full_name())
        self.assertContains(response, self.task.executor.get_full_name())
        labels = self.task.labels.all()
        for label in labels:
            self.assertContains(response, label.name)

    def test_task_update(self):
        response = self.client.post(
            reverse_lazy(
                'update_task',
                kwargs={'pk': self.task.id}
            ), TASK_EDIT, follow=True
        )
        self.assertRedirects(response, reverse_lazy('tasks'))
        updated_task = Task.objects.get(pk=self.task.id)
        self.assertEqual(updated_task.name, TASK_EDIT.get('name'))
        self.assertEqual(updated_task.executor.id, TASK_EDIT.get('executor'))
        self.assertEqual(updated_task.status.id, TASK_EDIT.get('status'))
        label_ids = list(map(lambda x: x.id, updated_task.labels.all()))
        self.assertEqual(label_ids, TASK_EDIT.get('labels'))

    def test_task_delete(self):
        response = self.client.post(
            reverse_lazy(
                'delete_task',
                kwargs={'pk': self.task.id}
            )
        )
        self.assertRedirects(response, reverse_lazy('tasks'))
        self.assertNotIn(self.task, Task.objects.all())
