"""Schema entry serializers."""

from django.template.defaultfilters import date

from rest_framework import serializers

from apps.schema.serializers.base import ListItemSerializerBase, UIDSerializer


class ItemSerializer(UIDSerializer):
  """Entry item serializer."""

  occurred = serializers.SerializerMethodField()
  occurred_year = serializers.SerializerMethodField()
  text = serializers.SerializerMethodField()

  def get_occurred(self, obj):
    """Get occurred."""

    return date(obj.occurred)

  def get_occurred_year(self, obj):
    """Get occurred year."""

    return obj.occurred_year

  def get_text(self, obj):
    """Get text."""

    return obj.summary


class ListItemSerializer(ListItemSerializerBase):
  """Entry list item serializer."""

  occurred = serializers.SerializerMethodField()
  text = serializers.SerializerMethodField()

  def get_occurred(self, obj):
    """Get occurred."""

    return obj.occurred or obj.occurred_year

  def get_text(self, obj):
    """Get text."""

    return obj.summary
