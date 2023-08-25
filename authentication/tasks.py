import smtplib

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response

from django_test.settings import EMAIL_HOST_USER


@shared_task
def send_email(html_page, text_file, subject, email, data):
    """
        Function to send email
    """
    try:
        message = render_to_string(text_file, data)
        html_body = render_to_string(html_page, data)
        emails = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=EMAIL_HOST_USER,
            to=[email],
        )

        emails.attach_alternative(html_body, "text/html")
        emails.send()
    except smtplib.SMTPSenderRefused as e:
        return Response({"data": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return True
