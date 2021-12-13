from django.db import models

from users.models import User

# Create your models here.


class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=5)
    verified = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
