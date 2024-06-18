import json
import os
from django.urls import reverse_lazy
from django.test import TestCase
from django.utils.translation import override

FIXTURES_DIR_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'fixtures'
)
URL_NAMES = json.load(open(os.path.join(FIXTURES_DIR_PATH, '\
check_access_url_names.json')))
URL_NAMES_PK = json.load(open(os.path.join(FIXTURES_DIR_PATH, '\
check_access_pk_url_names.json')))


class AccessTest(TestCase):
    @override('en')
    def test_access_not_logged_in(self):
        for url_name in URL_NAMES:
            response = self.client.get(reverse_lazy(url_name), follow=True)
            self.assertRedirects(response, reverse_lazy('login'))
            self.assertContains(response,
                                'You are not logged in! Please log in.')

    @override('en')
    def test_urls_with_id_access_while_not_logged_in(self):
        for url_name in URL_NAMES_PK:
            response = self.client.post(
                reverse_lazy(
                    url_name,
                    kwargs={'pk': 1}
                ), follow=True
            )
            self.assertRedirects(response, reverse_lazy('login'))
            self.assertContains(response,
                                'You are not logged in! Please log in.')
