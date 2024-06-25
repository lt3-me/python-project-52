from django.urls import reverse_lazy
from django.test import override_settings
from task_manager.tests.base import BaseTestCase


@override_settings(LANGUAGE_CODE='en')
class AccessTest(BaseTestCase):
    def test_access_not_logged_in(self):
        url_names = self.load_fixture('check_access_url_names.json')
        for url_name in url_names:
            response = self.client.get(reverse_lazy(url_name), follow=True)
            self.assertRedirects(response, reverse_lazy('login'))
            self.assertContains(response,
                                'You are not logged in! Please log in.')

    def test_urls_with_id_access_while_not_logged_in(self):
        url_names_pk = self.load_fixture('check_access_pk_url_names.json')
        for url_name in url_names_pk:
            response = self.client.post(
                reverse_lazy(
                    url_name,
                    kwargs={'pk': 1}
                ), follow=True
            )
            self.assertRedirects(response, reverse_lazy('login'))
            self.assertContains(response,
                                'You are not logged in! Please log in.')
