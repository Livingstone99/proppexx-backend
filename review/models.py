from django.db import models
from users.models import User
from property.models import Property
from users.utils import phone_regex
from team.models import AdminAgent
# Create your models here.


class Review(models.Model):
    Status = (
        ('pending', 'pending'),
        ('assigned', 'assigned'),
        ('reviewed', 'reviewed')
    )
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    status = models.CharField(choices=Status,default='pending', max_length=10)
    assiged_agent = models.ForeignKey(AdminAgent, on_delete=models.CASCADE, null=True)
    refrence_code = models.CharField(max_length= 15,  blank=True, null=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        unique_together  = ('user', 'property',)
    