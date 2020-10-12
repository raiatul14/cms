from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model # If used custom user model

User = get_user_model()

class RegistrationTest(APITestCase):
    def setUp(self):
        self.create_url = reverse('register_api')
    
    def test_create_user(self):
        """
        Ensure we can create a new user.
        """
        data = {
            'email': 'foobar@example.com',
            'password': 'SomePass123',
            'full_name': 'Atul Rai',
            'phone': 7483847123,
            'pincode': 400025
        }

        response = self.client.post(self.create_url , data, format='json')

        # We want to make sure we have one users in the database..
        self.assertEqual(User.objects.count(), 1)
        # And that we're returning a 200 created code.
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user_without_mandatory_fields(self):
        """
        Test creation without mandatory fields
        """
        data = {
            'email': 'foobar@example.com',
            'password': 'somepassword',
            'full_name': 'Atul Rai'
        }

        response = self.client.post(self.create_url , data, format='json')

        # We want to make sure we have 0 users in the database..
        self.assertEqual(User.objects.count(), 0)
        # And that we're returning a 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_all_fields(self):
        """
        Create users with mandatory as well as optional fields
        """
        data = {
            "email":"test3@user.com",
            "password":"SomePass123",
            "full_name": "FDFD DSJF",
            "phone": 3248948951,
            "pincode": 400025,
            "address": "jsaifdisdfd",
            "city": "mumbai",
            "state": "mah",
            "country": "ind"
        }

        response = self.client.post(self.create_url , data, format='json')

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user_with_invalid_pass_format(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        data = {
            "email":"test3@user.com",
            "password":"123",
            "full_name": "FDFD DSJF",
            "phone": 3248948951,
            "pincode": 400025,
            "address": "jsaifdisdfd",
            "city": "mumbai",
            "state": "mah",
            "country": "ind"
        }

        response = self.client.post(self.create_url , data, format='json')

        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class LoginTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
        'testuser@user.com',
        'Atul',
        'Rai',
        8879192322,
        'fkjdsf',
        'Mumbai',
        'Mah',
        'India',
        400025,
        '8PostUser'
        )
        self.login_url = reverse('login_api')


    def test_login_user(self):
        """
        Check login api with correct credentials
        """
        data = {
            'email': 'testuser@user.com',
            'password': '8PostUser'
        }

        response = self.client.post(self.login_url , data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_user_without_email_pass(self):
        """
        Check login without email or password
        """
        data = {
            'email': 'testuser@user.com'
        }

        response = self.client.post(self.login_url , data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        new_data = {
            'password': '8PostUser'
        }

        response = self.client.post(self.login_url , new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user_with_wrong_cred(self):
        """
        Test login with wrong crediantials
        """
        data = {
            'email': 'testuser@user.com',
            'password': '8PostUs'
        }

        response = self.client.post(self.login_url , data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)