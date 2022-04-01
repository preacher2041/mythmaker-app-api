from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Campaign

from campaign.serializers import CampaignSerializer


CAMPAIGN_URL = reverse('campaign:campaign-list')
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


def sample_campaign(user, **params):
    """Create a return a sample campaign"""
    defaults = {
        'name': 'Sample Campaign'
    }
    defaults.update(params)

    return Campaign.objects.create(user=user, **defaults)


class PublicCampaignApiTests(TestCase):
    """Test unauthenticated campaign API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(CAMPAIGN_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCampaignApiTests(TestCase):
    """Test authenticated campaign API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(**TEST_USER)
        self.client.force_authenticate(self.user)

    def test_retrieve_campaigns(self):
        """Test retrieving a list of campaigns"""
        sample_campaign(user=self.user)
        sample_campaign(user=self.user)

        res = self.client.get(CAMPAIGN_URL)

        campaigns = Campaign.objects.all().order_by('-id')
        serializer = CampaignSerializer(campaigns, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_campaigns_limited_to_user(self):
        """Test retrieving campaigns for user"""
        user2 = get_user_model().objects.create_user(**TEST_USER_2)
        sample_campaign(user2)
        sample_campaign(self.user)

        res = self.client.get(CAMPAIGN_URL)

        campaigns = Campaign.objects.filter(user=self.user)
        serializer = CampaignSerializer(campaigns, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)
