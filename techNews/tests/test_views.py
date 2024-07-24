from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from techNews.models import News, Sources, Tags

class NewsListViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.source = Sources.objects.create(source_name="Test Source", source_url="http://testsource.com")
        self.tag_economy = Tags.objects.create(tag_name="economy")
        self.tag_politics = Tags.objects.create(tag_name="politics")
        self.news1 = News.objects.create(heading="News 1", news_text="Text for news 1", source=self.source)
        self.news2 = News.objects.create(heading="News 2", news_text="Text for news 2", source=self.source)
        self.news1.tags.add(self.tag_economy)
        self.news2.tags.add(self.tag_politics)

    def test_get_all_news(self):
        response = self.client.get(reverse('newsList'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_get_news_by_tag(self):
        # by one tag
        response = self.client.get(reverse('newsList'), {'tags': 'economy'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['heading'], 'News 1')
        # by nultiple tags
        response = self.client.get(reverse('newsList'), {'tags': ['economy', 'politics']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_post_news(self):
        data = {
            'heading': 'News 3',
            'news_text': 'Text for news 3',
            'source': {
                'source_name': self.source.source_name,
                'source_url': self.source.source_url
            },
            'tags': [{'tag_name': 'economy'}]
        }
        response = self.client.post(reverse('newsList'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(News.objects.count(), 3)
        self.assertEqual(News.objects.last().heading, 'News 3')


class SpecificNewsViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.source = Sources.objects.create(source_name="Test Source", source_url="http://testsource.com")
        self.tag_economy = Tags.objects.create(tag_name="economy")
        self.news = News.objects.create(heading="Test News", news_text="Some text", source=self.source)
        self.news.tags.add(self.tag_economy)
        self.valid_data = {
            'heading': 'Updated News',
            'news_text': 'Updated text',
            'source': {
                'source_name': 'Updated Source',
                'source_url': 'http://updatedsource.com'
            },
            'tags': [{'tag_name': 'economy'}, {'tag_name': 'politics'}]
        }
        self.invalid_data = {
            'heading': '',
            'news_text': '',
            'source': {},
            'tags': []
        }

    def test_get_specific_news(self):
        response = self.client.get(reverse('specificNews', args=[self.news.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['heading'], 'Test News')

    def test_update_specific_news(self):
        response = self.client.put(reverse('specificNews', args=[self.news.id]), self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['heading'], 'Updated News')

    def test_update_specific_news_invalid(self):
        response = self.client.put(reverse('specificNews', args=[self.news.id]), self.invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_specific_news(self):
        response = self.client.delete(reverse('specificNews', args=[self.news.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(News.objects.filter(id=self.news.id).exists())
