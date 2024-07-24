from django.http import JsonResponse
from .models import News
from .serializers import NewsSerializer, TagSerializer, SourceSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST'])
def newsList (request): 
    if request.method == 'GET':
        tag_names = request.GET.getlist('tags')
        
        if tag_names:
            news = News.objects.filter(tags__tag_name__in=tag_names).distinct()
        else:
            news = News.objects.all()
            
        serializer = NewsSerializer(news, many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method == 'POST':
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def specificNews (request, id):
    try:
        news = News.objects.get(pk=id)
    except News.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = NewsSerializer(news)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = NewsSerializer(news, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
