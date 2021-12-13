from team.models import Team
from django.contrib.sites.models import Site
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import ugettext_lazy as _
from .utils import (phone_regex, token_generator, upload_location,)
from .models import User, Agent, Buyer
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.template.loader import render_to_string
from users.models import Agent, Buyer
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from users.utils import send_instant_mail, current_site
from propexx.settings.base import EMAIL_HOST_USER
from subscription.models import Customer, userMembershipFeatures


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    userMembershipFeatures.objects.get_or_create(user=instance)
    if instance.user_type == 'agent':
        Agent.objects.get_or_create(agents=instance)
    elif instance.user_type == 'buyer':
        Buyer.objects.get_or_create(buyers=instance)
    elif instance.user_type == 'developer':
        Team.objects.get_or_create(developer = instance)
    else:
        pass


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.user_features.save()
    if instance.user_type == 'buyer':
        instance.buyer_profile.save()
    elif instance.user_type == 'agent':
        instance.agent_profile.save() 
    elif instance.user_type == 'developer':
        instance.team.save()
    else:
        pass


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_site': f'http://{current_site.domain}',
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.first_name,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
    }

    send_instant_mail.delay(
                reset_password_token.user.email, 'Password Reset', EMAIL_HOST_USER, 'email/user_reset_password.html', context)
        
    

@receiver(post_save, sender=User)
def verify_on_signup(sender, instance, created, **kwargs):
    if created:
        print("instance check", instance)
        if instance.social_auth.exists() is False:
            title = 'Propexx'

            uidb64 = urlsafe_base64_encode(force_bytes(instance.pk))

            relativeLink = reverse('activate', kwargs={
                'uidb64': uidb64, 'token': token_generator.make_token(instance)})
            context = {
                'current_site': f'https://{current_site.domain}',
                'current_user': instance,
                'username': instance.first_name,
                'email': instance.email,
                'absurl': relativeLink
            }

            # send_instant_mail.delay(
            #     instance.email, 'Verify Account', EMAIL_HOST_USER, 'email/verify_email.html', context)
