"""Schema serializers base."""

from rest_framework import serializers


class UIDSerializer(serializers.Serializer):
  """UID serializer base."""

  uid = serializers.SerializerMethodField()

  def get_uid(self, obj):
    """Get object UID."""

    return obj.uid


class ListItemSerializerBase(UIDSerializer):
  """List item serializer base."""


class TreeNodeSerializerBase(UIDSerializer):
  """Tree node serializer base."""
