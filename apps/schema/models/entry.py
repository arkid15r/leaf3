"""Entry models."""

from django.conf import settings
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from neomodel import DateProperty, StringProperty

from apps.schema.models.base import TreeNodeModel
from apps.schema.models.person import Person


class Entry(TreeNodeModel):
  """Entry model."""

  ACTION_GAVE_BIRTH = 'GAVE_BIRTH'
  ACTION_MARRIED = 'MARRIED'

  ACTIONS = (
      (ACTION_GAVE_BIRTH, _('Gave birth')),
      (ACTION_MARRIED, _('Married')),
  )

  action_uid = StringProperty(choices=ACTIONS, required=True)
  actor_uid = StringProperty(max_length=settings.SHORT_UUID_LENGTH,
                             required=True)
  entity_uid = StringProperty(max_length=settings.SHORT_UUID_LENGTH)
  location_uid = StringProperty(max_length=settings.SHORT_UUID_LENGTH)
  occurred = DateProperty(label=_('Date'), required=True, index=True)
  person_uid = StringProperty(max_length=settings.SHORT_UUID_LENGTH)

  def __str__(self):
    """Entity str()."""

    return str(self.actor)

  @property
  def action(self):
    """Return entry action."""

    for key, title in self.ACTIONS:
      if key == self.action_uid:
        return title

  @property
  def actor(self):
    """Return entity actor."""

    try:
      return Person.nodes.get(uid=self.actor_uid)
    except Person.DoesNotExist:
      pass

  def get_absolute_url(self):
    """Return entry absolute URL."""

    return reverse_lazy('entry', args=(self.tree_uid, self.uid))

  class Meta:
    """Entry model meta."""

    app_label = 'schema'
    verbose_name = _('Entry')
    verbose_name_plural = _('Entries')
