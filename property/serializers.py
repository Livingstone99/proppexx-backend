from copy import error
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from team.models import Team
from django.db.models import fields
from subscription.models import userMembershipFeatures
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from .models import AssignPropertyToDeveloper,DetailPropertyAddress, Draft, Property, PropertyType, Feature, Report
from property.models import PropertyImage
from users.serializers import UserSerializer


class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = '__all__'


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ["image"]


class PropertyListSerializer(serializers.ModelSerializer):
    property_image = PropertyImageSerializer(many=True)
    agent = UserSerializer()

    class Meta:
        model = Property
        fields = '__all__'
        extra_fields = ['property_image']
        extra_kwargs = {
            'longitude': {'required': True},
            'latitude': {'required': True},
        }
        read_only_fields = ('draft', 'agent', 'location', 'status', 'views')
        depth = 1


class FeatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feature
        fields = ["id", "title"]


class PropertySerializer(serializers.ModelSerializer):
    property_image = PropertyImageSerializer(many=True)
    # agent = UserSerializer()
    class Meta:
        model = Property
        fields = '__all__'
        extra_fields = ('property_image',)
        excludes = ('status',)
        extra_kwargs = {
            'longitude': {'required': True},
            'latitude': {'required': True},
        }
        read_only_fields = ('draft', 'agent', 'location', 'views')

    def create(self, validated_data):
        validated_data['available'] = True
        membership_type = userMembershipFeatures.objects.get(
            user=self.context['request'].user)
        if membership_type.listing == 0:
            raise serializers.ValidationError(
                "Your subscription plan, have been exhausted😪")
        if validated_data["features_fix"] == []:
            raise serializers.ValidationError(
                "select at least one feature")
        if len(validated_data["features_fix"]) == 0:
            raise serializers.ValidationError(
                "select at least one feature")
        if membership_type.listing >= 1:
            max_image = 10
            initial = 0
            user = Property(agent=self.context['request'].user)
            # features = validated_data.pop('features')

            property_image_data = validated_data.pop('property_image')
            property = Property.objects.create(
                agent=user.agent, **validated_data)
            # property.features.add(*features)

            for property_image in property_image_data:
                initial += 1
                if initial <= max_image:
                    PropertyImage.objects.create(
                        property=property, **property_image)
                if initial > max_image:
                    raise serializers.ValidationError(
                        f"{initial} images uploaded, Maximum of 10 image")
            membership_type.listing -= 1
            if validated_data['premium']:
                if membership_type.premium_listing >=1:
                    membership_type.premium_listing -= 1
                else:
                    raise serializers.ValidationError(
                        'you dont have premium listing left'
                    )
            membership_type.save()

        return property


class AgentPropertyOnRequestSerializers(serializers.ModelSerializer):
    property_image = PropertyImageSerializer(many=True)

    class Meta:
        model = Property
        exclude = ('draft',  'featured', 'slug', 'active', )
        extra_fields = ('property_image',)
        read_only_fields = ('buyer_user', 'selected')
        # depth = 1


class PropertyAdminUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'
        depth = 1


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = '__all__'
        read_only_fields = ('user',)

    def create(self, validated_data):
        buyer = Report(user=self.context['request'].user)
        report = Report.objects.create(
            user=buyer.user, **validated_data)
        report.save()
        return report

class StatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['status', 'id', 'agent']
        read_only_fields =('id', 'agent',)
        depth = 1


class NearestPropertySerializer(serializers.Serializer):
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()


class AssignPropertyToMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignPropertyToDeveloper
        fields = '__all__'

    def create(self, validated_data):
        team = Team(user=self.context['request'].user)
        member_instance = AssignPropertyToDeveloper.objects.create(
            developer=team.user, **validated_data)
        member_instance.save()
        return member_instance


class CreateDraftSerializer(serializers.ModelSerializer):
    class Meta:

        model = Draft
        fields = '__all__'
        read_only_fields = ('user',)
    def create(self, validated_data):
        draft = Draft.objects.filter(
            user = self.context['request'].user).count()
        if draft == 5:
            raise serializers.ValidationError(
                    'you can only have have 5 draft maximum'
            )
        instance = Draft.objects.create(user = self.context['request'].user,
         **validated_data)
        return instance
class DraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Draft
        fields = '__all__'
        read_only_fields = ('user',) 
    # def update(self, instance, validated_data):
    #     draft = get_object_or_404(Draft, user = instance)
    #     draft.draft_box = validated_data.get('draft_box', Draft.draft_box)
    #     draft.save()
    #     return 

class PropertySerializer2(serializers.ModelSerializer):
    """
    this is for a friendlier nested results, displaying neccessary deetails
     """
    class Meta:
        model = Property
        fields = ('id', 'title', 'purpose', 'price', 'available',
         'location','country', 'state', 'lGA', 'city', 'address', )

# class NearestPropertySerializer(serializers.ModelSerializer):
class DetailPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailPropertyAddress
        fields = '__all__'

class DetailPropertySerializer1(serializers.ModelSerializer):
    # for get request
    property = PropertySerializer()
    class Meta:
        model = DetailPropertyAddress
        fields = '__all__'

 
