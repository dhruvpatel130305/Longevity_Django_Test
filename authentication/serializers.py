from rest_framework import serializers


class LoginWithPasswordSerializer(serializers.Serializer):
    """
    Serializer  for user login with password
    """
    email = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['email', 'password']


class SendOtpSerializer(serializers.Serializer):
    """
    Serializer to send otp to user
    """
    email = serializers.CharField(max_length=150)

    class Meta:
        fields = ['email']


class LoginWithOtpSerializer(serializers.Serializer):
    """
    Serializer for user login with otp
    """
    otp = serializers.IntegerField(write_only=True)

    class Meta:
        fields = ['otp']