"""Schema person serializers."""

from rest_framework import serializers


class PersonSerializer(serializers.Serializer):
  """Person serializer."""

  birthplace = serializers.SerializerMethodField()
  birth_year = serializers.SerializerMethodField()
  entry_list_url = serializers.SerializerMethodField()
  name = serializers.SerializerMethodField()
  object_update_url = serializers.SerializerMethodField()
  residence = serializers.SerializerMethodField()
  summary = serializers.SerializerMethodField()

  def get_birthplace(self, obj):
    """Get birthplace."""

    if not obj.birthplace:
      return

    return obj.birthplace.short_address

  def get_birth_year(self, obj):
    """Get birth year."""

    return obj.birth_year

  def get_entry_list_url(self, obj):
    """Get entry list URL."""

    return obj.entry_list_url

  def get_name(self, obj):
    """Get name."""

    return obj.name

  def get_object_update_url(self, obj):
    """Get object update URL."""

    return obj.object_update_url

  def get_residence(self, obj):
    """Get residence."""

    if not obj.residence:
      return

    return obj.residence.short_address

  def get_summary(self, obj):
    """Get summary."""

    return obj.summary
