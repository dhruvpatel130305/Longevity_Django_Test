from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions
import base64
import datetime

import pyotp
from django.utils import timezone

from authentication.constants import EMAIL_MESSAGE
from users.models import User
from authentication.tasks import send_email


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    """
    Generates both http and https schema for swagger
    """
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]
        return schema


schema_view = get_schema_view(
    openapi.Info(
        title="Django API",
        default_version='v1',
        description="Django Test",
        security='Bearer',
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    generator_class=BothHttpAndHttpsSchemaGenerator,
)

class generateKey:
    """
        class to return value for generating key
    """
    @staticmethod
    def returnValue(email):
        return str(email) + "Some Random Secret Key"


def generate_otp(email):
    """
        Function to generate otp
    """
    keygen = generateKey()
    key = base64.b32encode(keygen.returnValue(email).encode())
    totp = pyotp.TOTP(key)
    otp = totp.now()
    return otp


def prepare_and_send_email(email, request_data, otp):
    """Function to send Email Through celery """
    user = User.objects.get(email=email)
    html_page = 'otp_template.html'
    subject = 'Otp for login'
    text_file = 'otp_template.txt'
    data = {
        'message': EMAIL_MESSAGE,
        'username': user.username,
        "login_otp": otp
    }
    send_email.delay(html_page, text_file, subject, email, data)


def verify_otp(request):
    """
        function to verify otp
    """
    current_time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user = User.objects.filter(otp=request.data["otp"]).first()
    if user is not None and user.otp == int(request.data["otp"]) and current_time_str <= str(
            timezone.localtime(user.otp_validity)):
        user.otp = None
        user.otp_validity = None
        user.save()
        return user
    return False
