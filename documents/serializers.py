from users.models import Agent, User
from django.db.models import fields
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from .models import Documents
from users.serializers import UserSerializer

from documents import models


class UserSerializer2(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'is_staff', 'groups', 'user_permissions', 'accept_newsletter', 'date_joined',
                   'last_login', 'is_active', 'is_admin', 'is_superuser', 'is_email_verified', 'about',)


class AgentSerializer2(serializers.ModelSerializer):
    agents = UserSerializer2(required=True)

    class Meta:
        model = Agent
        fields = '__all__'


class AdminGetDocumentSerializer(serializers.ModelSerializer):
    user = AgentSerializer2(required=True)

    class Meta:
        model = Documents
        fields = '__all__'
        read_only_fields = ('id', 'message', 'status', 'user')
        # depth = 3


class AgentGetDocumentSerializer(serializers.ModelSerializer):
    user = AgentSerializer2(required=True)

    class Meta:
        model = Documents
        fields = '__all__'


class CheckDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Documents
        fields = ('user', 'message', 'status',)
        read_only_fields = ('user',)

    def update(self, instance, validated_data):
        message = validated_data.pop('message')
        status = validated_data.pop('status')
        instance.message = message
        instance.status = status
        instance.save()
        return instance


class EditDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = '__all__'
        read_only_fields = ('id', 'message', 'status', 'user',)
        extra_kwargs = {
            'government_issued_id': {'required': True},
            'utility_bill': {'required': True},
            'cac_document': {'required': True},
        }

    def update(self, instance, validated_data):
        for value in validated_data:
            if validated_data[value] == '':
                raise serializers.ValidationError(f"provide {value}")
        document = get_object_or_404(Documents, user=instance.id)
        if document.status == 'pending' or document.status == 'accepted':
            raise serializers.ValidationError(
                f'cannot upload documents if status is {document.status}')
        document = get_object_or_404(Documents, user=instance.id)
        document.government_issued_id = validated_data.get(
            'government_issued_id', document.government_issued_id)
        document.utility_bill = validated_data.get(
            'utility_bill', document.utility_bill)
        document.cac_document = validated_data.get(
            'cac_document', document.cac_document)
        document.save()
        return document
