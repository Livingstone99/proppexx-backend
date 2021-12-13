from rest_framework import serializers
from .models import AgentRating
from users.models import Agent, Buyer, User
from users.serializers import UserSerializer


class AgentRatingSerializers(serializers.ModelSerializer):
    buyer_user = serializers.StringRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    agent_user = UserSerializer
    class Meta:
        model = AgentRating
        fields = '__all__'
        read_only_fields = ('buyer_user','selected', 'eligibilty' )
        # depth = 1
        

    def create(self, validated_data):
        # try:
        # buyer = Buyer.objects.get(buyers = self.context['request'].user)
        user = AgentRating(buyer_user=self.context['request'].user)
        rating = AgentRating(
        buyer_user = user.buyer_user,
        agent_user = validated_data['agent_user'],
        rate = validated_data['rate'],
        comment = validated_data['comment']
    )
        
        rating.save()
        return rating
    def update(self, instance, validated_data):
        print(dir(instance))
        return super().update(instance, validated_data)

    # except Buyer.DoesNotExist:
    #         raise('you are not authorized')
        
class AllRatingPerAgentSerializer(serializers.ModelSerializer):
    agent_user = UserSerializer(required= True)
    class Meta:

        model = AgentRating
        fields = '__all__'
        depth = 1

class AllRatingsPerAgentSerializer(serializers.ModelSerializer):
    agent = UserSerializer(required= True)
    class Meta:
        model = Agent
        # fields = ['agents', 'verified', 'rating', 'active', 'rating', 'total_reviewer']
        fields = '__all__'
        depth = 1

