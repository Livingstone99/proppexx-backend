from datetime import datetime, timedelta
from propexx.settings.base import PAYSTACK_SECRET_KEY

import requests
from django.utils import timezone
from django.contrib.sites.models import Site
from celery import task
import threading
from django.core.validators import RegexValidator

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
# upload to the media_cdn
import random
import string
import os
from django.core.exceptions import ValidationError


def upload_location(instance, filename):
    return f'{instance.id}{filename}'


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_avatar_path(instance, filename):
    new_filename = instance.first_name
    name, ext = get_filename_ext(filename)
    final_filename = f"{new_filename}{ext}"
    return f"avatar/{final_filename}"


def upload_verification_document_path(instance, filename):
    new_filename = instance.user
    name, ext = get_filename_ext(filename)
    final_filename = f"{new_filename}{ext}"
    return f"documents/{final_filename}"


def upload_property_path(instance, filename):
    new_filename = instance.property
    name, ext = get_filename_ext(filename)
    final_filename = f"{new_filename}{ext}"
    return f"property/{final_filename}"


def upload_property_document_path(instance, filename):
    new_filename = instance.slug
    name, ext = get_filename_ext(filename)
    final_filename = f"{new_filename}{ext}"
    return f"property-document/{final_filename}"


def validate_document(image):
    file_size = image.size
    limit_kb = 5000
    if file_size > limit_kb * 1024:
        raise ValidationError(
            f"Document size is {file_size}KB. Max size of file is {limit_kb}KB")


# phone number regex
phone_regex = RegexValidator(
    r'^\d{11}$',
    message="Input a valid phone number (must be 11 digits)."
)


class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.is_email_verified) + text_type(user.pk) + text_type(timestamp)

    # if not PasswordResetTokenGenerator.check_token(user, token)
token_generator = AppTokenGenerator()


def intcomma(value):
    """Add comma on every 10^3. Returns string."""
    value = str(value)

    dot_position = value.find('.')

    if dot_position != -1:
        int_part, decimal_part = value[:dot_position], value[dot_position:]
    else:
        int_part, decimal_part = value, ''

    comma_position = int_part.find(',')

    if comma_position != -1:
        left, right = int_part[:comma_position], int_part[comma_position:]
    else:
        left, right = int_part, ''

    if len(left) > 3:
        comma_ready = ''.join((intcomma(left[:-3]), ',', left[-3:], right))
        if decimal_part:
            return ''.join((comma_ready, decimal_part))
        else:
            return comma_ready
    return value


def random_string_generator(size=8,
                            chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def random_uniquekey_generator(size=5,
                               chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def validate_image(image):
    file_size = image.size
    limit_kb = 1000
    if file_size > limit_kb * 1024:
        raise ValidationError(
            f"Image size is {file_size}KB. Max size of file is {limit_kb}KB")


@task(serializer='pickle')
def send_instant_mail(user_email, email_title, email_sender, template, context):
    '''
        user email,
        email_title,
        email_sender,
        template,
        context
    '''
    email_html_message = render_to_string(
        template, context)
    msg = EmailMultiAlternatives(
        # title:
        "{email} {title}".format(email=email_title, title="Propexx"),
        # message:
        '',
        # from:
        email_sender,
        # to:
        [user_email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()


try:
    current_site = Site.objects.get_current()
except:
    current_site = "https://test.com"


def delete_draft():
    # import positioned here to avoid circular import exception
    from property.models import Draft
    DURATION = os.getenv('DURATION')
    duration = timezone.now() - timedelta(days=int(DURATION))
    Draft.objects.filter(updated_at__gte = duration).delete()

def cancel_paystack_subscription():
    from subscription.models import Subscription

    subscriptions = Subscription.objects.filter(active=True)
    for subscription in subscriptions:
        schedule = timezone.now()- subscription.created_at

        if  schedule >= timedelta(days = 27):
            url = 'https://api.paystack.co/subscription/disable'
            payload = {"code": subscription.subscription_code,"token":subscription.email_token}
            response = requests.post(url, data=payload,  headers={'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}'})
            subscription.active = False
            subscription.save()
            print('#######################################',response.json())
        
def generate_otp(phone_number):
    import math, random
    digit = str(phone_number)
    otp = ""
    for i in range(4):
        otp += digit[math.floor(random.random()*10)]
    return otp

