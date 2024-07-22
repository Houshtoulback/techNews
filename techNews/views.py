from django.http import JsonResponse
from .models import Tags, Sources, News
from .serializers import NewsSerializer, TagSerializer, SourceSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST'])
def newsList (request): 
    if request.method == 'GET':
        news = News.objects.all()
        serializer = NewsSerializer(news, many= True)
        return JsonResponse(serializer.data, safe=False)
    
    if request.method == 'POST':
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)