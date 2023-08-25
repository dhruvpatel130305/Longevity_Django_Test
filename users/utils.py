from django.utils import timezone

from users.constants import DATE_TIME_FORMAT


def current_time():
    """
    Get current time
    :return: current time
    """
    today = timezone.now()
    current_time = today.strftime(DATE_TIME_FORMAT)
    return current_time
