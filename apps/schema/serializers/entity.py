"""Schema entity serializers."""

from rest_framework import serializers

from apps.schema.serializers.base import ListItemSerializerBase


class ListItemSerializer(ListItemSerializerBase):
  """Entity list item serializer."""

  name = serializers.SerializerMethodField()
  category = serializers.SerializerMethodField()
  location = serializers.SerializerMethodField()

  def get_category(self, obj):
    """Get category."""

    return obj.category

  def get_location(self, obj):
    """Get location."""

    return obj.location.short_address

  def get_name(self, obj):
    """Get name."""

    return obj.name
