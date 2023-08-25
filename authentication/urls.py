from django.urls import path

from authentication.views import LoginWithPasswordView, LoginWithOtpView, SendOtpView

urlpatterns = [
    path('login-with-password/', LoginWithPasswordView.as_view(), name='login-with-password'),
    path('login-with-otp', LoginWithOtpView.as_view(), name='login-with-otp'),
    path('send-otp', SendOtpView.as_view(), name='send-otp'),
]