"""Schema entry serializers."""

from rest_framework import serializers

from apps.schema.serializers.base import (ListItemSerializerBase,
                                          TreeNodeSerializerBase)


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


class TreeNodeSerializer(TreeNodeSerializerBase):
  """Entry tree node serializer."""

  occurred = serializers.SerializerMethodField()
  summary = serializers.SerializerMethodField()

  def get_occurred(self, obj):
    """Get occurred."""

    return obj.occurred

  def get_summary(self, obj):
    """Get summary."""

    return obj.summary
