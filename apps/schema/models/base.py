"""Schema models base."""

from datetime import datetime

from django.conf import settings
from django.utils.translation import gettext_lazy as _

import pytz
from django_neomodel import DjangoNode
from neomodel import DateTimeProperty, StringProperty

from apps.schema.models.properties import UIDProperty


class TimestampModel(DjangoNode):
  """Timestamp model."""

  __abstract_node__ = True

  created = DateTimeProperty(label=_('Created date'), default_now=True)
  updated = DateTimeProperty(label=_('Last updated date'))

  def save(self):
    self.updated = datetime.utcnow().replace(tzinfo=pytz.utc)

    return super().save()


class UIDModel(DjangoNode):
  """Model with an UID field."""

  __abstract_node__ = True

  uid = UIDProperty(label='UID', max_length=settings.SHORT_UUID_LENGTH)


class TreeNodeModel(TimestampModel, UIDModel):
  """Tree node model."""

  __abstract_node__ = True

  tree_uid = StringProperty(label=_('Tree UID'), index=True, max_length=settings.SHORT_UUID_LENGTH)
