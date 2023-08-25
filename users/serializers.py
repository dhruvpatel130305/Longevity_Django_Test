from rest_framework import serializers

from users.models import User
from users.validations import custom_validate_password


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer to retrieve, update, delete and list user.
    """

    class Meta:
        model = User
        fields = ['id', 'gender', 'email', 'username', 'first_name',
                  'last_name', 'phone_number',
                  'is_active']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer to register user.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[custom_validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'gender', 'email', 'username', 'first_name',
                  'last_name', 'phone_number', 'password', 'confirm_password',
                  'is_active']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        """
        validate password and confirm password
        :param data:
        :return: json data
        """
        password = data.get('password')
        confirm_password = data.pop('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError({'validation_error': "Passwords do not match."})
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserDeleteSerializer(serializers.ModelSerializer):
    """
    Serializer to delete user
    """

    class Meta:
        model = User
        fields = []
