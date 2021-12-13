from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Feedback
from users.utils import random_string_generator


@receiver(pre_save, sender=Feedback)
def feedback_pre_save_reciever(sender, instance, *args, **kwargs):
    if not instance.feedback_id:
        instance.feedback_id = random_string_generator()
