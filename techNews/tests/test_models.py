from django.test import TestCase
from techNews.models import Sources, Tags, News 

class SourcesModelTest(TestCase):

    def setUp(self):
        self.source = Sources.objects.create(source_name="Test Source", source_url="http://testsource.com")

    def test_source_creation(self):
        self.assertEqual(self.source.source_name, "Test Source")
        self.assertEqual(self.source.source_url, "http://testsource.com")

    def test_source_string_representation(self):
        self.assertEqual(str(self.source), "Test Source")


class TagsModelTest(TestCase):

    def setUp(self):
        self.tag = Tags.objects.create(tag_name="economy")

    def test_tag_creation(self):
        self.assertEqual(self.tag.tag_name, "economy")

    def test_tag_string_representation(self):
        self.assertEqual(str(self.tag), "economy")


class NewsModelTest(TestCase):

    def setUp(self):
        self.source = Sources.objects.create(source_name="Test Source", source_url="http://testsource.com")
        self.tag_economy = Tags.objects.create(tag_name="economy")
        self.tag_politics = Tags.objects.create(tag_name="politics")
        self.news = News.objects.create(
            heading="Test News",
            news_text="Some text",
            source=self.source
        )
        self.news.tags.add(self.tag_economy, self.tag_politics)

    def test_news_creation(self):
        self.assertEqual(self.news.heading, "Test News")
        self.assertEqual(self.news.news_text, "Some text")
        self.assertEqual(self.news.source, self.source)

    def test_news_tags(self):
        self.assertIn(self.tag_economy, self.news.tags.all())
        self.assertIn(self.tag_politics, self.news.tags.all())

    def test_news_string_representation(self):
        self.assertEqual(str(self.news), "Test News")
