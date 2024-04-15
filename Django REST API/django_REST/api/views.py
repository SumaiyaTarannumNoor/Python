from django.shortcuts import render
from rest_framework import generics
from.models import BlogPost
from .serializers import BlogPostSerializers

class BlogPostListCreate(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializers
