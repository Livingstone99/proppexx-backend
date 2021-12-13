from django.db import models
from team.serializers import AdminAgentSerializer
from property.serializers import PropertyListSerializer, PropertySerializer, PropertySerializer2
from users.serializers import UserSerializer
from rest_framework.generics import get_object_or_404
from rest_framework import serializers
from .models import Review
from django.utils.translation import ugettext_lazy as _


class PropertyReviewSerializer(serializers.ModelSerializer):
    # property = PropertyListSerializer()
    class Meta:
        model = Review
        fields = ('id', 'user','paid', 'property', 'status', 'created_at',
                  'updated_at', 'assiged_agent', 'refrence_code',)
        read_only_fields = (
            'user', 'status', 'assiged_agent', 'refrence_code',)

    def create(self, validated_data):
        try:
            checker = Review.objects.get(user=self.context['request'].user,property = validated_data['property'] )
            if checker.paid:
                raise serializers.ValidationError(
                    detail = [AssignAgentSerializer(checker).data]
                )
            raise serializers.ValidationError(
                detail=[AssignAgentSerializer(checker).data]
            )
        except Review.DoesNotExist:
            user = Review(user=self.context['request'].user)
            review = Review.objects.create(user=user.user,  **validated_data)
            review.save()
            return review

    #
    # validators = [
    #         serializers.UniqueTogetherValidator(
    #             queryset=Review.objects.all(),
    #             fields=('user', 'property'),
    #             message=_("Some custom message.")
    #         )
    #     ]


class AssignAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user', 'status', 'paid',
                            'property', 'refrence_code',)

class AssignAgentSerializer2(serializers.ModelSerializer):
    user = UserSerializer(required = True)
    property = PropertySerializer(required=True)
    assiged_agent = AdminAgentSerializer(required = True)
    class Meta:
        model = Review
        fields = '__all__'

class ConfirmPropReviewSerializer(serializers.ModelSerializer):
    # property  = PropertyListSerializer() 
    class Meta:
        model = Review
        fields = '__all__'      
        read_only_fields = ('user', 'status','assiged_agent',
                            'property', "paid",)

    # def update(self, instance, validated_data):
    #     instance.refrence_code = validated_data.get(
    #         'refrence_code', '')
    #     instance.paid = True
    #     instance.save()
    #     return instance


class PropertyReviewSerializer2(serializers.ModelSerializer):
    # property = PropertyListSerializer()
    class Meta:
        model = Review
        fields = ('id', 'user', 'paid', 'property', 'status', 'created_at',
                  'updated_at', 'assiged_agent', 'refrence_code',)
        read_only_fields = (
            'user', 'status', 'assiged_agent', 'refrence_code','paid')
