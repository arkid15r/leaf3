"""Tree models."""

from django.urls import reverse
from django.utils.translation import gettext as _

from neomodel import StringProperty

from apps.schema.models.base import TimestampModel, UIDModel


class Tree(TimestampModel, UIDModel):
  """Tree model."""

  creator_uid = StringProperty(label=_('Creator UID'))
  description = StringProperty(label=_('Description'), max_length=100)
  name = StringProperty(label=_('Name'), max_length=50, required=True)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    """Return object absolute URL."""

    return reverse('tree-manage', args=(self.uid,))

  class Meta:
    """Tree model meta."""

    app_label = 'schema'
    verbose_name = _('Tree')
    verbose_name_plural = _('Trees')
