from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


TEST_USER = {
    'email': 'test@mythmaker.net',
    'username': 'mythMaker1',
    'first_name': 'Gary',
    'last_name': 'Gygax',
    'dob': '1974-01-01',
    'password': 'Test123!',
}


def sample_user():
    """Create a sample user"""
    return get_user_model().objects.create_user(**TEST_USER)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""

        email = 'test@gmail.com'
        password = 'Testpass123'
        first_name = 'Joe'
        last_name = 'bloggs'
        dob = '1984-06-18'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            dob=dob,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""

        email = 'test@GMAIL.COM'
        password = 'Testpass123'
        first_name = 'Joe'
        last_name = 'bloggs'
        dob = '1984-06-18'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            dob=dob,
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""

        with self.assertRaises(ValueError):
            email = ''
            password = 'Testpass123'
            first_name = 'Joe'
            last_name = 'bloggs'
            dob = '1984-06-18'
            get_user_model().objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                dob=dob,
            )

    def test_create_new_super_user(self):
        """Test creating a new super user"""

        email = 'test@gmail.com'
        password = 'Testpass123'
        first_name = 'Joe'
        last_name = 'bloggs'
        dob = '1984-06-18'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            dob=dob,
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""

        tag = models.Tag.objects.create(
            user=sample_user(),
            name='BBEG'
        )

        self.assertEqual(str(tag), tag.name)
