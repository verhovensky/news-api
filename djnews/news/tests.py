from django.test import TestCase
from django.core.management import call_command


class ListPostTests(TestCase):

    # fixture here

    @classmethod
    def setUpTestData(cls):
        cls.user = 1
        # cls.client.login()

    def test_get_all_news(self):
        pass

    def test_get_specific_date_news(self):
        pass

    def test_get_specific_tag_news(self):
        pass

    def test_get_date_and_tag_specific_news(self):
        pass
