"""Schema person serializers."""

from rest_framework import serializers

from apps.schema.serializers.base import (ListItemSerializerBase,
                                          TreeNodeSerializerBase, UIDSerializer)


class ItemSerializer(UIDSerializer):
  """Person item serializer."""

  has_child = serializers.SerializerMethodField()
  has_cousin = serializers.SerializerMethodField()
  has_cousin_nephew_or_niece = serializers.SerializerMethodField()
  has_nephew_or_niece = serializers.SerializerMethodField()
  has_parent = serializers.SerializerMethodField()
  has_timeline = serializers.SerializerMethodField()

  def get_has_child(self, obj):
    """Get has_child."""

    return obj.has_child

  def get_has_cousin(self, obj):
    """Get has_cousin."""

    return obj.has_cousin

  def get_has_cousin_nephew_or_niece(self, obj):
    """Get has_cousin_nephew_or_niece."""

    return obj.has_cousin_nephew_or_niece

  def get_has_nephew_or_niece(self, obj):
    """Get has_nephew_or_niece."""

    return obj.has_nephew_or_niece

  def get_has_parent(self, obj):
    """Get has_parent."""

    return obj.has_parent

  def get_has_timeline(self, obj):
    """Get has_timeline."""

    return obj.has_timeline


class ListItemSerializer(ListItemSerializerBase):
  """Person list item serializer."""

  birth_place = serializers.SerializerMethodField()
  birth_year = serializers.SerializerMethodField()
  name = serializers.SerializerMethodField()
  residence = serializers.SerializerMethodField()
  summary = serializers.SerializerMethodField()

  def get_birth_place(self, obj):
    """Get birthplace."""

    if not obj.birth_place:
      return

    return obj.birth_place.short_address

  def get_birth_year(self, obj):
    """Get birth year."""

    return obj.birth_year

  def get_name(self, obj):
    """Get name."""

    return obj.name

  def get_residence(self, obj):
    """Get residence."""

    if not obj.residence:
      return

    return obj.residence.short_address

  def get_summary(self, obj):
    """Get summary."""

    return obj.summary


class TreeNodeSerializer(TreeNodeSerializerBase):
  """Person tree node serializer."""

  birth_year = serializers.SerializerMethodField()
  name = serializers.SerializerMethodField()

  def get_birth_year(self, obj):
    """Get birth year."""

    return obj.birth_year

  def get_name(self, obj):
    """Get name."""

    return obj.short_name
