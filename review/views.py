from decimal import Context
from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework import authentication
from property_request import serializers
from .models import Review
from rest_framework.response import Response
from team.models import AdminAgent
from users.permissions import IsBuyer
from .serializers import AssignAgentSerializer, AssignAgentSerializer2, ConfirmPropReviewSerializer, PropertyReviewSerializer, PropertyReviewSerializer2
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import get_object_or_404
# Create your views here.


class RequestReviewApiViewSet(CreateAPIView):
    """
    function|   Request for property review
    permission| Buyer user
    """
    serializer_class = PropertyReviewSerializer
    permission_classes = [IsBuyer, ]
    queryset = Review


class RequestListApiViewSet(ListAPIView):
    """
    function|  list of all property review requested by a signed in buyer  
    permission| buyer
    """
    serializer_class = AssignAgentSerializer2
    permission_classes = [IsBuyer, ]
    # authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        qs = Review.objects.filter(user=self.request.user.id)
        return qs


class AllRequestApiViewSet(ListAPIView):
    """
    function|   Get all  request for property review, filter query with 


    permission| AdminUser
    """
    permission_classes = [IsAdminUser, ]
    serializer_class = AssignAgentSerializer2
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ['status']
    queryset = Review.objects.all()


class AssignAgentApiViewSet(GenericAPIView):
    """
    function| assign agent to a buyer review request 
    permission| Admin user
    """
    serializer_class = AssignAgentSerializer
    permission_classes = [IsAdminUser, ]

    def patch(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        data = request.data
        agent = get_object_or_404(AdminAgent, pk=data['assiged_agent'])
        review.assiged_agent = agent
        review.status = 'assigned'
        review.save(update_fields=['assiged_agent', 'status'])
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'update was successfully'}, status=status.HTTP_200_OK)


class ConfirmPropReviewViewSet(GenericAPIView):
    """
    permission only buyer authenticated users
    only a valid ref code is accepted
    """

    serializer_class = ConfirmPropReviewSerializer
    permission_classes = [IsBuyer, ]

    def patch(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        if review.paid:
            return Response("payment already made on this review", status=status.HTTP_406_NOT_ACCEPTABLE)

        else:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.data
            review.paid = True
            review.refrence_code = data['refrence_code']
            review.save(update_fields=['paid', 'refrence_code'])
            return Response('successfully saved', status=status.HTTP_200_OK)


class RetrieveReviewViewSet(RetrieveAPIView):
    """
    get a particular review
    permission only for buyer, to get the details of a review
    """
    serializer_class = ConfirmPropReviewSerializer
    # permission_classes = [IsBuyer,]
    lookup_field = 'id'
    lookup_url_kwarg = "review_id"
    queryset = Review.objects.all()
