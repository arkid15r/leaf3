"""Schema location serializers."""

from rest_framework import serializers

from apps.schema.serializers.base import ListItemSerializerBase


class ListItemSerializer(ListItemSerializerBase):
  """Location list item serializer."""

  summary = serializers.SerializerMethodField()

  def get_summary(self, obj):
    """Get name."""

    return obj.full_address
