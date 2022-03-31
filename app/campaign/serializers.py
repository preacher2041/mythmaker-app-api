from rest_framework import serializers

from core.models import Tag, World


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
