from property.models import Property
from users.serializers import UserSerializer
from users.models import User
from django.core.exceptions import ObjectDoesNotExist
import time
import requests
from paystackapi.transaction import Transaction
from users.permissions import IsAgent, IsAgentOrDeveloper
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from propexx.settings.base import paystack, PAYSTACK_SECRET_KEY
from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
# Create your views here.

from .serializers import MembershipPlanCreateSerializer, MembershipPlanListSerializer, UsermembershipFeaturesSerializer
from .models import MembershipPlan
from _decimal import Decimal
from users.utils import random_string_generator
from subscription.serializers import SubscriptionSerializer
from subscription.models import Customer, Subscription, userMembershipFeatures


class MembershipPlanCreateView(APIView):
    """
    create and edit new Membership Plan.
    """
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        request_body=MembershipPlanCreateSerializer,
        operation_description="Saves Membership Plan",
        responses={200: "Done!!"}
    )
    def post(self, request):
        serializer = MembershipPlanCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'message': "Subscription Plan have been successfully created!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MembershipPlanDeleteView(APIView):
    """
    Delete Membership Plan.
    """
    permission_classes = [IsAdminUser]

    def delete(self, request, pk, format=None):
        membership_plan = get_object_or_404(MembershipPlan, pk=pk)
        membership_plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MembershipPlanListView(APIView):
    """
    List all code Membership Plan
    """
    permission_classes = [IsAuthenticated]

    def get(self, format=None):
        membership_plan = MembershipPlan.objects.all()
        serializer = MembershipPlanListSerializer(membership_plan, many=True)
        return Response(serializer.data)


class MembershipPlanDetailView(APIView):
    """
    Member Plan Detail Membership Plan.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        plan = MembershipPlan.objects.get(slug=slug)
        try:
            serializer = MembershipPlanListSerializer(plan)
            return Response(serializer.data)
        except plan.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class InitializeSubscriptionPayment(APIView):
    """
    Initialise paystack Subscription payment, and get authorization url for payment
    """
    permission_classes = [IsAgentOrDeveloper]

    def post(self, request, plan_code, format=None):
        try:

            membership_plan = MembershipPlan.objects.get(plan_code=plan_code)
            url = 'https://api.paystack.co/transaction/initialize'
            payload = {"email": f'{request.user}',
                       "amount": membership_plan.price*100,
                       #    "plan": plan_code
                       # don't include the plan_code in the payload, else the user will be
                       # be automatically subscribed.
                       }
            response = requests.post(url, data=payload,  headers={
                'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}'})
            data = response.json()
            if data['status']:
                return Response(data, status=status.HTTP_200_OK)
            return Response(data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except MembershipPlan.DoesNotExist:
            return Response({"message": "A subscription plan with this plan code doesn't exist!"}, status=status.HTTP_404_NOT_FOUND)


class AuthorizeSubscription(APIView):
    """
    Subscribe after successull Authorization
    """
    permission_classes = [IsAgentOrDeveloper]

    def post(self, request, reference, plan_code, format=None):

        try:
            membership_plan = MembershipPlan.objects.get(plan_code=plan_code)

            try:
                customer = Customer.objects.get(user=request.user)
                # Check if transaction is valid , using the transaction code before subscribing
                url = f'https://api.paystack.co/transaction/verify/{reference}'
                response = requests.get(url, headers={
                    'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}'})
                data = response.json()
                if data['status']:
                    if data['data']['status'] == "success":

                        # If transaction is valid, head on to subscribing to plan
                        subscription_url = 'https://api.paystack.co/subscription'
                        subscription_payload = {
                            "customer": customer.customer_code,
                            "plan": plan_code}
                        print(subscription_payload)
                        subscription_response = requests.post(subscription_url, data=subscription_payload, headers={
                            'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}'})
                        subscription_data = subscription_response.json()
                        if subscription_data['status']:
                            subscription = Subscription(
                                agent=request.user,
                                subscription_plan=membership_plan,
                                subscription_code=subscription_data['data']['subscription_code'],
                                email_token=subscription_data['data']['email_token'],
                                status='active'
                            )
                            subscription.save()

                            print("subscription",
                                  subscription_data)
                            membership_type = userMembershipFeatures.objects.get(
                                user=request.user)
                            membership_type.listing += subscription.subscription_plan.membership_features.listing
                            membership_type.premium_listing += subscription.subscription_plan.membership_features.listing
                            membership_type.save()
                            return Response({'message': "You have successully subscribed!"}, status=status.HTTP_201_CREATED)
                        else:
                            return Response(subscription_data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                return Response({"status": data["data"]["status"], "gateway_response": data["data"]["gateway_response"], "reference": data["data"]["reference"], }, status=status.HTTP_400_BAD_REQUEST)
            except Customer.DoesNotExist:
                return Response({"message": "user customer code does not exist, please reach out to our admin!"}, status=status.HTTP_404_NOT_FOUND)
        except MembershipPlan.DoesNotExist:
            return Response({"message": "A subscription plan with this plan code doesn't exist!"}, status=status.HTTP_404_NOT_FOUND)


class GetCurrentSubscription(APIView):
    """
    Get user's active subscription
    """
    permission_classes = [IsAgentOrDeveloper]
    def get(self, request, format=None):
        subscription = Subscription.objects.filter(
            agent=request.user, active=True).last()
        serializer = SubscriptionSerializer(subscription)
        if subscription:
            url = f'https://api.paystack.co/subscription/{subscription.subscription_code}'
            response = requests.get(url, headers={
                'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}'})
            data = response.json()
            if data['status']:
                # check if subscribe is active, if it's not active then update local DB
                if data['data']['status'] == 'active':
                    subscription_data = serializer.data
                    subscription_plan  =get_object_or_404(Subscription, subscription_code= data['data']['subscription_code'])
                    user_serializer = UserSerializer(request.user)
                    user_plan_features =  get_object_or_404(userMembershipFeatures, user_id = request.user.id)
                    user_listing_features = UsermembershipFeaturesSerializer(user_plan_features)
                    # user_data = get_object_or_404(User, id = request.user.id)
                    property_counter = Property.objects.filter(agent = request.user).count()
                    # print(f"counting {request.user} properties which is {property_counter}")
                    data = {'subscription':subscription_data, 'user': user_serializer.data['email'],'total_published_properties':property_counter, 'listing_features':user_listing_features.data}
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    Subscription.objects.filter(id=subscription.id).update(
                        status=data['data']['status'], active=False)
                    return Response({"message": "you don't have an active subscription!(initial)"}, status=status.HTTP_404_NOT_FOUND)
            return Response({"message": data}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            return Response({"message": "you don't have an active subscription!"}, status=status.HTTP_404_NOT_FOUND)
# class GetCurrentSubscription(APIView):
#     """
#     Get user's active subscription
#     """
#     permission_classes = [IsAgentOrDeveloper]

#     def get(self, request, format=None):
#         user_plan_features = get_object_or_404(
#             userMembershipFeatures, user_id=request.user.id)
#         # serializer = SubscriptionSerializer(subscription)
#         if user_plan_features.listing > 0 or user_plan_features.premium_listing > 0:
#             user_serializer = UserSerializer(request.user)
#             user_listing_features = UsermembershipFeaturesSerializer(
#                 user_plan_features)
#             data = {'user': user_serializer.data['email'],
#                     'listing_features': user_listing_features.data}
#             return Response(data, status=status.HTTP_200_OK)
#         else:
#             return Response({"message": "you don't have an active subscription!"}, status=status.HTTP_404_NOT_FOUND)


class CancelSubscriptionView(APIView):
    """
    Cancel Subscription.
    """
    permission_classes = [IsAgentOrDeveloper]

    def post(self, request):
        subscription = Subscription.objects.filter(
            agent=request.user, active=True).last()
        if subscription:
            url = 'https://api.paystack.co/subscription/disable'
            payload = {"code": subscription.subscription_code,
                       "token": subscription.email_token}
            response = requests.post(url, data=payload,  headers={
                'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}'})
            data = response.json()
            if data['status']:
                Subscription.objects.filter(id=subscription.id).update(
                    status="cancelled", active=False)
                return Response({'message': "Subscription Plan have been successfully Cancelled!"}, status=status.HTTP_201_CREATED)
            return Response(data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            return Response({"message": "you don't have an active subscription!"}, status=status.HTTP_404_NOT_FOUND)


class GetAllSubscription(APIView):
    """
    List of all subscriptions
    """
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        url = f'https://api.paystack.co/subscription'
        response = requests.get(url, headers={
            'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}'})
        data = response.json()
        if data['status']:
            return Response(data, status=status.HTTP_200_OK)
        return Response(data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class GetAllTransactions(APIView):
    """
    List of all Transactions
    """
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        url = f'https://api.paystack.co/transaction'
        response = requests.get(url, headers={
            'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}'})
        data = response.json()
        if data['status']:
            return Response(data, status=status.HTTP_200_OK)
        return Response(data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
