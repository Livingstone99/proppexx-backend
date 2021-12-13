from django.shortcuts import render
from knox.auth import TokenAuthentication
from .serializers import PropertyRequestSerializer, PropertyRequestListSerializer
from rest_framework.generics import CreateAPIView, ListAPIView
from .models import PropertyRequest
from rest_framework import status, viewsets

# Create your views here.


class PropertyRequestList(ListAPIView):
    """ List properties owned by an Agent query by id. Allow Any Permission"""
    serializer_class = PropertyRequestListSerializer
    permission_classes = []
    queryset = PropertyRequest.objects.all()


class CreatePropertyRequestApiViewSet(CreateAPIView):
    """Add request for property request"""
    permission_classes = []
    authentication_classes = (TokenAuthentication,)
    serializer_class = PropertyRequestSerializer


class PropertyRequestDetailView(viewsets.ModelViewSet):
    """
   Get detail of property request.
    """
    lookup_field = 'id'
    authentication_classes = (TokenAuthentication,)
    serializer_class = PropertyRequestListSerializer
    queryset = PropertyRequest.objects.all()

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.views = obj.views + 1
        obj.save(update_fields=("views", ))
        return super().retrieve(request, *args, **kwargs)
