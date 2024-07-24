from django.test import TestCase
from rest_framework.exceptions import ValidationError
from techNews.models import News, Sources, Tags
from techNews.serializers import SourceSerializer, TagSerializer, NewsSerializer

class SourceSerializerTest(TestCase):

    def setUp(self):
        self.source_attributes = {
            'source_name': 'Test Source',
            'source_url': 'http://testsource.com'
        }
        self.serializer = SourceSerializer(data=self.source_attributes)

    def test_source_serializer_valid(self):
        self.assertTrue(self.serializer.is_valid())

    def test_source_serializer_invalid(self):
        invalid_data = {
            'source_name': '',
            'source_url': 'http://testsource.com'
        }
        serializer = SourceSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

class TagSerializerTest(TestCase):

    def setUp(self):
        self.tag_attributes = {
            'tag_name': 'economy'
        }
        self.serializer = TagSerializer(data=self.tag_attributes)

    def test_tag_serializer_valid(self):
        self.assertTrue(self.serializer.is_valid())

    def test_tag_serializer_invalid(self):
        invalid_data = {
            'tag_name': ''
        }
        serializer = TagSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

class NewsSerializerTest(TestCase):

    def setUp(self):
        self.source = Sources.objects.create(source_name='Test Source', source_url='http://testsource.com')
        self.tag_economy = Tags.objects.create(tag_name='economy')
        self.tag_politics = Tags.objects.create(tag_name='politics')
        self.news_attributes = {
            'heading': 'Test News',
            'news_text': 'Some text',
            'source': {
                'source_name': self.source.source_name,
                'source_url': self.source.source_url
            },
            'tags': [
                {'tag_name': 'economy'},
                {'tag_name': 'politics'}
            ]
        }
        self.serializer = NewsSerializer(data=self.news_attributes)

    def test_news_serializer_valid(self):
        self.assertTrue(self.serializer.is_valid())

    def test_news_serializer_create(self):
        self.serializer.is_valid()
        news = self.serializer.save()
        self.assertEqual(news.heading, self.news_attributes['heading'])
        self.assertEqual(news.news_text, self.news_attributes['news_text'])
        self.assertEqual(news.source.source_name, self.news_attributes['source']['source_name'])
        self.assertEqual(news.tags.count(), 2)

    def test_news_serializer_update(self):
        news = News.objects.create(
            heading='Old News',
            news_text='Old text',
            source=self.source
        )
        news.tags.add(self.tag_economy)

        updated_data = {
            'heading': 'Updated News',
            'news_text': 'Updated text',
            'source': {
                'source_name': 'Updated Source',
                'source_url': 'http://updatedsource.com'
            },
            'tags': [
                {'tag_name': 'economy'},
                {'tag_name': 'politics'}
            ]
        }
        serializer = NewsSerializer(instance=news, data=updated_data)
        serializer.is_valid()
        updated_news = serializer.save()

        self.assertEqual(updated_news.heading, updated_data['heading'])
        self.assertEqual(updated_news.news_text, updated_data['news_text'])
        self.assertEqual(updated_news.source.source_name, updated_data['source']['source_name'])
        self.assertEqual(updated_news.tags.count(), 2)

