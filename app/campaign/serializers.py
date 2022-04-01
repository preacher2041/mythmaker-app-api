from rest_framework import serializers

from core.models import Campaign, Tag, World


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class WorldSerializer(serializers.ModelSerializer):
    """Serializer for world objects"""

    class Meta:
        model = World
        fields = ('id', 'name')
        read_only_fields = ('id',)


class CampaignSerializer(serializers.ModelSerializer):
    """Serializer for campiagn objects"""

    class Meta:
        model = Campaign
        fields = ('id', 'name',)
        read_only_fields = ('id',)
