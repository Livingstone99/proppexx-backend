from .serializers import BookmarkSerializer, DeleteBookmarkSerializer, GetBookmarkSerializer
from .models import BookmarkProperty
from users.permissions import IsBuyer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, RetrieveAPIView, DestroyAPIView,ListAPIView 
# Create your views here.


class AddBookmarkViewSet(CreateAPIView):
    """ Buyers can bookmark property"""
    serializer_class = BookmarkSerializer
    permission_classes = [IsBuyer,]
    queryset = BookmarkProperty

class BookmarkListViewSet(ListAPIView, RetrieveAPIView):
    """Retrieving  All the bookmarks made throgh a buyers id"""
    serializer_class = GetBookmarkSerializer
    permission_classes = [IsBuyer,]
    lookup_field = 'buyer'
    lookup_url_kwarg = 'buyer_id'

    def get_queryset(self):
        qs = BookmarkProperty.objects.filter(buyer = self.kwargs['buyer_id'])
        return qs

class  DeleteBoookmarkApiviewSet(DestroyAPIView):
    serializer_class = DeleteBookmarkSerializer
    permission_classes = [IsBuyer,]
    # queryset = BookmarkProperty
    lookup_field = 'property'
    lookup_url_kwarg = 'property_id'

    def get_queryset(self):
        qs = BookmarkProperty.objects.filter(buyer=self.request.user.id)
        return qs
