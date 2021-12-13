from django.urls import path
from . import views 

urlpatterns = [
    path('add-bookmark', views.AddBookmarkViewSet.as_view(), name = 'add_bookmark'),
    path('bookmarks/<int:buyer_id>', views.BookmarkListViewSet.as_view(), name = 'buyer_bookmark'),
    path('delete/<int:property_id>', views.DeleteBoookmarkApiviewSet.as_view(), name = 'delete_bookmark'),

]
