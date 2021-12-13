from django.shortcuts import get_object_or_404
from users.models import Agent, User
from rating.models import AgentRating
from propexx.settings.base import EMAIL_HOST_USER
from users.utils import send_instant_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Verification
from users.utils import current_site


# @receiver(post_save, sender=Verification)
# def pushNotification(sender, instance, created, **kwargs):
#     if instance.status == 'accepted':
#         # send an e-mail to the user
#         context = {
#             'current_site': f'https://{current_site.domain}',
#             'username': instance.user.first_name,
#             'email': instance.user.email,
#         }

#         send_instant_mail.delay(
#                 instance.user.email, 'Accepted', EMAIL_HOST_USER, 'email/accepted.html', context)

#     elif instance.status == 'rejected':
#         # send an e-mail to the user
#         context = {
#             'current_site': f'https://{current_site.domain}',
#             'username': instance.user.first_name,
#             'email': instance.user.email,
#             'reply': instance.response
#         }

#         send_instant_mail.delay(
#                 instance.user.email, 'Rejected', EMAIL_HOST_USER, 'email/reject.html', context)

@receiver(post_save, sender= AgentRating)
def check_agent_eligibilty(sender, instance, *args, **kwargs):
    agent = get_object_or_404(Agent, agents = instance.agent_user)
    if int(agent.total_rev) == 3:
        print(f'############ total_rev{agent.total_rev}')
        # print(f'############ rating{agent.total_rev}')
        verify_state = get_object_or_404(Agent, agents  = instance.agent_user)
        if float(verify_state.ratings) >= 3.0 and not verify_state.verified and not instance.sent_eligibilty:
            verification = Verification.objects.get_or_create(user = instance.agent_user, status = 'pending')

            instance.sent_eligibilty = True
            instance.save(update_fields=['sent_eligibilty'])

            context = {
            'current_site': f'https://{current_site.domain}',
            'username': verify_state.agents.first_name,
            'email': verify_state.agents.email,
            }
            
            send_instant_mail.delay(
                    verify_state.agents.email, 'Verification Eligibilty', EMAIL_HOST_USER, 'email/elibilty.html', context)

@receiver(post_save, sender = Verification)
def email_accept_or_decline_eligibilty(sender, instance, *args, **kwargs ):
    if instance.status == 'accepted' or instance.status == 'rejected':
         context = {
            'current_site': f'https://{current_site.domain}',
            'username': instance.user.first_name,
            'email': instance.user.email,
            'status': instance.status,
            'response': instance.response
            }
         send_instant_mail.delay(
                    instance.user.email, 'Verification Eligibilty', EMAIL_HOST_USER, 'email/message.html', context)
         if instance.status == 'accepted':
              verify_state = get_object_or_404(Agent, agents  = instance.user)
              verify_state.verified = True
              verify_state.save(update_fields=['verified'])
       