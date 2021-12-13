from django.shortcuts import get_object_or_404
from documents.models import Documents
from rest_framework import serializers
from .models import Verification
from users.models import User

class VerifyAgentSerializer(serializers.ModelSerializer):
    """ for agent request viewset """
    class Meta:
        model = Verification
        fields = '__all__'
        read_only_fields = ('user', 'status', )

    def create(self, validated_data):
        # try:
        # buyer = Buyer.objects.get(buyers = self.context['request'].user)
        user = Verification(user=self.context['request'].user)
        verify = Verification(
            user=user.user,
            status=validated_data.get('status', 'pending'),
            documents=validated_data['document']
        )
        verify.save()
        return verify


class VerificationByAdminSerializer(serializers.ModelSerializer):
    """ for Admin Endpoints"""
    class Meta:
        model = Verification
        fields = '__all__'
        depth = 1
        read_only_fields = ('id', 'user', 'document',)

class UploadDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verification
        fields = ('id', 'user', 'status', 'document', )
        read_only_fields = ('id', 'user', 'status', )

    def update(self, instance, validated_data):
        verification = get_object_or_404(Verification, user = instance.id)
        verification.status = 'uploaded'
        verification.document = validated_data.get('document', verification.document)
        verification.save()
        return verification
    


# class AcceptOrDeclineUploadSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Verification
#         fields = '__all__'
#         read_only_fields = ('id','document', 'response', )


