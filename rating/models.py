from django.db import models
from users.models import User, Buyer, Agent
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class AgentRating(models.Model):
    buyer_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='buyer_user', null= True)
    agent_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='agent_user', null=True)
    rate = models.IntegerField(validators = [
        MaxValueValidator(5), MinValueValidator(0)
    ])
    comment = models.TextField(max_length=200)
    selected = models.BooleanField(default = False)
    sent_eligibilty = models.BooleanField(default= False)
    
    # clause_together = ('buyer_user', 'agent_user',)

    def __str__(self):
        return f'{self.agent_user}'
