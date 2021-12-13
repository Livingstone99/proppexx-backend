from django.urls import path
from . import views


urlpatterns = [
    path('send-otp', views.getOTPview),
    path('verify-otp/<str:code_id>', views.getOTPview1),

]
