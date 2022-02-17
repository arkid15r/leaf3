"""Entry models."""

from django.conf import settings
from django.template.defaultfilters import date
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from neomodel import (BooleanProperty, DateProperty, IntegerProperty,
                      StringProperty)

from apps.schema.models.base import TreeNodeModel
from apps.schema.models.entity import Entity
from apps.schema.models.entry_translation import EntryTranslation
from apps.schema.models.location import Location
from apps.schema.models.person import Person


class Entry(EntryTranslation, TreeNodeModel):
  """Entry model."""

  AVAILABLE_EVENT_CHOICES = tuple(
      (key, value) for key, value in EntryTranslation.AVAILABLE_EVENTS.items())
  EVENT_CHOICES = AVAILABLE_EVENT_CHOICES + tuple(
      (key, value) for key, value in EntryTranslation.AUTO_ENTRY_EVENTS.items())

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

    return self.summary

  @staticmethod
  def add_relative_birth(relative, event, person):
    """
      Add an entry about <person>'s birth to <relative>'s entry list.
    """

    entry = Entry.auto_create(relative, event, person_uid=person.uid)
    entry.person_uid = person.uid
    entry.location_uid = person.birth_place_uid
    entry.occurred = person.birth_date
    entry.occurred_year = person.birth_year

    entry.save()

  @staticmethod
  def add_relative_death(relative, event, person):
    """
      Add an entry about <person>'s death to <relative>'s entry list.
    """

    entry = Entry.auto_create(relative, event, person_uid=person.uid)
    entry.person_uid = person.uid
    entry.location_uid = person.death_place_uid
    entry.occurred = person.death_date
    entry.occurred_year = person.death_year

    entry.save()

  @staticmethod
  def auto_create(actor, event, **kwargs):
    """Get or create entry for one of the AUTO_ENTRY_EVENTS."""

    if event not in Entry.AUTO_ENTRY_EVENTS:
      raise ValueError(f'Unknown event: {event}')

    try:
      entry = Entry.nodes.get(actor_uid=actor.uid, event_uid=event, **kwargs)
    except Entry.DoesNotExist:
      entry = Entry(actor_uid=actor.uid,
                    auto_created=True,
                    event_uid=event,
                    tree_uid=actor.tree_uid,
                    **kwargs)

    if event == Entry.AUTO_EVENT_BORN:
      entry.position = -100
    # TODO(ark): death/burial events normally go last. There is a need to handle
    # cases when a soon to be a father dies before his child is born.
    elif event == Entry.AUTO_EVENT_DIED:
      if not entry.position:
        entry.position = 100
    elif event == Entry.AUTO_EVENT_BURIED:
      if not entry.position:
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

    return self.event_uid in (
        Entry.AUTO_EVENT_BORN,
        Entry.AUTO_EVENT_BURIED,
        Entry.AUTO_EVENT_DIED,
        Entry.AUTO_EVENT_HAD_CHILD,
        Entry.AUTO_EVENT_HAD_COUSIN,
        Entry.AUTO_EVENT_HAD_GRANDCHILD,
        Entry.AUTO_EVENT_HAD_GREAT_GRANDCHILD,
        Entry.AUTO_EVENT_HAD_NEPHEW_OR_NIECE,
        Entry.AUTO_EVENT_HAD_SIBLING,
    )

  @property
  def is_no_person_event(self):
    """Return True if entry should not have (an additional) person."""

    return self.event_uid in (
        Entry.AUTO_EVENT_BORN,
        Entry.AUTO_EVENT_DIED,
        Entry.AUTO_EVENT_BURIED,
    )

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

    date_format = 'j E Y, l'
    fields = []

    key = self.event_uid
    context = {}

    if self.occurred:
      key = f'{key}_date'
      context.update({
          'f': date(self.occurred, date_format).lower(),
          'm': date(self.occurred, date_format).lower(),
      })
    else:
      key = f'{key}_year'
      context.update({'f': self.occurred_year, 'm': self.occurred_year})

    # Special cases.
    if self.event_uid == self.AUTO_EVENT_BURIED:
      key = f'{self.event_uid}_date'
      if not self.occurred:
        key = self.event_uid
        context['f'] = ''
        context['m'] = ''

    gender = self.actor.gender
    if self.person:
      gender = self.person.gender

    fields.append(self.ENTRY_EVENT_DICT[key][gender].format(**context))

    if self.person:
      fields.append(self.person.long_name)

    if self.location:
      fields.append(str(self.location))

    text = ', '.join(fields)

    if self.text:
      text = f'{text}<br>{self.text}'

    return text

  class Meta:
    """Entry model meta."""

    app_label = 'schema'
    verbose_name = _('Entry')
    verbose_name_plural = _('Entries')
