from django.shortcuts import render
from .models import AgentRating
from users.permissions import IsBuyer
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    AgentRatingSerializers, AllRatingPerAgentSerializer, AllRatingPerAgentSerializer)
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# Create your views here.


class AgentRatingApiViewSet(CreateAPIView):
    """ Only Buyers Can Add Review For An Agent """
    serializer_class = AgentRatingSerializers
    queryset = AgentRating
    permission_classes = [IsBuyer, IsAuthenticated, ]
    # handler500 = 'rest_framework.exceptions.server_error'


class RatingRetrieveApiViewSet(RetrieveDestroyAPIView):
    """ Retrieve a particular rating """
    permission_classes = [IsAdminUser, ]
    serializer_class = AllRatingPerAgentSerializer
    lookup_field = 'id'
    queryset = AgentRating


class AllRatingApiViewSet(ListAPIView):
    """ Get all the reviews from buyers"""
    permission_classes = [IsAdminUser, ]
    serializer_class = AllRatingPerAgentSerializer
    queryset = AgentRating.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ['rate',]


class AllRatingsPerAgentAPIViewSet(ListAPIView):
    """Get the reviews including commments for any Agent"""
    serializer_class = AllRatingPerAgentSerializer
    permission_classes = [IsAdminUser, ]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ['rate',]
    def get_queryset(self):
        return AgentRating.objects.filter(agent_user=self.kwargs['id'])


 