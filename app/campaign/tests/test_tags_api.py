from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from campaign.serializers import TagSerializer


TAGS_URL = reverse('campaign:tag-list')

TEST_USER = {
    'email': 'test1@mythmaker.net',
    'username': 'mythMaker1',
    'first_name': 'Gary',
    'last_name': 'Gygax',
    'dob': '1974-01-01',
    'password': 'Test123!',
}

TEST_USER_2 = {
    'email': 'test2@mythmaker.net',
    'username': 'mythMaker2',
    'first_name': 'Gary',
    'last_name': 'Gygax',
    'dob': '1974-01-01',
    'password': 'Test123!',
}


class PublicTagsApiTests(TestCase):
    """Test the publicaly available tags API"""

    def setup(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving tags"""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test the authorised user tags API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(**TEST_USER)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """test retrieving tags"""

        Tag.objects.create(user=self.user, name='Humanoid')
        Tag.objects.create(user=self.user, name='Aberration')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that tags returned are for authenticated user"""

        user2 = get_user_model().objects.create_user(**TEST_USER_2)
        Tag.objects.create(user=user2, name='Celestial')
        tag = Tag.objects.create(user=self.user, name='Fiend')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
