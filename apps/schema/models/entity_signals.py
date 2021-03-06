"""Entity signals/handlers."""

from apps.schema.models.location import Location


def post_save(sender, instance, created, **kwargs):
  """Entity post save handler."""

  # Location.
  instance.location_rel.disconnect_all()
  if instance.location_uid:
    instance.location_rel.connect(Location.nodes.get(uid=instance.location_uid))
