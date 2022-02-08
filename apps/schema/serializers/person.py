"""Schema person serializers."""

from rest_framework import serializers

from apps.schema.serializers.base import (ListItemSerializerBase,
                                          TreeNodeSerializerBase, UIDSerializer)


class ItemSerializer(UIDSerializer):
  """Person item serializer."""

  has_children = serializers.SerializerMethodField()
  has_parents = serializers.SerializerMethodField()
  has_timeline = serializers.SerializerMethodField()

  def get_has_children(self, obj):
    """Get has_children."""

    return obj.has_children

  def get_has_parents(self, obj):
    """Get has_parents."""

    return obj.has_parents

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
