from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Campaign, Tag, World

from campaign import serializers


class BaseCampaignAttrViewset(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    """Base viewset for user owned campaign attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return object for current authenticated user only"""

        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class CampaignViewSet(viewsets.ModelViewSet):
    """Manage campaigns in the database"""
    serializer_class = serializers.CampaignSerializer
    queryset = Campaign.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve campaigns for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')


class TagViewSet(BaseCampaignAttrViewset):
    """Manage tags in the database"""

    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class WorldViewSet(BaseCampaignAttrViewset):
    """Manage worlds in the database"""

    queryset = World.objects.all()
    serializer_class = serializers.WorldSerializer
