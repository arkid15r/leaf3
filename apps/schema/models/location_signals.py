"""Location signals/handlers."""


def post_save(sender, instance, created, **kwargs):
  """Location post save handler."""

  location = instance

  location.parent_rel.disconnect_all()
  if location.parent:
    location.parent_rel.connect(location.parent)
