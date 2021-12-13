from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from celery import task


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
