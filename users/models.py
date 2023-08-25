from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from users.constants import USERNAME_HELPTEXT, UNIQUE_USERNAME, FIRSTNAME_ERROR, LASTNAME_ERROR


class User(AbstractUser):
    """
    Stores user's personal and authentication details.
    """
    genders = (
        ('female', 'Female'),
        ('male', 'Male'),
        ('other', 'Other'),
    )
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=50,
        unique=True,
        help_text=(
            USERNAME_HELPTEXT
        ),
        validators=[username_validator, MinLengthValidator(2)],
        error_messages={
            "unique": UNIQUE_USERNAME,
        },
    )
    first_name = models.CharField(max_length=50, validators=[MinLengthValidator(2), RegexValidator(
        regex='^[a-zA-Z]+$',
        message=FIRSTNAME_ERROR,
        code='first_name'
    )])
    last_name = models.CharField(max_length=50, validators=[MinLengthValidator(2), RegexValidator(
        regex='^[a-zA-Z]+$',
        message=LASTNAME_ERROR,
        code='last_name'
    )])
    gender = models.CharField(max_length=10, choices=genders)
    password = models.CharField(max_length=128)
    phone_number = PhoneNumberField(unique=True, null=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)

    otp = models.IntegerField(null=True, blank=True)
    otp_validity = models.DateTimeField(null=True)

    class Meta:
        db_table = 'AuthUsers'
        verbose_name = "User details"
        indexes = [
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.username}-{self.id}"