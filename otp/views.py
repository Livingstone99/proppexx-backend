from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from otp.models import OTP
from users.models import User
from users.utils import generate_otp,send_instant_mail, current_site
from users.permissions import IsAgentOrDeveloper
from rest_framework.response import Response
from propexx.settings.base import EMAIL_HOST_USER


# Create your views here.


@api_view(['GET'])
@permission_classes([IsAgentOrDeveloper])
def getOTPview(request, format=None):
    try:
        user_otp = OTP.objects.get(user=request.user)
        otp = generate_otp(request.user.phone_number)
        user_otp.otp = otp
        user_otp.save()
    except OTP.DoesNotExist:
        if request.user.is_email_verified:
            return Response('this user is already verified', status=status.HTTP_208_ALREADY_REPORTED)
        else:
            otp = generate_otp(request.user.phone_number)
            otp_gen = OTP(user=request.user,
                          otp=otp)
            otp_gen.save()
            context = {
                'current_site': f'https://{current_site.domain}',
                'current_user': request.user,
                'username': request.user.first_name,
                'email': request.user.email,
                "otp": otp
            }
            send_instant_mail.delay(
                request.user.email, 'Verify Account with OTP', EMAIL_HOST_USER, 'email/otp.html', context)

            return Response('OTP create and sent', status=status.HTTP_201_CREATED)

    context = {
        'current_site': f'https://{current_site.domain}',
        'current_user': request.user,
        'username': request.user.first_name,
        'email': request.user.email,
        "otp": user_otp.otp
    }
    send_instant_mail.delay(
        request.user.email, 'Verify Account with OTP', EMAIL_HOST_USER, 'email/otp.html', context)

    return Response(f"otp has been sent to {request.user.email}", status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAgentOrDeveloper])
def getOTPview1(request, code_id):
    try:
        user_otp = OTP.objects.get(otp=code_id, user=request.user)
        user_otp.verified = True
        user = User.objects.get(id=request.user.id)
        print('this is the user', user)

        user.is_email_verified = True
        user.save()
        user_otp.delete()
        return Response("user email is successfully verified", status=status.HTTP_202_ACCEPTED)
    except OTP.DoesNotExist:
        return Response("wrong password", status=status.HTTP_403_FORBIDDEN)
