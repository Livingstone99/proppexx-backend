from rest_framework import serializers
from .models import PropertyRequest
from users.serializers import UserSerializer


class PropertyRequestListSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = PropertyRequest
        fields = '__all__'
        excludes = ('status', 'views')
        read_only_fields = ('user',)
        depth = 1


class PropertyRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = PropertyRequest
        fields = '__all__'
        read_only_fields = ('user', 'views',)
        extra_kwargs = {
            'state': {'required': True},
            'city': {'required': True},
            'country': {'required': True},
        }

    def create(self, validated_data):
        # user = PropertyRequest(user=self.context['request'].user)
        propertyRequest = PropertyRequest.objects.create(
            user=self.context['request'].user, **validated_data)
        propertyRequest.save()
        return propertyRequest
