from django.shortcuts import render
from .models import Article
from rest_framework import filters
from rest_framework.permissions import IsAdminUser, AllowAny
from .serializers import ArticleSerializer, CreateArticleSerializer
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.


class ArticleCreateApiViewSet(CreateAPIView):
    """Only Admin Users create articles """
    permission_classes = [IsAdminUser,]
    queryset = Article
    serializer_class =  CreateArticleSerializer

class ArticleRetrieveApiViewSet(RetrieveUpdateDestroyAPIView):
    """ Retrieve, update and destroy article select by article id"""
    permission_classes = [IsAdminUser, ]
    serializer_class = CreateArticleSerializer
    queryset = Article
    lookup_field = 'id'

class ArticleReadApiViewSet(RetrieveAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [AllowAny,]
    queryset = Article
    lookup_field = 'slug'

class ArticleRetrieveByUserIdViewSet(ListAPIView):
    """Get all the artiles written by the specified admin id""" 
    serializer_class = ArticleSerializer
    permission_classes = [AllowAny,]
    def get(self, request,id, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    def get_queryset(self):
        qs = Article.objects.filter(writer_id =self.kwargs['id'])
        return qs
    
class ArticleTagViewset(ListAPIView):
    """ Qeury articles by their the tags"""
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ['tag',]

class AllArticlesApiViewSet(ListAPIView):
    """Get all articles"""
    permission_classes = [AllowAny, ]
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    # def get_queryset(self):
    #     return Article.objects.all()