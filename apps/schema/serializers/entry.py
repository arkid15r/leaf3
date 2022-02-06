"""Schema entry serializers."""

from apps.schema.serializers.base import ListItemSerializerBase
from rest_framework import serializers


class ListItemSerializer(ListItemSerializerBase):
  """Entry list item serializer."""

  occurred = serializers.SerializerMethodField()
  summary = serializers.SerializerMethodField()

  def get_occurred(self, obj):
    """Get occurred."""

    return obj.occurred

  def get_summary(self, obj):
    """Get summary."""

    return obj.summary
