from users.utils import send_instant_mail,current_site
from django.db.models.signals import  post_save, pre_save
from .models import Review
from django.dispatch import receiver
from propexx.settings.base import EMAIL_HOST_USER
from django.contrib.sites.models import Site





@receiver(post_save,  sender = Review)
def notify_buyer_on_request_for_Review(sender,instance, created, *args, **kwargs):
    if created and instance.status == 'pending':
        print('if param', instance.status)
        title = 'Propexx'
        message  = f"your request for {instance.property} is being proccessed,\n we will asign you to our agent as soon as possible ."
        context = {
                'current_site': f'https://{current_site.domain}',
                'title': title,
                'current_user': instance,
                'username': instance.user.first_name,
                'email': instance.user.email,
                'message': message,
                'property': instance.property
        }
        send_instant_mail.delay(
                instance.user.email, 'Agent Asssigned for Property Review', EMAIL_HOST_USER, 'email/request_review.html', context
            )
    elif instance.status == 'assigned':
        print('else if param', instance.status)
        title = 'Propexx'
        context = {
                'current_site': f'https://{current_site.domain}',
                'title': title,
                'current_user': instance,
                'username': instance.user.first_name,
                'email': instance.user.email,
                'agent_first_name': instance.assiged_agent.first_name,
                'agent_last_name':  instance.assiged_agent.last_name,
                'agent_number': instance.assiged_agent.phone_number,
                'agent_whatapp':instance.assiged_agent.whatapp_number,
                'agent_email': instance.assiged_agent.email,
                'property': instance.property
        }
        send_instant_mail.delay(
                instance.user.email, 'Agent Assigned for property review', EMAIL_HOST_USER, 'email/agent_detail.html', context
            )


# @receiver(pre_save, sender = Review)
# def notify_agent_after_asig

