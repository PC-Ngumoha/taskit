from authentication.models import User
from rest_framework.test import APITestCase


class TestUserModel(APITestCase):

    def test_should_not_create_user_if_email_not_provided(self):
        payload = {"password": "password123#"}
        error_msg = "The 'email' field must be set to a valid email"
        with self.assertRaisesMessage(ValueError, error_msg):
            User.objects.create_user(**payload)

    def test_create_regular_user(self):
        payload = {"email": "test@example.com", "password": "testing123#"}
        user = User.objects.create_user(**payload)
        self.assertEqual(user.email, payload.get("email"))
        self.assertFalse(user.is_staff)

    def test_create_super_user(self):
        payload = {"email": "test@example.com", "password": "testing123#"}
        superuser = User.objects.create_superuser(**payload)
        self.assertTrue(superuser.is_staff)
