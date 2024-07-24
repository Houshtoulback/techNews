from django.test import SimpleTestCase
from django.urls import reverse, resolve
from techNews import views

class URLTests(SimpleTestCase):

    def test_news_list_url(self):
        url = reverse('newsList')
        self.assertEqual(resolve(url).func, views.newsList)

    def test_specific_news_url(self):
        url = reverse('specificNews', args=[1])  # 1 is a placeholder for the id
        self.assertEqual(resolve(url).func, views.specificNews)
