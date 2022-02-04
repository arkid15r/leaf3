"""Schema person serializers."""

from rest_framework import serializers


class ListItemSerializer(serializers.Serializer):
  """Person list item serializer."""

  birthplace = serializers.SerializerMethodField()
  birth_year = serializers.SerializerMethodField()
  name = serializers.SerializerMethodField()
  residence = serializers.SerializerMethodField()
  summary = serializers.SerializerMethodField()
  uid = serializers.SerializerMethodField()

  def get_birthplace(self, obj):
    """Get birthplace."""

    if not obj.birthplace:
      return

    return obj.birthplace.short_address

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

  def get_uid(self, obj):
    """Get object UID."""

    return obj.uid


class TreeNodeSerializer(serializers.Serializer):
  """Person tree node serializer."""

  birth_year = serializers.SerializerMethodField()
  name = serializers.SerializerMethodField()
  uid = serializers.SerializerMethodField()

  def get_birth_year(self, obj):
    """Get birth year."""

    return obj.birth_year

  def get_name(self, obj):
    """Get name."""

    return obj.short_name

  def get_uid(self, obj):
    """Get UID."""

    return obj.uid
