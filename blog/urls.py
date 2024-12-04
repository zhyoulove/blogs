from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('index' , views.index, name='index'),
    path('blog_detail/<blog_id>' ,views.blog_detail, name='detail'),
    path('blog_pub' , views.blog_pub, name='blog_pub'),
]
