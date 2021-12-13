import re
from users.permissions import IsAgentOrDeveloper, IsAgentOrDeveloperOrAdmin
import users
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import timezone
from datetime import datetime
from rest_framework.views import APIView
from knox.auth import TokenAuthentication
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.models import Site
from rest_framework.decorators import api_view, permission_classes
from knox.models import AuthToken
from rest_framework import generics, status
from rest_framework.response import Response
from knox.views import LoginView as knox_login_view
from knox.views import LogoutAllView as knox_logout_view
from knox.views import LogoutAllView as knox_logoutall_view
from django.contrib.auth import login, logout
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView, get_object_or_404
from .serializers import (
    AgentLoginSerializer, BuyerLoginSerializer, LoginSerializer, AgentRegistrationSerializer, BuyerRegistrationSerializer, PasswordResetSerializer, SetNewPasswordApiSerializer,
    UserSerializer, UpdateUserSerializer, ChangePasswordSerializer, AgentSerializer,
    AllAgentSerializer)
from .models import User, Agent
from drf_yasg.utils import swagger_auto_schema
# Register API
from django.utils.encoding import DjangoUnicodeDecodeError, force_bytes, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import generate_otp, token_generator
from django.http import HttpResponsePermanentRedirect
from .utils import send_instant_mail, current_site
from propexx.settings.base import EMAIL_HOST_USER
import os
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser
from users.tasks import update_customer_on_paystack_and_locally
from users.serializers import AdminLoginSerializer, AdminRegistrationSerializer, UpdateStaffSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Q
from datetime import timedelta
from django.core.serializers import serialize
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render

class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']






class BuyerRegistrationApi(generics.GenericAPIView):
    """Registers New buyer"""
    serializer_class = BuyerRegistrationSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # handing login immeddiately a user is register
        log_serializer = LoginSerializer(data = request.data)
        log_serializer.is_valid(raise_exception=True)
        user = log_serializer.validated_data 
        login(request, user)
        return Response({
            "user": UserSerializer(user).data,
            "token": AuthToken.objects.create(user)[1]
        })


class AgentRegistrationApi(generics.GenericAPIView):
    """Registers new Agent"""
    serializer_class = AgentRegistrationSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # handing login immeddiately a user is register
        log_serializer = LoginSerializer(data = request.data)
        log_serializer.is_valid(raise_exception=True)
        user = log_serializer.validated_data 
        login(request, user)
        return Response({
            "user": UserSerializer(user).data,
            "token": AuthToken.objects.create(user)[1]
        })

class StaffRegistrationApi(generics.GenericAPIView):
    """Registers new Staff"""
    serializer_class = AdminRegistrationSerializer
    authentication_classes = (TokenAuthentication,)

    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Your account have been successfully created, Contact admin for activation"})


class LoginAPIView(knox_login_view):
    """Logs in already registered user and returns token"""
    serializer_class = LoginSerializer
    authentication_classes = ()
    permission_classes = ()

    @swagger_auto_schema(
        request_body=LoginSerializer,
        operation_description="Logs user in.",
        responses={200: 'login_response'}
    )
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)
        return Response({
            "user": UserSerializer(user).data,
            "token": AuthToken.objects.create(user)[1]
        })
class AgentLoginAPIView(knox_login_view):
    """Logs in already registered user and returns token"""
    serializer_class = AgentLoginSerializer
    authentication_classes = ()
    permission_classes = ()

    @swagger_auto_schema(
        request_body=AgentLoginSerializer,
        operation_description="Logs user in.",
        responses={200: 'login_response'}
    )
    def post(self, request, *args, **kwargs):
        serializer = AgentLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)
        return Response({
            "user": UserSerializer(user).data,
            "token": AuthToken.objects.create(user)[1]
        })
class BuyerLoginAPIView(knox_login_view):
    """Logs in already registered user and returns token"""
    serializer_class = BuyerLoginSerializer
    authentication_classes = ()
    permission_classes = ()

    @swagger_auto_schema(
        request_body=BuyerLoginSerializer,
        operation_description="Logs user in.",
        responses={200: 'login_response'}
    )
    def post(self, request, *args, **kwargs):
        serializer = BuyerLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)
        return Response({
            "user": UserSerializer(user).data,
            "token": AuthToken.objects.create(user)[1]
        })



class AdminLoginAPIView(knox_login_view):
    """Logs in already registered Admin user and returns token"""
    serializer_class = AdminLoginSerializer
    authentication_classes = ()
    permission_classes = ()

    @swagger_auto_schema(
        request_body=AdminLoginSerializer,
        operation_description="Logs user in.",
        responses={200: 'login_response'}
    )
    def post(self, request, *args, **kwargs):
        serializer = AdminLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)
        return Response({
            "user": UserSerializer(user).data,
            "token": AuthToken.objects.create(user)[1]
        })


class UpdateProfileView(APIView):
    "Update User profile"
    # queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    parser_classes = [MultiPartParser, FormParser, ]
    serializer_class = UpdateUserSerializer

    @swagger_auto_schema(
        request_body=UpdateUserSerializer,
        operation_description="Update User profile",
        responses={200: "Done!!"}
    )
    def put(self, request, format=None):
        profile = User.objects.get(id=request.user.id)
        serializer = UpdateUserSerializer(
            profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            update_customer_on_paystack_and_locally.delay(profile.id)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateStaffProfileView(APIView):
    "Update Staff User profile"
    # queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    parser_classes = [MultiPartParser, FormParser, ]
    serializer_class = UpdateStaffSerializer

    @swagger_auto_schema(
        request_body=UpdateStaffSerializer,
        operation_description="Update staff profile",
        responses={200: "Done!!"}
    )
    def put(self, request, format=None):
        profile = User.objects.get(id=request.user.id)
        serializer = UpdateStaffSerializer(
            profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class AgentListView(generics.ListAPIView):
#     "Get list of All Agents"
#     queryset = User.objects.filter(user_type='agent')
#     permission_classes = (IsAdminUser,)
#     serializer_class = UserSerializer


class BuyerListView(generics.ListAPIView):
    "Get list of all buyers"
    queryset = User.objects.filter(user_type='buyer')
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deactivate_account(request):
    "Deactivate user account"
    if request.method == 'POST':
        request.user.is_active = False
        request.user.save()
        return Response({"message": "Acccount Successfully Deactivated!"})
    return Response({"message": "Acccount Successfully Deactivated!"})


@api_view(['POST'])
@permission_classes([IsAdminUser])
def activate_account(request, pk, format=None):
    "Only admin should be able to activate user acccount"
    if request.method == 'POST':
        try:
            user = User.objects.get(id=pk)

            if user.is_active == False:
                user.is_active = True
                user.save()
                # send an e-mail to the user
                context = {
                    'current_site': f'http://{current_site.domain}',
                    'current_user': user,
                    'username': user.first_name,
                    'email': user.email,
                }

                send_instant_mail.delay(user.email, 'Account Activated',
                                        EMAIL_HOST_USER, 'email/activate_user.html', context)
                return Response({"message": "Acccount Successfully Activated!"})
            else:
                return Response({"message": "Acccount has already been Activated!"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        except ObjectDoesNotExist:
            return Response({"message": "User with ID doesnot exist!"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([
    IsAgentOrDeveloper])
def verify_email(request):
    if request.user.is_email_verified:
        return Response('this user is already verified')
    else:
        uidb64 = urlsafe_base64_encode(force_bytes(request.user.id))

        relativeLink = reverse('activate', kwargs={
            'uidb64': uidb64, 'token': token_generator.make_token(request.user)})
        context = {
            'current_site': f'https://{current_site.domain}',
            'current_user': request.user,
            'username': request.user.first_name,
            'email': request.user.email,
            'absurl': relativeLink
        }

        send_instant_mail.delay(
            request.user.email, 'Verify Account', EMAIL_HOST_USER, 'email/verify_email.html', context)
        return Response("success! check your mail")


def responsePageHtml(request):
    return render(request, 'users/response.html')


@api_view(['POST'])
@permission_classes([IsAdminUser])
def deactivate_account(request, pk, format=None):
    "Only admin should be able to Deactivate user acccount"
    if request.method == 'POST':
        user = User.objects.get(id=pk)
        try:
            if user.is_active == True:
                user.is_active = False
                user.save()
                # send an e-mail to the user
                context = {
                    'current_site': f'https://{current_site.domain}',
                    'current_user': user,
                    'username': user.first_name,
                    'email': user.email,
                }

                send_instant_mail.delay(user.email, 'Account Deactivated',
                                        EMAIL_HOST_USER, 'email/deactivate_user.html', context)
                return Response({"message": "Acccount Successfully Deactivated!😞"})
            else:
                return Response({"message": "Acccount has already been DeActivated!"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        except ObjectDoesNotExist:
            return Response({"message": "User with ID doesnot exist!"}, status=status.HTTP_404_NOT_FOUND)


class UserProfileView(generics.ListAPIView):
    "Get profile detail of logged in user"
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(email=self.request.user)


class PasswordTokenCheckApi(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def get(self, request, uidb64, token):
        try:
            id = smart_bytes(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, request for new one'})
            return Response({'success': True, 'message': 'credentials are valid', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, request for new one'})

class ChangePasswordView(generics.UpdateAPIView):
    """
        An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({
                'message': 'Password updated successfully',
            })


class VerificationView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def get(self, request, uidb64, token):
        try:
            uid = force_bytes(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            return Response('user does not exist')

        if user and token_generator.check_token(user, token):
            user.is_email_verified = True
            user.save()
            serializer = UserSerializer(user)

            data = {'user': serializer.data}
            # return Response(data, status=status.HTTP_201_CREATED)
            return render(request,'users/response.html', status=status.HTTP_201_CREATED)
        else:
            # return Response({'user not found'}, status=status.HTTP_400_BAD_REQUEST)
            return render(request,'users/already_verified.html', status=status.HTTP_400_BAD_REQUEST)


class AllAgentsApiViewSet(ListAPIView):
    serializer_class = AllAgentSerializer
    permission_classes = [AllowAny, ]
    queryset = Agent.objects.all()
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    # search_fields = ['user_type', ]
    # queryset = User.objects.filter(Q(user_type='agent') |
    #                                Q(user_type='developer'))
class AllDeveloperApiViewSet(ListAPIView):
    """
    get all developer
    """
    serializer_class = UserSerializer
    permission_classes = [AllowAny,]
    queryset = User.objects.filter(user_type = 'developer')
    

class AllStaffApiViewSet(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny, ]
    queryset = User.objects.filter(is_staff=True)


class GetAgentApiViewSet(RetrieveAPIView):
    permission_classes = [IsAdminUser, ]
    serializer_class = AgentSerializer
    queryset = Agent
    lookup_field = 'agents_id'


class UserAPI(generics.RetrieveAPIView):
    """
    get user by passing token through header
    """
    permission_classes = [AllowAny, ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class SearchAgentApiViewSet(ListAPIView):
    """
    Search for agent and 
    """
    permission_classes = [AllowAny, ]
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ['first_name', 'last_name', ]
    # queryset = User.objects.filter(user_type = 'agent')
    queryset = User.objects.filter(Q(user_type='agent') |
                                   Q(user_type='developer'))


class NewUserPerMonth(RetrieveAPIView):
    """Get count of new users per month of the current user"""
    permission_class = [IsAdminUser, ]

    def get(self, request, **kwargs):
        year = timezone.now().year
        months = 13
        login_analytics_data = []

        for month in range(1, months):
            login_analytics_data.append({
                'count': User.objects.filter(date_joined__year__gte=year, date_joined__month=month,
                                             date_joined__year__lte=year).count(),
                'date': month
            })
        return Response(login_analytics_data, status=status.HTTP_200_OK)



# password reset!!!!

class PasswordResetEmail(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        data = {'request': request, 'data':request.data}
        serializer = self.serializer_class



class RequestPasswordChange(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))

            token = PasswordResetTokenGenerator().make_token(user)

            current_site = get_current_site(request=request).domain
            current_site_frontend = os.getenv('CURRENT_SITE')
            relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'https://' + current_site_frontend + relativeLink
            subject = 'Reset password'
            email = str(email)
            context = {
                    'current_site': absurl,
                    'current_user': user,
                    'username': user.first_name,
                    'email': user.email,
                }
            send_instant_mail.delay(user.email, 'Reset Forgotten password',
                                        EMAIL_HOST_USER, 'email/user_reset_password.html', context)
                
            return Response({'success': 'we have send you a link to reset password'}, status = status.HTTP_200_OK)
        return Response({'error': 'this email does not exist'}, status = status.HTTP_404_NOT_FOUND)


class SetNewPasswordApiView(generics.GenericAPIView):
    serializer_class = SetNewPasswordApiSerializer
    def patch(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)



