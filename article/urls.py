from django.urls import path
from . import views

urlpatterns = [
    path('create', views.ArticleCreateApiViewSet.as_view(), name = 'create'),
    path('article-id/<int:id>', views.ArticleRetrieveApiViewSet.as_view(), name = 'get_by_id'),
    path('writer-id/<int:id>', views.ArticleRetrieveByUserIdViewSet.as_view(), name = 'get_by_writer_id'),
    path('<str:slug>', views.ArticleReadApiViewSet.as_view(), name ='article'),
    path('tag', views.ArticleTagViewset.as_view(), name = 'tags'),
    path('articlee-list', views.AllArticlesApiViewSet.as_view(), name = 'all'),
]
