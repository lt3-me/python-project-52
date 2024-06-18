import json
import os

from django.urls import reverse_lazy
from django.test import TestCase

from task_manager.users.models import User
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.labels.models import Label

FIXTURES_DIR_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'fixtures'
)
TESTUSER = json.load(open(os.path.join(
    FIXTURES_DIR_PATH, 'user.json')))
TASK = json.load(open(os.path.join(
    FIXTURES_DIR_PATH, 'task.json')))
TASK_EDIT = json.load(open(os.path.join(
    FIXTURES_DIR_PATH, 'task_edit.json')))


def create_task_object(task_kwargs, creator):
    kwargs = task_kwargs.copy()
    kwargs['status'] = Status.objects.get(pk=task_kwargs['status'])
    kwargs['creator'] = creator
    kwargs['executor'] = User.objects.get(pk=task_kwargs['executor'])
    labels = list(map(
        lambda x: Label.objects.get(pk=x), task_kwargs['labels']))
    kwargs.pop('labels')
    task = Task.objects.create(**kwargs)
    task.labels.set(labels)
    return task


class CRUDTest(TestCase):
    fixtures = ['task_manager/tests/fixtures/db.json']

    def setUp(self):
        self.user = User.objects.create_user(TESTUSER)
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
        task = create_task_object(TASK, self.user)
        response = self.client.get(reverse_lazy('tasks'))
        self.assertEqual(response.status_code, 200)
        task_detail_url = reverse_lazy("task_detail", kwargs={"pk": task.id})
        self.assertContains(response, f'\
<a href="{task_detail_url}">{TASK.get("name")}</a>')
        response = self.client.get(task_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, TASK.get('name'))
        self.assertContains(response, TASK.get('description'))
        status = Status.objects.get(pk=TASK.get('status'))
        self.assertContains(response, status.name)
        self.assertContains(response, self.user.get_full_name())
        executor = User.objects.get(pk=TASK.get('executor'))
        self.assertContains(response, executor.get_full_name())
        labels = list(map(
            lambda x: Label.objects.get(pk=x), TASK.get('labels')))
        for label in labels:
            self.assertContains(response, label.name)

    def test_task_update(self):
        task = create_task_object(TASK, self.user)
        response = self.client.post(
            reverse_lazy(
                'update_task',
                kwargs={'pk': task.id}
            ), TASK_EDIT, follow=True
        )
        self.assertRedirects(response, reverse_lazy('tasks'))
        updated_task = Task.objects.get(pk=task.id)
        self.assertEqual(updated_task.name, TASK_EDIT.get('name'))
        self.assertEqual(updated_task.executor.id, TASK_EDIT.get('executor'))
        self.assertEqual(updated_task.status.id, TASK_EDIT.get('status'))
        label_ids = list(map(lambda x: x.id, updated_task.labels.all()))
        self.assertEqual(label_ids, TASK_EDIT.get('labels'))

    def test_task_delete(self):
        task = create_task_object(TASK, self.user)
        response = self.client.post(
            reverse_lazy(
                'delete_task',
                kwargs={'pk': task.id}
            )
        )
        self.assertRedirects(response, reverse_lazy('tasks'))
        self.assertNotIn(task, Task.objects.all())
