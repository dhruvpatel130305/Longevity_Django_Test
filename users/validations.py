from rest_framework.exceptions import ValidationError

from users.constants import PASSWORD_SHORT_LENGTH_ERROR, PASSWORD_LONG_LENGTH_ERROR, PASSWORD_CONTAINS_NO_DIGIT_ERROR, \
    PASSWORD_CONTAINS_NO_SPECIAL_CHARACTER_ERROR, PASSWORD_CONTAINS_NO_UPPERCASE_ERROR, \
    PASSWORD_CONTAINS_NO_LOWERCASE_ERROR


def custom_validate_password(password):
    """
    Function to validate user password
    :param password: takes in password and validates it
    :return: validated password
    """

    special_symbol = ['$', '@', '#', '%']
    password_error = []

    if len(password) < 8:
        password_error.append(PASSWORD_SHORT_LENGTH_ERROR)

    if len(password) > 20:
        password_error.append(PASSWORD_LONG_LENGTH_ERROR)

    if not any(char.isdigit() for char in password):
        password_error.append(PASSWORD_CONTAINS_NO_DIGIT_ERROR)

    if not any(char.isupper() for char in password):
        password_error.append(PASSWORD_CONTAINS_NO_UPPERCASE_ERROR)

    if not any(char.islower() for char in password):
        password_error.append(PASSWORD_CONTAINS_NO_LOWERCASE_ERROR)

    if not any(char in special_symbol for char in password):
        password_error.append(PASSWORD_CONTAINS_NO_SPECIAL_CHARACTER_ERROR)

    if password_error:
        raise ValidationError(password_error)
    return password
