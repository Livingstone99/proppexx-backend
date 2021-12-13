from django.db import models
from users.models import User, Agent
from users.utils import upload_verification_document_path, validate_document
# Create your models here.

Status = (
    ('pending', 'pending'),
    ('created', 'created'),
    ('accepted', 'accepted'),
    ('rejected', 'rejected')
)


class Documents(models.Model):
    user = models.OneToOneField(Agent, on_delete=models.CASCADE)
    government_issued_id = models.FileField(upload_to=upload_verification_document_path, validators=[
        validate_document], null=True, blank=True)
    utility_bill = models.FileField(upload_to=upload_verification_document_path, validators=[
        validate_document], null=True, blank=True)
    cac_document = models.FileField(upload_to=upload_verification_document_path, validators=[
        validate_document], null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=Status, max_length=10, default='created')
    message = models.TextField(blank=True, null=True, max_length=300)

    class Meta:
        verbose_name_plural = "Agent documents"

    def __str__(self):
        return str(self.user)
