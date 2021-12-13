from property.serializers import PropertySerializer2
from users.serializers import UserSerializer
from users.models import User
from rest_framework.fields import ReadOnlyField
from property.models import AssignPropertyToDeveloper
from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import MethodNotAllowed
from .models import AdminAgent, Member, Team

class  AdminAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminAgent
        fields = '__all__'

class  AdminAgentSerializer2(serializers.ModelSerializer):
    class Meta:
        model = AdminAgent
        fields = '__all__'
        depth = 1

class TeamSerializer(serializers.ModelSerializer):
    class  Meta:
        model  = Team
        fields = '__all__'

class TeamSerializer2(serializers.ModelSerializer):
    developer = UserSerializer(required = True)
    class  Meta:
        model  = Team 
        fields = '__all__'
class MemberSerializer(serializers.ModelSerializer):
    class  Meta:
        model  = Member
        fields = '__all__'
        read_only_fields = ('team',)
        # depth = 2
        
class CreateMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        exclude = ('team',)
    def create(self, validated_data):
        team_instance = get_object_or_404(Team, developer = self.context['request'].user)
        member = Member(team = team_instance, **validated_data)
        member.save()
        return member

class AssignPropertyToMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignPropertyToDeveloper
        fields = '__all__'
        read_only_fields = ('developer','property', 'created_at',)

    def update(self, instance, validated_data):
        instance.assigned_team_member = validated_data.get('assigned_team_member', '')
        instance.save()
        return instance
class GetAssignedPropertySerializer(serializers.ModelSerializer):
    property = PropertySerializer2(required = True)
    # developer = UserSerializer(required = True)
    assigned_team_member = MemberSerializer(required = True)

    class Meta:
        model = AssignPropertyToDeveloper
        fields = '__all__'
        # depth = 1
class GetAssignedPropertySerializer2(serializers.ModelSerializer):
    # property = PropertySerializer2(required = True)
    # developer = UserSerializer(required = True)
    assigned_team_member = MemberSerializer(required = True)

    class Meta:
        model = AssignPropertyToDeveloper
        fields = '__all__'

class TeamMemberSerializer(serializers.ModelSerializer):
    # team = TeamSerializer2(required = True)
    class  Meta:
        model  = Member
        fields = '__all__'
        read_only_fields = ('team',)
        depth = 2
