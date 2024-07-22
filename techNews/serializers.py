from rest_framework import serializers
from .models import News, Sources, Tags

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sources
        fields = ['id','source_name', 'source_url']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['id','tag_name']

class NewsSerializer(serializers.ModelSerializer):
    source = SourceSerializer()
    tags = TagSerializer(many=True)
    class Meta:
        model = News
        fields = ['id', 'heading', 'news_text', 'source', 'tags']

    def create(self, validated_data):
        source_data = validated_data.pop('source')
        tags_data = validated_data.pop('tags')

        source, created = Sources.objects.get_or_create(
            source_name=source_data['source_name'],
            defaults={'source_url': source_data.get('source_url', '')}
        )

        news = News.objects.create(source=source, **validated_data)

        for tag_data in tags_data:
            tag, created = Tags.objects.get_or_create(tag_name=tag_data['tag_name'])
            news.tags.add(tag)

        return news
    
    def update(self, instance, validated_data):
        source_data = validated_data.pop('source')
        tags_data = validated_data.pop('tags')

        source, created = Sources.objects.get_or_create(
            source_name=source_data['source_name'],
            defaults={'source_url': source_data.get('source_url', '')}
        )
        instance.source = source

        instance.heading = validated_data.get('heading', instance.heading)
        instance.news_text = validated_data.get('news_text', instance.news_text)
        instance.save()

        instance.tags.clear()
        for tag_data in tags_data:
            tag, created = Tags.objects.get_or_create(tag_name=tag_data['tag_name'])
            instance.tags.add(tag)

        return instance