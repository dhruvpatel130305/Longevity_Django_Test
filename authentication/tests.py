from unittest.mock import patch
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from django.contrib.auth import get_user_model

from authentication.constants import EMAIL_MESSAGE, OTP_VALIDATION, EMAIL_ERROR, PASSWORD_ERROR
from django.contrib.auth.hashers import make_password

User = get_user_model()


class TestLoginCase(APITestCase):
    """
        Test case for login user
    """
    login_with_password_url = reverse('login-with-password')
    login_otp_url = reverse('send-otp')
    login_with_otp_url = reverse('login-with-otp')

    def setUp(self):
        """Setup To create user"""
        future_time = datetime.now() + timedelta(minutes=10)
        future_time_str = future_time.strftime("%Y-%m-%d %H:%M:%S")
        self.user = User.objects.create(username='testuser', email='testuser@example.com', phone_number="+917678954377",
                                        gender="female", first_name='test', last_name='user1', is_active=True, password=make_password("password")
                                        )

        self.user_with_otp =  User.objects.create(username='testuser3', email='testuser3@example.com',
                                         phone_number="+917278954377", password=make_password("password"),
                                         gender="female", first_name='test', last_name='user1', is_active=True, otp=304050, otp_validity=future_time_str
                                         )

    def test_login_response_200(self):
        """ Test case for login"""
        data = {'email': "testuser@example.com", 'password': "password"}
        response = self.client.post(self.login_with_password_url, data)
        body = response.json()
        self.assertEquals(response.status_code, 200, body)
        self.assertTrue('refresh' in body, True)
        self.assertTrue('access' in body, True)

    def test_login_with_wrong_email(self):
        """ Test case to login with wrong username"""
        data = {'email': 'testuser1@example.com', 'password': "password"}
        response = self.client.post(self.login_with_password_url, data)
        body = response.json()
        self.assertEquals(response.status_code, 400, body)
        self.assertEquals(body['message'], EMAIL_ERROR)

    def test_login_with_wrong_password(self):
        """ Test case to login with wrong password"""
        data = {'email': "testuser@example.com", 'password': "password123"}
        response = self.client.post(self.login_with_password_url, data)
        body = response.json()
        self.assertEquals(response.status_code, 400, body)
        self.assertEquals(body['message'], PASSWORD_ERROR)

    @patch('rest_framework.test.APIClient.post')
    def test_otp_send(self, mock_post):
        """
            Test case to send otp on email
        """
        data = {'email': "testuser@example.com"}
        mock_response = self.client.post(self.login_otp_url, data)
        mock_response.status_code = status.HTTP_200_OK
        mock_response.content = {"message": EMAIL_MESSAGE}
        mock_post.return_value = mock_response
        self.assertEqual(mock_response.status_code, status.HTTP_200_OK)

    def test_otp_verified(self):
        """
            Test case to verify correct otp
        """
        data = {'otp': "304050"}
        self.client.force_authenticate(user=self.user_with_otp)
        response = self.client.post(self.login_with_otp_url, data)
        body = response.json()
        self.assertEquals(response.status_code, 200, body)
        self.assertTrue('refresh' in body, True)
        self.assertTrue('access' in body, True)

    def test_otp_unverified(self):
        """
            Test case to verify incorrect otp
        """
        data = {'otp': "304070"}
        self.client.force_authenticate(user=self.user_with_otp)
        response = self.client.post(self.login_with_otp_url, data)
        body = response.json()
        self.assertEquals(response.status_code, 400, body)
        self.assertEquals(body['message'], OTP_VALIDATION)
