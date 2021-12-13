from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from .models import Verification
from rest_framework.permissions import IsAdminUser
from users.permissions import IsAgent, IsAgentOrDeveloper
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, UpdateAPIView
from .serializers import UploadDocumentSerializer, VerifyAgentSerializer, VerificationByAdminSerializer
from rest_framework import status
from rest_framework.response import Response

# Create your views here.
class VerificationRequestApiViewSet(CreateAPIView):
    """Only Agent can make request to get  verified"""
    serializer_class = VerifyAgentSerializer
    permission_classes = [IsAgent, ]
    queryset = Verification


class GetAllRequestApiViewSet(ListAPIView):
    """Get all request whatever the status"""
    serializer_class = VerificationByAdminSerializer
    permission_classes = [IsAdminUser, ]
    queryset = Verification.objects.all()


class GetAllPendingRequestApiViewSet(ListAPIView):
    """Get all the pending request request"""
    serializer_class = VerificationByAdminSerializer
    permission_classes = [IsAdminUser, ]
    queryset = Verification.objects.all()


class VerifyingAgentApiViewSet(RetrieveUpdateAPIView):
    """ verify agent get Agent through ID"""
    serializer_class = VerificationByAdminSerializer
    permission_classes = [IsAdminUser, ]
    queryset = Verification
    lookup_field = 'user_id'


class uploadDocumentApiViewSet(UpdateAPIView):
    """ Only Agent and developer can Retrieve and Edit Document"""
    serializer_class = UploadDocumentSerializer
    permission_classes = [IsAgentOrDeveloper, ]
    queryset = Verification

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class AcceptORDeclineUploadViewSet(UpdateAPIView):
    """ Only Admin can Retrieve and Edit Document"""
    serializer_class = UploadDocumentSerializer
    permission_classes = [IsAdminUser, ]
    queryset = Verification

    # def update(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(
    #         request.user, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
   #     return Response(serializer.data, status=status.HTTP_200_OK)

@permission_classes([IsAgent])
@api_view(['GET'])
def get_agent_status(request):
    """
    retrieves agent verification status on request
    """
    if request.method == 'get':
        verification = get_object_or_404(Verification, user = request.user)
        serializer = VerificationByAdminSerializer(verification, many = True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)