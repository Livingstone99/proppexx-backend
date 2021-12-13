from re import M
import team
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from property.models import AssignPropertyToDeveloper
from users.permissions import IsDeveloper
from django.shortcuts import get_object_or_404, render
from rest_framework import filters, status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import AdminAgent, Member, Team
from .serializers import AdminAgentSerializer, AdminAgentSerializer2, AssignPropertyToMemberSerializer, CreateMemberSerializer, GetAssignedPropertySerializer, GetAssignedPropertySerializer2, TeamMemberSerializer, TeamSerializer, MemberSerializer, TeamSerializer2
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.




class CreateAminAgentViewSet(CreateAPIView):
    """
    Function: Create an Admin Agent 
    Permission: AdminUser 
    """
    permission_classes  = [IsAdminUser,]
    serializer_class = AdminAgentSerializer
    queryset = AdminAgent

class RetrieveAdminAgentViewSet(RetrieveUpdateDestroyAPIView):
    """
    function| retrieve, update or destroy Admin Agent
    permission| Adminuser
    """
    permission_classes = [IsAdminUser,]
    serializer_class = AdminAgentSerializer
    queryset = AdminAgent
    lookup_field = 'id'
    lookup_url_kwarg ='admin_agent_id'
class ListAdminAgentViewSet(ListAPIView):
    """
    function| get all Admin Agent
    permission| Adminuser
    """
    permission_classes = [AllowAny,]
    serializer_class = AdminAgentSerializer2
    queryset = AdminAgent.objects.all()

class AgentSearchApiViewSet(ListAPIView):
    """
    Search Agents by names, Allow all Authenticated users
    """
    permission_classes = [AllowAny,]
    serializer_class = AdminAgentSerializer2
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ['first_name','last_name',]
    queryset = AdminAgent.objects.all()

class MemberRegistrationViewSet(CreateAPIView):
    """
    create member profile
    """
    permission_classes = (IsDeveloper,)
    serializer_class = CreateMemberSerializer
    queryset = Member
class DeveloperMemberList(ListAPIView):
    """
    A developer get all the members registered
    """
    permission_classes = (IsDeveloper,)
    serializer_class = MemberSerializer
    def get_queryset(self):
        developer = get_object_or_404(Team, developer = self.request.user)
        qs = Member.objects.filter(team =developer)
        return qs
    
class MemberListViewSet(ListAPIView):
    """
    get all members in a specific  team
    """
    permission_classes = (AllowAny,)
    serializer_class = MemberSerializer
    def get(self, request,developer_id, *args, **kwargs):
            return self.list(request, *args, **kwargs)
    def get_queryset(self):
        qs = Member.objects.filter(team =self.kwargs['developer_id'])
        return qs
    

class UpdateMemberApiViewSet(RetrieveUpdateDestroyAPIView):
    """
    Developer can Edit,Update, Delete or Read a specific member details
    """
    permission_classes = (IsDeveloper, )
    serializer_class = MemberSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'member_id'
    def get_queryset(self):
        developer = get_object_or_404(Team, developer = self.request.user)
        qs = Member.objects.filter(team = developer)
        return qs

# class AssignMemberToPropertyApiViewSet(CreateAPIView):
#     permission_classes = [IsDeveloper,]
#     serializer_class = AssignPropertyToMemberSerializer
#     queryset = AssignPropertyToDeveloper

class AssignMemberToPropertyApiViewSet(RetrieveUpdateAPIView):
    """
    assign member to a property
    """
    permission_classes = (IsDeveloper,)
    serializer_class = AssignPropertyToMemberSerializer
    queryset = AssignPropertyToDeveloper
    lookup_field = 'property'
    lookup_url_kwarg = 'property_id'

class AgentAssignedPropertyList(ListAPIView):
    
    """
    Get the list of developer properties
    """
    serializer_class = GetAssignedPropertySerializer
    permission_classes = (IsDeveloper, )
    def get_queryset(self):
        qs = AssignPropertyToDeveloper.objects.filter(developer = self.request.user)
        return qs


class AgentAssignedPropertyList2(ListAPIView):
    
    """
    simplified nest to get active and inactive members
    """
    serializer_class = GetAssignedPropertySerializer2
    permission_classes = (IsDeveloper, )
    def get_queryset(self):
        qs = AssignPropertyToDeveloper.objects.filter(developer = self.request.user)
        return qs

class ListDeveloperTeamApiSerializer(ListAPIView):
    """
    get the total list of developer with the members under them
    """
    serializer_class = TeamMemberSerializer
    permission_classes = (AllowAny, )
    queryset = Member.objects.all()


# @permission_classes([IsAdminUser])
@api_view(['GET'])
def developer_and_team_list(request, format=None):
    """
    get the total list of developer with the members under them
    """
    developer = Team.objects.values_list('developer')
    try:
        developer[0]
        data_list = []
        for id in developer:
            members = Member.objects.filter(team__developer = id)
            developer = Team.objects.get(developer = id)
            try:
                members[0]
                member_serializer = TeamMemberSerializer(members, many = True)
                team_serializers =  TeamSerializer2(developer)
                data_list.append([team_serializers.data,member_serializer.data])

            except IndexError:
                pass
        member = Member.objects.all()
        team_serializer = TeamSerializer2(developer, many = True)
        return Response(data_list, status = status.HTTP_200_OK)

    except IndexError:
        return Response({'message':'no team created yet'})
    
@permission_classes([IsDeveloper])
@api_view(['GET'])
def active_and_inactive_member(request, state):
    """
    state = active [to get the list of active members]
    state = inactive [to get the list of inactive members]
    state = all [all members]
    """
    property_list = AssignPropertyToDeveloper.objects.filter(developer = request.user)
    members = property_list.exclude(assigned_team_member__isnull =True).values_list('assigned_team_member', flat = True).distinct()
    if state == 'active':
        all_members = Member.objects.filter(id__in = members)
        member_serializer = MemberSerializer(all_members, many = True)        
        return Response(member_serializer.data, status=status.HTTP_200_OK)
    elif state == 'inactive':
        all_members = Member.objects.filter(team__developer = request.user)
        inactive_members = all_members.exclude(id__in = members)
        member_serializer = MemberSerializer(inactive_members, many = True)     
        return Response(member_serializer.data, status=status.HTTP_200_OK)   
    elif state == 'all':
        all_members = Member.objects.filter(team__developer = request.user)
        member_serializer = MemberSerializer(all_members, many = True)     
        return Response(member_serializer.data, status=status.HTTP_200_OK)   
    

