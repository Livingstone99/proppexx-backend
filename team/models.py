from users.models import User
from django.db import models
from django.db.models.fields.related import OneToOneField
from users.utils import phone_regex
# Create your models here.

class AdminAgent(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    phone_number = models.CharField(max_length=11, validators=[phone_regex])
    whatapp_number = models.CharField(max_length=11, validators=[phone_regex])
    email = models.EmailField(blank=True, null=True)

    def  __str__(self):
        return f'{self.first_name} {self.last_name}'
class Team(models.Model):
    developer = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.developer)
    

class Member(models.Model):
    team = models.ForeignKey(Team, on_delete= models.CASCADE, related_name= 'member')
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    phone_number = models.CharField(max_length=11, validators=[phone_regex])
    whatapp_number = models.CharField(max_length=11, validators=[phone_regex])
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.first_name
    