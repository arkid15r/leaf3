"""Entry models."""

from django.conf import settings
from django.template.defaultfilters import date, safe
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from neomodel import (BooleanProperty, DateProperty, IntegerProperty,
                      StringProperty)

from apps.schema.models.base import TreeNodeModel
from apps.schema.models.entity import Entity
from apps.schema.models.location import Location
from apps.schema.models.person import Person


class Entry(TreeNodeModel):
  """Entry model."""

  AUTO_ENTRY_EVENT_BORN = 'born'
  AUTO_ENTRY_EVENT_BURIED = 'buried'
  AUTO_ENTRY_EVENT_DIED = 'died'
  AUTO_ENTRY_EVENT_GAVE_BIRTH = 'gave_birth'

  AUTO_ENTRY_EVENTS = {
      AUTO_ENTRY_EVENT_BORN: _('Born'),
      AUTO_ENTRY_EVENT_BURIED: _('Buried'),
      AUTO_ENTRY_EVENT_DIED: _('Died'),
      AUTO_ENTRY_EVENT_GAVE_BIRTH: _('Gave birth')
  }

  EVENT_STARTED = 'started'
  EVENT_CHANGED = 'changed'
  EVENT_ENDED = 'ended'

  AVAILABLE_EVENTS = {
      EVENT_STARTED: _('Started'),
      EVENT_CHANGED: _('Changed'),
      EVENT_ENDED: _('Ended'),
  }

  AVAILABLE_EVENT_CHOICES = tuple(
      (key, value) for key, value in AVAILABLE_EVENTS.items())

  EVENT_CHOICES = AVAILABLE_EVENT_CHOICES + tuple(
      (key, value) for key, value in AUTO_ENTRY_EVENTS.items())

  actor_uid = StringProperty(max_length=settings.SHORT_UUID_LENGTH)
  auto_created = BooleanProperty(default=False, index=True)
  event_uid = StringProperty(choices=EVENT_CHOICES, required=True)
  entity_uid = StringProperty(max_length=settings.SHORT_UUID_LENGTH)
  location_uid = StringProperty(max_length=settings.SHORT_UUID_LENGTH)
  occurred = DateProperty(label=_('Date'), index=True)
  occurred_year = StringProperty(label=_('Year'), index=True)
  person_uid = StringProperty(max_length=settings.SHORT_UUID_LENGTH)
  position = IntegerProperty(default=0, index=True)
  text = StringProperty(label=_('Text'), max_length=1000)

  def __str__(self):
    """Entity str()."""

    return str(self.actor)

  @staticmethod
  def auto_create(actor, event):
    """Get or create entry for one of the AUTO_ENTRY_EVENTS."""

    if event not in Entry.AUTO_ENTRY_EVENTS:
      raise ValueError(f'Unknown event: {event}')

    try:
      entry = Entry.nodes.get(actor_uid=actor.uid, event_uid=event)
    except Entry.DoesNotExist:
      entry = Entry(actor_uid=actor.uid,
                    auto_created=True,
                    event_uid=event,
                    tree_uid=actor.tree_uid)

    if event == Entry.AUTO_ENTRY_EVENT_BORN:
      entry.position = -100
    elif event == Entry.AUTO_ENTRY_EVENT_DIED:
      entry.position = 100
    elif event == Entry.AUTO_ENTRY_EVENT_BURIED:
      entry.position = 110
    entry.save()

    return entry

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
  def event(self):
    """Return entry event."""

    events = self.AUTO_ENTRY_EVENTS
    events.update(self.AVAILABLE_EVENTS)

    return events[self.event_uid]

  @property
  def is_auto_created(self):
    """Return True if entry is automatically created."""

    return self.event_uid in Entry.AUTO_ENTRY_EVENTS

  @property
  def is_no_entity_event(self):
    """Return True if entry should not have an entity."""

    return self.event_uid in (Entry.AUTO_ENTRY_EVENT_BORN,
                              Entry.AUTO_ENTRY_EVENT_DIED,
                              Entry.AUTO_ENTRY_EVENT_BURIED)

  @property
  def is_no_person_event(self):
    """Return True if entry should not have a person."""

    return self.event_uid in (Entry.AUTO_ENTRY_EVENT_BORN,
                              Entry.AUTO_ENTRY_EVENT_DIED,
                              Entry.AUTO_ENTRY_EVENT_BURIED)

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

    fields = []
    if self.event_uid == self.AUTO_ENTRY_EVENT_BORN:
      if self.occurred:
        dob = date(self.occurred)
        if self.actor.is_female:
          template = _('Born {f}')
        else:
          template = _('Born {m}')
      else:
        dob = self.occurred_year
        if self.actor.is_female:
          template = _('Born in {f}')
        else:
          template = _('Born in {m}')

      fields.append(template.format(f=dob, m=dob))

    elif self.event_uid == self.AUTO_ENTRY_EVENT_DIED:
      if self.occurred:
        dod = date(self.occurred)
        if self.actor.is_female:
          template = _('Died {f}')
        else:
          template = _('Died {m}')
      else:
        dod = self.occurred_year
        if self.actor.is_female:
          template = _('Died in {f}')
        else:
          template = _('Died in {m}')

      fields.append(template.format(f=dod, m=dod))

    if self.location_uid:
      fields.append(str(self.location))

    if self.person_uid:
      fields.append(str(self.person))

    text = ', '.join(fields)

    if self.text:
      text = safe(f'{text}<br>{self.text}')

    return text

  class Meta:
    """Entry model meta."""

    app_label = 'schema'
    verbose_name = _('Entry')
    verbose_name_plural = _('Entries')
