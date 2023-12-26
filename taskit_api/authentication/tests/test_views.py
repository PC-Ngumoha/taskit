from authentication.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestUserRegisterView(APITestCase):

    def test_user_registered_and_created_successfully(self):
        prev_db_count = User.objects.all().count()
        payload = {"email": "test@example.com", "password": "testing123#"}
        response = self.client.post(reverse("user-register"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), prev_db_count + 1)
        self.assertEqual(response.data.get("email"), payload.get("email"))

    def test_should_not_register_with_password_less_than_8_characters(self):
        payload = {"email": "test@example.com", "password": "test"}
        response = self.client.post(reverse("user-register"), payload)
        actual_message = response.data.get("password")[0]
        expected_message = "Ensure this field has at least 8 characters."
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(actual_message, expected_message)


class TestUserLoginView(APITestCase):

    def test_response_should_contain_JWT_token(self):
        payload = {"email": "test@example.com", "password": "testing123#"}
        self.client.post(reverse("user-register"), payload)
        response = self.client.post(reverse("user-login"), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get("token"))
