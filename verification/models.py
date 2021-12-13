from django.db import models
from users.models import User, Agent
from django.contrib.postgres.fields import ArrayField
from users.utils import upload_avatar_path, upload_verification_document_path, validate_document

# Create your models here.


class Verification(models.Model):
    "Verify the authenticity of user"
    Status = (
        ('pending', 'pending'),
        ('uploaded', 'uploaded'),
        ('accepted', 'accepted'),
        ('rejected', 'rejected')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(choices=Status, max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(
        auto_now_add=False, auto_now=True)
    document = models.FileField(upload_to=upload_verification_document_path, validators=[
        validate_document],)
    response = models.TextField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.email

    class Meta:
        get_latest_by = ['created_at']
