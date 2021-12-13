from propexx.settings.base import EMAIL_HOST_USER
from users.utils import send_instant_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from users.models import User, Agent
from  .models import Documents
from users.utils  import send_instant_mail

@receiver(post_save, sender = Agent)
def create_document(sender, instance, created, **kwargs):
    if created:
        documents = Documents.objects.get_or_create(user = instance)


@receiver(pre_save, sender = Documents)
def update_document(sender, instance, **kwargs):
    
    if instance.status == 'created':
        if instance.created_at != instance.updated_at:
            instance.status = 'pending'
    
        

# @receiver(post_save, sender = Documents)
# def send_mail(sender, instance, **kwargs):
#     if instance.status == 'rejected':
#         current_site = Site.objects.get_current()
#         title = 'Propexx'
#         context = {
#                 'current_site': f'http://{current_site.domain}',
#                 'title': title,
#                 'current_user': instance,
#                 'username': instance.user.agents.first_name,
#                 'email': instance.user.agents.email,
#                 'message': instance.message
               
#             }
#         send_instant_mail.delay(
#                 instance.email, 'rejected documents', EMAIL_HOST_USER, 'email/rejected.html', context
#             )