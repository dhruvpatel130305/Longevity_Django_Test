from datetime import datetime, timedelta

from django.contrib.auth.hashers import check_password
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.constants import EMAIL_ERROR, EMAIL_SUCCESS, OTP_VALIDATION, PASSWORD_ERROR
from authentication.jwt_token import get_tokens_for_user
from authentication.serializers import LoginWithPasswordSerializer, SendOtpSerializer, LoginWithOtpSerializer
from authentication.utils import generate_otp, prepare_and_send_email, verify_otp
from django_test.settings import OTP_EXPIRATION_TIME
from users.models import User


class LoginWithPasswordView(APIView):
    """
        APIView to login with email and password
    """
    @swagger_auto_schema(request_body=LoginWithPasswordSerializer)
    def post(self, request, *args, **kwargs):
        serializers = LoginWithPasswordSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()
        if not user:
            raise ValidationError({"message": EMAIL_ERROR})
        if not check_password(password, user.password):
            raise ValidationError({"message": PASSWORD_ERROR})
        data = get_tokens_for_user(user)
        return Response(data, status=status.HTTP_200_OK)


class SendOtpView(APIView):
    """
        APIView to send otp through email
    """

    @swagger_auto_schema(request_body=SendOtpSerializer)
    def post(self, request, *args, **kwargs):
        serializer = SendOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if not user:
            raise ValidationError({"message": EMAIL_ERROR})
        otp = generate_otp(email)
        prepare_and_send_email(serializer.data.get('email'), request, otp)
        future_time = datetime.now() + timedelta(minutes=int(OTP_EXPIRATION_TIME))
        future_time_str = future_time.strftime("%Y-%m-%d %H:%M:%S")
        User.objects.filter(email=email).update(otp=otp, otp_validity=future_time_str)
        return Response({"message": EMAIL_SUCCESS}, status=status.HTTP_200_OK)


class LoginWithOtpView(APIView):
    """
        APIView to validate otp for login
    """

    @swagger_auto_schema(request_body=LoginWithOtpSerializer)
    def post(self, request, *args, **kwargs):
        serializers = LoginWithOtpSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        verified_user = verify_otp(request)
        if not verified_user:
            raise ValidationError({"message": OTP_VALIDATION})
        data = get_tokens_for_user(verified_user)
        return Response(data, status=status.HTTP_200_OK)
