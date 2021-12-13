from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .models import Documents
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from users.permissions import IsAgent, IsAgentOrDeveloper
from .models import Documents
from .serializers import AdminGetDocumentSerializer, AgentGetDocumentSerializer, EditDocumentSerializer, CheckDocumentSerializer
# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from users.models import Agent


class UpdateDocumentApiViewSet(UpdateAPIView):
    """ Only Agent can Retrieve and Edit Document"""
    serializer_class = EditDocumentSerializer
    permission_classes = [IsAgentOrDeveloper, ]
    queryset = Documents

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def get_queryset(self):
    #     qs = Documents.objects.filter(user = self.request.user.id)
    #     return qs


class AllAgentsDocumentApiViewSet(ListAPIView):
    """ Only Admin can perform this action"""
    serializer_class = AdminGetDocumentSerializer
    permission_classes = [IsAdminUser, ]
    queryset = Documents.objects.exclude(status='created')


class CheckDocumentApiViewSet(RetrieveUpdateAPIView):
    """ Only Admin can perform this action"""
    serializer_class = CheckDocumentSerializer
    permission_classes = [IsAdminUser, ]
    queryset = Documents
    lookup_field = 'user'
    lookup_url_kwarg = 'agent_id'



class AgentRetrieveDocumentApiViewSet(ListAPIView):
    permission_classes = [IsAgentOrDeveloper, ]
    serializer_class = AgentGetDocumentSerializer

    def get_queryset(self):
        qs = Documents.objects.filter(user=self.request.user.id)
        return qs


@api_view(['GET'])
@permission_classes([IsAgentOrDeveloper])
def activation_status_check(request):
    "Get agent activation status"
    if request.method == 'GET':
        agent_qs = Agent.objects.get(agents_id=request.user.id)
        qs = Documents.objects.get(user=agent_qs)
        return Response({"status": qs.status})
