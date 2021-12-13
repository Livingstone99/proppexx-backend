from propexx.settings.base import paystack
from rest_framework import serializers
from .models import MembershipPlan, MembershipPlanFeatures, userMembershipFeatures
from .models import MembershipPlan
from rest_framework.views import APIView
from subscription.models import Subscription


class UsermembershipFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = userMembershipFeatures
        fields = ('listing', 'premium_listing',)
        # exclude = ['user',]
class MembershipPlanFeaturesSerializer(serializers.ModelSerializer):

    class Meta:
        model = MembershipPlanFeatures
        fields = '__all__'


class MembershipPlanCreateSerializer(serializers.ModelSerializer):
    membership_features = MembershipPlanFeaturesSerializer(required=True)

    class Meta:
        model = MembershipPlan
        fields = ('name', 'price', 'interval',
                  'membership_features', 'plan_code',)
        readonly = ('id', 'slug')
        extra_kwargs = {"price": {"required": True},
                        "interval": {"required": True},
                        "plan_code": {"required": False, "read_only": True},
                        }

    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of student
        :return: returns a successfully created student record
        """
        plan_data = validated_data.pop('membership_features')
        plan_name = validated_data['name']
        plan_interval = validated_data['interval']
        plan_amount = int(validated_data['price'])

        paystack_response = paystack.plan.create(name=plan_name,
                                                 interval=plan_interval,
                                                 amount=plan_amount*100)
        plan_code = paystack_response['data']['plan_code']
        membership_feature = MembershipPlanFeaturesSerializer.create(
            MembershipPlanFeaturesSerializer(), validated_data=plan_data)
        plan, created = MembershipPlan.objects.update_or_create(name=validated_data.pop('name'),
                                                                price=validated_data.pop(
            'price'),
            plan_code=plan_code,
            interval=validated_data.pop(
            'interval'),
            membership_features=membership_feature)
        return plan


class MembershipPlanListSerializer(serializers.ModelSerializer):
    membership_features = MembershipPlanFeaturesSerializer(required=True)

    class Meta:
        model = MembershipPlan
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('subscription_code',
                  'email_token', 'status','subscription_plan', 'active')
        read_only_fields = (
            'status', 'active')
        extra_kwargs = {
            'subscription_code': {'required': False},
            'email_token': {'required': False},
        }
        depth = 1

    def create(self, validated_data):
        return Subscription.objects.create(**validated_data)
