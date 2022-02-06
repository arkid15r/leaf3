"""Entry models."""

from django.conf import settings
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from neomodel import DateProperty, StringProperty

from apps.schema.models.base import TreeNodeModel
from apps.schema.models.entity import Entity
from apps.schema.models.location import Location
from apps.schema.models.person import Person


class Entry(TreeNodeModel):
  """Entry model."""

  EVENT_BEGIN = 'begin'
  EVENT_CHANGE = 'change'
  EVENT_END = 'end'

  EVENT_CHOICES = {
      EVENT_BEGIN: _('Begin'),
      EVENT_CHANGE: _('Change'),
      EVENT_END: _('End'),
  }

  EVENTS = tuple((key, value) for key, value in EVENT_CHOICES.items())

  event_uid = StringProperty(choices=EVENTS, required=True)
  actor_uid = StringProperty(max_length=settings.SHORT_UUID_LENGTH)
  entity_uid = StringProperty(max_length=settings.SHORT_UUID_LENGTH)
  location_uid = StringProperty(max_length=settings.SHORT_UUID_LENGTH)
  occurred = DateProperty(label=_('Date'), required=True, index=True)
  person_uid = StringProperty(max_length=settings.SHORT_UUID_LENGTH)
  text = StringProperty(label=_('Text'), max_length=1000)

  def __str__(self):
    """Entity str()."""

    return str(self.actor)

  @property
  def action(self):
    """Return entry action."""

    for key, title in self.ACTIONS:
      if key == self.EVENT_uid:
        return title

  @property
  def actor(self):
    """Return entry actor."""

    try:
      return Person.nodes.get(uid=self.actor_uid)
    except Person.DoesNotExist:
      pass

  @property
  def entity(self):
    """Return entry entity."""

    try:
      return Entity.nodes.get(uid=self.entity_uid)
    except Entity.DoesNotExist:
      pass

  @property
  def location(self):
    """Return entry location."""

    try:
      return Location.nodes.get(uid=self.location_uid)
    except Location.DoesNotExist:
      pass

  @property
  def object_delete_url(self):
    """Return entry delete URL."""

    return reverse_lazy('entry-delete',
                        args=(self.tree_uid, self.actor_uid, self.uid))

  @property
  def object_read_url(self):
    """Return entry read URL."""

    return reverse_lazy('entry', args=(self.tree_uid, self.actor_uid, self.uid))

  @property
  def object_update_url(self):
    """Return entry update URL."""

    return reverse_lazy('entry-update',
                        args=(self.tree_uid, self.actor_uid, self.uid))

  @property
  def person(self):
    """Return entry person."""

    try:
      return Person.nodes.get(uid=self.person_uid)
    except Person.DoesNotExist:
      pass

  @property
  def summary(self):
    """Return entry summary."""

    fields = [str(self.EVENT_CHOICES[self.event_uid])]

    if self.entity_uid:
      fields.append(str(self.entity))

    if self.location_uid:
      fields.append(str(self.location))

    if self.person_uid:
      fields.append(str(self.person))

    return ' '.join(fields)

  class Meta:
    """Entry model meta."""

    app_label = 'schema'
    verbose_name = _('Entry')
    verbose_name_plural = _('Entries')
