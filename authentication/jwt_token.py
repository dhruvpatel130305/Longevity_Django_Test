from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    """
        Function for generating access and refresh token
    """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
