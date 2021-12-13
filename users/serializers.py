from propexx.settings.base import PAYSTACK_SECRET_KEY
import requests

from users.utils import generate_otp
from .models import User, Agent
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
# Serializers define the API representation.
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from subscription.models import Customer
from users.tasks import create_customer_on_paystack_and_locally, update_customer_on_paystack_and_locally
from otp.models import OTP

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'phone_number', 'is_active', 'is_staff', 'last_login', 'avatar', 'about', 'user_type', 'is_email_verified'
        )


class BuyerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email', 'first_name', 'last_name', 'phone_number',
            'password', 'user_type', 'about', 'accept_newsletter', 'is_email_verified'
        )
        read_only_fields = ('user_type', 'is_email_verified')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data["phone_number"],
            about=validated_data.get('about', ''),
            accept_newsletter=validated_data["accept_newsletter"],
            user_type='buyer'
        )
        user.set_password(validated_data['password'])
        user.save()
        user_id = user.id
        create_customer_on_paystack_and_locally.delay(user_id)
        return user


class AgentRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email', 'first_name', 'last_name', 'phone_number',
            'password', 'user_type', 'about', 'accept_newsletter', 'is_email_verified'
        )
        read_only_fields = ('is_email_verified',)

        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'user_type': {'required': True},
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data.get("phone_number"),
            about=validated_data["about"],
            accept_newsletter=validated_data["accept_newsletter"],
            user_type=validated_data['user_type'],
        )
        user.set_password(validated_data['password'])
        user.save()
        otp = generate_otp(validated_data.get("phone_number"))
        otp_gen = OTP(user=user,
                      otp = otp )
        otp_gen.save()
        user_id = user.id
        create_customer_on_paystack_and_locally.delay(user_id)
        return user
# class DeveloperRegistrationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = (
#             'email', 'first_name', 'last_name', 'phone_number',
#             'password', 'user_type', 'about', 'accept_newsletter', 'is_email_verified'
#         )
#         read_only_fields = ('user_type', 'is_email_verified')

#         extra_kwargs = {
#             'password': {
#                 'write_only': True,
#                 'required': True},
#             'first_name': {'required': True},
#             'last_name': {'required': True},
#         }

#     def create(self, validated_data):
#         user = User(
#             email=validated_data['email'],
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name'],
#             phone_number=validated_data.get("phone_number"),
#             about=validated_data["about"],
#             accept_newsletter=validated_data["accept_newsletter"],
#             user_type='developer',
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         # user_id = user.id
#         # create_customer_on_paystack_and_locally.delay(user_id)
#         return user


class AdminRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email', 'first_name', 'last_name', 'phone_number',
            'password'
        )

        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data.get("phone_number"),
            is_staff=True,
            is_admin=True,
            is_active=False
        )
        user.set_password(validated_data['password'])
        user.save()
        user_id = user.id
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    user_id = serializers.CharField(read_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        if user and user.is_staff:
            return user
        if user and not user.is_active:
            raise serializers.ValidationError(
                "Your Account is Currently Inactive, please wait for verification")
        raise serializers.ValidationError("Incorrect Credentials")


class AgentLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    user_id = serializers.CharField(read_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active and user.user_type == 'agent':
            return user
        if user and user.is_active and user.user_type == 'developer':
            return user
        if user and user.is_active and user.user_type == 'buyer':
            raise serializers.ValidationError(
                "Your are not an agent!")
        if user and user.is_staff:
            """
            staffs are not supposed to login into agent app
            """
            raise serializers.ValidationError(
                "Your are not supposed to sign in here! ")
        if user and not user.is_active:
            raise serializers.ValidationError(
                "Your Account is Currently Inactive, please wait for verification")
        raise serializers.ValidationError("Incorrect Credentials")


class BuyerLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    user_id = serializers.CharField(read_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active and user.user_type == 'agent':
            raise serializers.ValidationError(
                "Your are not a buyer!")
        if user and user.is_active and user.user_type == 'developer':
            raise serializers.ValidationError(
                "Your are not a buyer!")
        if user and user.is_active and user.user_type == 'buyer':
            return user
        if user and user.is_staff:
            """
            staffs are not supposed to login into agent app
            """
            raise serializers.ValidationError(
                "Your are not supposed to sign in here! ")
        if user and not user.is_active:
            raise serializers.ValidationError(
                "Your Account is Currently Inactive, please wait for verification")
        raise serializers.ValidationError("Incorrect Credentials")


class AdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    user_id = serializers.CharField(read_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active and user.is_admin:
            return user
        if user and user.is_active and user.is_staff:
            return user
        if user and not user.is_active:
            raise serializers.ValidationError(
                "Your Account is Currently Inactive, please wait for verification")
        raise serializers.ValidationError("Incorrect Admin Credentials")


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'about', 'phone_number', 'avatar', 'accept_newsletter')
        extra_kwargs = {
            'about': {'required': False},
        }


class UpdateStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'phone_number', 'avatar')


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


""" To customize the depth of agent relational key field"""


class AllAgentSerializer(serializers.ModelSerializer):
    agents = UserSerializer(required=True)

    class Meta:
        model = Agent
        fields = ['agents', 'verified', 'active', 'rating', ]
        read_only_fields = ('agent', 'rating',)
        depth = 1


class AgentSerializer(serializers.ModelSerializer):
    agents = UserSerializer(required=True)

    class Meta:
        model = Agent
        fields = ['agents', 'verified', 'active', 'rating', ]
        depth = 1
        # read_only_fields = ('id', 'rating',)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        model = User
        fields = ['email']


class SetNewPasswordApiSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=8, max_length=40, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True
    )
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed(
                    'the the reset link is invalid', 401)
            user.set_password(password)
            user.save()

        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)

    