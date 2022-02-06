"""Schema location serializers."""

from rest_framework import serializers

from apps.schema.serializers.base import ListItemSerializerBase


class ListItemSerializer(ListItemSerializerBase):
  """Location list item serializer."""

  area = serializers.SerializerMethodField()
  country = serializers.SerializerMethodField()
  street = serializers.SerializerMethodField()
  state = serializers.SerializerMethodField()
  town = serializers.SerializerMethodField()

  def get_area(self, obj):
    """Get area."""

    return obj.area

  def get_country(self, obj):
    """Get country."""

    return obj.country

  def get_street(self, obj):
    """Get street."""

    return obj.street

  def get_state(self, obj):
    """Get state."""

    return obj.state

  def get_town(self, obj):
    """Get town."""

    return obj.town
