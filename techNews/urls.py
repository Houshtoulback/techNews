from django.contrib import admin
from django.urls import path
from techNews import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', views.newsList, name='newsList'),
    path('news/<int:id>', views.specificNews, name='specificNews')
]
