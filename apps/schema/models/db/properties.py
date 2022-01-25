"""Neomodel custom properties."""

from django.conf import settings

import shortuuid
from neomodel.properties import UniqueIdProperty


class UIDProperty(UniqueIdProperty):
  """A custom unique identifier property populated with a randomly generated shortuuid value.
  """

  def __init__(self, **kwargs):
    super(UIDProperty, self).__init__(**kwargs)

    self.default = lambda: shortuuid.ShortUUID(
        alphabet=settings.SHORT_UUID_ALPHABET).random(length=settings.
                                                      SHORT_UUID_LENGTH)
