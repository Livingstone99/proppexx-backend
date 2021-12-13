from django.db import models

from users.models import User
# Create your models here.


class Feedback(models.Model):
    user_from = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_from', null=True)
    user_to = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE, related_name='user_to')
    feedback_id = models.CharField(
        max_length=10, unique=True)
    title = models.CharField(max_length=100)
    message = models.TextField(max_length=500)
    has_replied = models.BooleanField(default=False)
    reply = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(
        auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        get_latest_by = ['created_at']
