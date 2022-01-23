"""Schema models base."""

from django.conf import settings

import shortuuid
from django_neomodel import DjangoNode
from neomodel import StringProperty


class ModelBase(DjangoNode):
  """Model base."""

  __abstract_node__ = True

  tree_uid = StringProperty(label='Tree UID', index=True)
  uid = StringProperty(label='UID', index=True, unique=True)

  def save(self):
    """Save ModelBase."""

    if not self.uid:
      self.uid = shortuuid.ShortUUID(
          alphabet=settings.SHORT_UUID_ALPHABET).random(
              length=settings.SHORT_UUID_LENGTH)

    return super().save()

  class Meta:
    """Model base meta."""

    abstract = True
    app_label = 'schema'
