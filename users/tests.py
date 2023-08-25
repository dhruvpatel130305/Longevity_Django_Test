from datetime import datetime

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User


class UserListCreateViewTest(APITestCase):
    """
    Test cases to test user registration and list API
    """
    url = reverse('list-register-user')

    def test_create_user(self):
        """
        Test user registration when valid data is provided
        """
        data = {
            "gender": "female",
            "email": "testuser1@gmail.com",
            "username": "testuser1",
            "first_name": "Mark",
            "last_name": "Lee",
            "phone_number": "+918485878167",
            "is_active": True,
            "password": "Testuser$123",
            "confirm_password": "Testuser$123"
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser1')

    def test_invalid_email(self):
        """
        Test user registration when invalid email is provided
        """
        data = {
            "gender": "female",
            "email": "testuser1gmail.com",
            "username": "testuser1",
            "first_name": "Mark",
            "last_name": "Lee",
            "phone_number": "+918485878167",
            "is_active": True,
            "password": "testuser1",
            "confirm_password": "testuser1"
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_invalid_phone_number(self):
        """
        Test user registration when invalid phone number is provided
        """
        data = {
            "gender": "female",
            "email": "testuser1@gmail.com",
            "username": "testuser1",
            "first_name": "Mark",
            "last_name": "Lee",
            "phone_number": "8485878167",
            "is_active": True,
            "password": "testuser1",
            "confirm_password": "testuser1"
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_missing_email_field(self):
        """
        Test user registration when email field is missing
        """
        data = {
            "gender": "female",
            "username": "testuser1",
            "first_name": "Mark",
            "last_name": "Lee",
            "phone_number": "+918485878167",
            "is_active": True,
            "password": "testuser1",
            "confirm_password": "testuser1"
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_password_validation_check_for_min_length_8_characters(self):
        """
        Test user password length less than 8 characters
        """
        data = {
            "email": "testuser1@gmail.com",
            "gender": "female",
            "username": "testuser1",
            "first_name": "Mark",
            "last_name": "Lee",
            "phone_number": "+918485878167",
            "is_active": True,
            "password": "T@123",
            "confirm_password": "testuser1"
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_password_validation_check_for_max_length_20_characters(self):
        """
        Test user password exceeding 20 characters
        """
        data = {
            "email": "testuser1@gmail.com",
            "gender": "female",
            "username": "testuser1",
            "first_name": "Mark",
            "last_name": "Lee",
            "phone_number": "+918485878167",
            "is_active": True,
            "password": "Test@1234567890123456789",
            "confirm_password": "testuser1"
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_password_validation_check_for_digit(self):
        """
        Test user password missing digit
        """
        data = {
            "email": "testuser1@gmail.com",
            "gender": "female",
            "username": "testuser1",
            "first_name": "Mark",
            "last_name": "Lee",
            "phone_number": "+918485878167",
            "is_active": True,
            "password": "Test@testtest",
            "confirm_password": "testuser1"
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_password_validation_check_for_lower_case_character(self):
        """
        Test user password missing lower case letter
        """
        data = {
            "email": "testuser1@gmail.com",
            "gender": "female",
            "username": "testuser1",
            "first_name": "Mark",
            "last_name": "Lee",
            "phone_number": "+918485878167",
            "is_active": True,
            "password": "AFGF@123456",
            "confirm_password": "testuser1"
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_password_validation_check_for_upper_case_character(self):
        """
        Test user password missing upper case letter
        """
        data = {
            "email": "testuser1@gmail.com",
            "gender": "female",
            "username": "testuser1",
            "first_name": "Mark",
            "last_name": "Lee",
            "phone_number": "+918485878167",
            "is_active": True,
            "password": "test@12345",
            "confirm_password": "testuser1"
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_password_validation_check_for_special_character(self):
        """
        Test user password not having special character
        """
        data = {
            "email": "testuser1@gmail.com",
            "gender": "female",
            "username": "testuser1",
            "first_name": "Mark",
            "last_name": "Lee",
            "phone_number": "+918485878167",
            "is_active": True,
            "password": "Test12345",
            "confirm_password": "testuser1"
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_missing_username_field(self):
        """
        Test user registration when username field is missing
        """
        data = {
            "gender": "female",
            "email": "testuser1@gmail.com",
            "first_name": "Mark",
            "last_name": "Lee",
            "phone_number": "+918485878167",
            "is_active": True,
            "password": "testuser1",
            "confirm_password": "testuser1"
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_missing_gender_field(self):
        """
        Test user registration when gender field is missing
        """
        data = {
            "email": "testuser1@gmail.com",
            "username": "testuser1",
            "first_name": "Mark",
            "last_name": "Lee",
            "phone_number": "+918485878167",
            "is_active": True,
            "password": "testuser1",
            "confirm_password": "testuser1"
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_missing_first_name_field(self):
        """
        Test user registration when first name field is missing
        """
        data = {
            "gender": "female",
            "email": "testuser1@gmail.com",
            "username": "testuser1",
            "last_name": "Lee",
            "phone_number": "+918485878167",
            "is_active": True,
            "password": "testuser1",
            "confirm_password": "testuser1"
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_missing_last_name_field(self):
        """
        Test user registration when last name field is missing
        """
        data = {
            "gender": "female",
            "email": "testuser1@gmail.com",
            "username": "testuser1",
            "first_name": "Mark",
            "phone_number": "+918485878167",
            "is_active": True,
            "password": "testuser1",
            "confirm_password": "testuser1"
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_missing_password_field(self):
        """
        Test user registration when password field is missing
        """
        data = {
            "gender": "female",
            "email": "testuser1@gmail.com",
            "username": "testuser1",
            "first_name": "Mark",
            "last_name": "Lee",
            "phone_number": "+918485878167",
            "is_active": True,
            "confirm_password": "testuser1"
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_missing_confirm_password_field(self):
        """
        Test user registration when confirm password field is missing
        """
        data = {
            "gender": "female",
            "email": "testuser1@gmail.com",
            "username": "testuser1",
            "first_name": "Mark",
            "last_name": "Lee",
            "phone_number": "+918485878167",
            "is_active": True,
            "password": "testuser1"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_duplicate_user_creation_with_username(self):
        """
        Test user registration when user already exists with same username
        """
        User.objects.create(username='testuser1')
        data = {
            "gender": "female",
            "email": "testuser1@gmail.com",
            "username": "testuser1",
            "first_name": "Mark",
            "last_name": "Lee",
            "phone_number": "+918485878167",
            "is_active": True,
            "password": "testuser1",
            "confirm_password": "testuser1"
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_duplicate_user_creation_with_email(self):
        """
        Test user registration when user already exists with same email
        """
        User.objects.create(email='testuser1@gmail.com')
        data = {
            "gender": "female",
            "email": "testuser1@gmail.com",
            "username": "testuser1",
            "first_name": "Mark",
            "last_name": "Lee",
            "phone_number": "+918485878267",
            "is_active": True,
            "password": "testuser1",
            "confirm_password": "testuser1"
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_duplicate_user_creation_with_phone_number(self):
        """
        Test user registration when user already exists with same phone number
        """
        User.objects.create(phone_number='+918485878167')
        data = {
            "gender": "female",
            "email": "testuser1@gmail.com",
            "username": "testuser1",
            "first_name": "Mark",
            "last_name": "Lee",
            "phone_number": "+918485878167",
            "is_active": True,
            "password": "testuser1",
            "confirm_password": "testuser1"
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_first_name_having_characters(self):
        """
        Test user registration when user enters digits in first name
        """
        data = {
            "gender": "female",
            "email": "testuser1@gmail.com",
            "username": "testuser1",
            "first_name": "332",
            "last_name": "Lee",
            "phone_number": "+918485878167",
            "is_active": True,
            "password": "testuser1",
            "confirm_password": "testuser1"
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_last_name_having_characters(self):
        """
        Test user registration when user enters digits in last name
        """
        data = {
            "gender": "female",
            "email": "testuser1@gmail.com",
            "username": "testuser1",
            "first_name": "Mark",
            "last_name": "776",
            "phone_number": "+918485878167",
            "is_active": True,
            "password": "testuser1",
            "confirm_password": "testuser1"
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_list_users(self):
        """
        Test users list API
        """
        User.objects.create(username='user1', email='user1@gmail.com')
        User.objects.create(username='user2', email='user2@gmail.com')

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 2)

    def test_ordering(self):
        """
        Test users list API with ordering
        """
        user1 = User.objects.create(username='user1', email='user1@example.com')
        user2 = User.objects.create(username='user2', email='user2@example.com')

        response = self.client.get(self.url, {'ordering': 'id'})  # Ordering by id
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data'][0]['id'], user2.id)


class RetrieveUpdateDestroyAPIViewTest(APITestCase):
    """
    Test cases to test user retrieve, update and delete API
    """

    def setUp(self):
        """
        Setup users in database and define url
        """
        self.user = User.objects.create(username='testuser', email='testuser@example.com', phone_number="+917678954377",
                                        gender="female", first_name='test', last_name='user1', is_active=True
                                        )
        self.user1 = User.objects.create(username='testuser3', email='testuser3@example.com',
                                         phone_number="+917278954377",
                                         gender="female", first_name='test', last_name='user1', is_active=True
                                         )
        self.user.set_password("password")
        self.user1.set_password("password")
        self.url = reverse('retrieve-update-delete-user')

    def test_retrieve_user_profile(self):
        """
        Test case to retrieve user
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_retrieve_user_profile_with_unauthorized_user(self):
        """
        Test case to retrieve user
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_profile_with_unauthorized_user(self):
        """
        Test case to retrieve user
        """
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_profile(self):
        """
        Test case to update user with valid data
        """
        new_data = {
            "gender": "male",
            "email": "testuser1@gmail.com",
            "username": "testuser1",
            "first_name": "Mark",
            "last_name": "Lee",
            "phone_number": "+917485878167",
            "is_active": True,
            "password": "testuser1",
            "confirm_password": "testuser1"
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['gender'], 'male')
        self.assertEqual(response.data['data']['email'], 'testuser1@gmail.com')
        self.assertEqual(response.data['data']['username'], 'testuser1')
        self.assertEqual(response.data['data']['first_name'], 'Mark')
        self.assertEqual(response.data['data']['last_name'], 'Lee')
        self.assertEqual(response.data['data']['phone_number'], '+917485878167')
        self.assertEqual(response.data['data']['is_active'], True)
        self.assertEqual(response.data['message'], "Account details updated successfully.")

    def test_update_user_with_email_already_existing_in_database(self):
        """
        Test case to update user when user enters email that already exists in database
        """
        new_data = {
            "gender": "male",
            "email": "testuser3@example.com",
            "username": "testuser1",
            "first_name": "Mark",
            "last_name": "Lee",
            "phone_number": "+917485878167",
            "is_active": True,
            "password": "testuser1",
            "confirm_password": "testuser1"
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'], ["User details with this email already exists."])

    def test_update_user_with_phone_number_already_existing_in_database(self):
        """
        Test case to update user when user enters phone number that already exists in database
        """
        new_data = {
            "gender": "male",
            "email": "testuser1@example.com",
            "username": "testuser1",
            "first_name": "Mark",
            "last_name": "Lee",
            "phone_number": "+917278954377",
            "is_active": True,
            "password": "testuser1",
            "confirm_password": "testuser1"
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['phone_number'], ["User details with this phone number already exists."])

    def test_update_user_with_username_already_existing_in_database(self):
        """
        Test case to update user when user enters username that already exists in database
        """
        new_data = {
            "gender": "male",
            "email": "testuser1@example.com",
            "username": "testuser3",
            "first_name": "Mark",
            "last_name": "Lee",
            "phone_number": "+917298954377",
            "is_active": True,
            "password": "testuser1",
            "confirm_password": "testuser1"
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['username'], ["A user with this username already exists."])

    def test_delete_user_profile_with_unauthorized_user(self):
        """
        Test case to retrieve user
        """
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_user(self):
        """
        Test case to delete active user
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['message'], "Account deleted successfully.")
