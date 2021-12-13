from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView, RetrieveUpdateAPIView, ListAPIView
from django.contrib.sites.models import Site

from users.models import User
from users.utils import send_instant_mail, current_site
from propexx.settings.base import EMAIL_HOST_USER
from .models import Feedback
from .serializers import CreateFeedbackSerializer, AdminReplySerializer, ListFeedbackSerializer
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status


class CreateFeedbackViewset(CreateAPIView):
    "User create feedback"
    serializer_class = CreateFeedbackSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = Feedback.objects.all()


class ListUserFeedbackViewset(ListAPIView):
    "List all feedbacks"
    serializer_class = ListFeedbackSerializer
    permission_classes = [IsAdminUser, ]
    queryset = Feedback.objects.all()
    paginate_by = 0


class AdminReplyViewset(RetrieveUpdateAPIView):
    serializer_class = AdminReplySerializer
    permission_classes = [IsAdminUser, ]
    lookup_field = 'id'


@swagger_auto_schema(method='put',  request_body=AdminReplySerializer)
@api_view(['GET', 'PUT'])
@permission_classes([IsAdminUser])
def Admin_reply_to_feedback_view(request, pk):

    try:
        feedback = Feedback.objects.get(id=pk)
    except Feedback.DoesNotExist:
        return Response({"message": "Feedback Id does not exist!"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        "Get Deatiail of admin request"
        serializer = ListFeedbackSerializer(feedback)
        return Response(serializer.data)

    if request.method == 'PUT':
        """
            Admin replies to feedback though the feedback ID
            params:
            {
                "reply": ""
            }
        """
        data = request.data.get(
            'message')
        serializer = AdminReplySerializer(feedback, data=request.data)

        if serializer.is_valid():
            if feedback.has_replied == False:
                serializer.save(user_to=request.user, has_replied=True)
                # send an e-mail to the user
                context = {
                    'current_site': f'https://{current_site.domain}',
                    'username': feedback.user_from.first_name,
                    'title': feedback.title,
                    'email': feedback.user_from.email,
                    'reply': feedback.reply,
                }

                send_instant_mail.delay(feedback.user_from.email,
                                        f'Feedback Reply: {feedback.title}.',
                                        EMAIL_HOST_USER, 'email/feedback_response.html', context)
                return Response({"message": "Your reply have been sent!"})
            else:
                return Response({"message": "Already replied user!"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
