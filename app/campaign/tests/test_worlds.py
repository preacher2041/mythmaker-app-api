from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import World

from campaign.serializers import WorldSerializer


WORLDS_URL = reverse('campaign:world-list')

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


class PublicWorldsApiTests(TestCase):
    """test the publicaly available worlds API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is rewuired to access endpoint"""
        res = self.client.get(WORLDS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateWorldsApiTests(TestCase):
    """Test the private worlds API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(**TEST_USER)
        self.client.force_authenticate(self.user)

    def test_retrieve_worlds_list(self):
        """Test retrieving a list of worlds"""
        World.objects.create(user=self.user, name='World1')
        World.objects.create(user=self.user, name='World2')

        res = self.client.get(WORLDS_URL)

        worlds = World.objects.all().order_by('-name')
        serializer = WorldSerializer(worlds, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_world_limited_to_user(self):
        """Test that worlds for the authenticated user are returned"""
        user2 = get_user_model().objects.create_user(**TEST_USER_2)

        World.objects.create(user=user2, name='World1')

        world = World.objects.create(user=self.user, name='World2')

        res = self.client.get(WORLDS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], world.name)

    def test_create_worlds_successful(self):
        """Test create a new world"""
        payload = {'name': 'New World'}
        self.client.post(WORLDS_URL, payload)

        exists = World.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_world_invalid(self):
        """Test creating invalid world fails"""
        payload = {'name': ''}
        res = self.client.post(WORLDS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
