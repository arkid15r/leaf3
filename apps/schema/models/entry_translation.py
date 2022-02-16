"""Schema entry translation.
   Ended up with a quite cumbersome multi-dict structure in order to satisfy
   ru i18n gender/pluralization grammar requirements.
"""

from django.utils.translation import gettext_lazy as _

from apps.schema.models.person import Person


class EntryTranslation:
  """Entry translation class."""

  EVENT_STARTED = 'started'
  EVENT_CHANGED = 'changed'
  EVENT_ENDED = 'ended'

  AVAILABLE_EVENTS = {
      EVENT_STARTED: _('Started'),
      EVENT_CHANGED: _('Changed'),
      EVENT_ENDED: _('Ended'),
  }

  AUTO_EVENT_BORN = 'born'
  AUTO_EVENT_BURIED = 'buried'
  AUTO_EVENT_DIED = 'died'

  AUTO_EVENT_HAD_CHILD = 'had_child'
  AUTO_EVENT_HAD_COUSIN = 'had_cousin'
  AUTO_EVENT_HAD_GRANDCHILD = 'had_grandchild'
  AUTO_EVENT_HAD_GREAT_GRANDCHILD = 'had_great_grandchild'
  AUTO_EVENT_HAD_GREAT_GREAT_GRANDCHILD = 'had_great_great_grandchild'
  AUTO_EVENT_HAD_NEPHEW_OR_NIECE = 'had_nephew_or_niece'
  AUTO_EVENT_HAD_SIBLING = 'had_sibling'

  AUTO_ENTRY_EVENTS = {
      AUTO_EVENT_BORN: _('Born'),
      AUTO_EVENT_BURIED: _('Buried'),
      AUTO_EVENT_DIED: _('Died'),
      AUTO_EVENT_HAD_CHILD: _('Had a child'),
      AUTO_EVENT_HAD_COUSIN: _('Had a cousin'),
      AUTO_EVENT_HAD_GRANDCHILD: _('Had a grandchild'),
      AUTO_EVENT_HAD_GREAT_GRANDCHILD: _('Had a great grandchild'),
      AUTO_EVENT_HAD_GREAT_GREAT_GRANDCHILD: _('Had a great-great grandchild'),
      AUTO_EVENT_HAD_NEPHEW_OR_NIECE: _('Had a nephew or a niece'),
      AUTO_EVENT_HAD_SIBLING: _('Had a sibling'),
  }

  AUTO_EVENT_HAD_CHILD_TEMPLATES = {
      Person.FEMALE: _('A birth of a daughter'),
      Person.MALE: _('A birth of a son'),
  }
  AUTO_EVENT_HAD_COUSIN_TEMPLATES = {
      Person.FEMALE: _('A birth of a cousin sister'),
      Person.MALE: _('A birth of a cousin brother'),
  }
  AUTO_EVENT_HAD_GRANDCHILD_TEMPLATES = {
      Person.FEMALE: _('A birth of a granddaughter'),
      Person.MALE: _('A birth of a grandson'),
  }
  AUTO_EVENT_HAD_GREAT_GRANDCHILD_TEMPLATES = {
      Person.FEMALE: _('A birth of a great granddaughter'),
      Person.MALE: _('A birth of a great grandson'),
  }
  AUTO_EVENT_HAD_GREAT_GREAT_GRANDCHILD_TEMPLATES = {
      Person.FEMALE: _('A birth of a great-great granddaughter'),
      Person.MALE: _('A birth of a great-great grandson'),
  }
  AUTO_EVENT_HAD_NEPHEW_OR_NIECE_TEMPLATES = {
      Person.FEMALE: _('A birth of a niece'),
      Person.MALE: _('A birth of a nephew'),
  }
  AUTO_EVENT_HAD_SIBLING_TEMPLATES = {
      Person.FEMALE: _('A birth of a sister'),
      Person.MALE: _('A birth of a brother'),
  }

  ENTRY_EVENTS_TEMPLATES = {
      f'{AUTO_EVENT_BORN}_date': {
          Person.FEMALE: _('Was born on {f}'),
          Person.MALE: _('Was born on {m}'),
      },
      f'{AUTO_EVENT_BORN}_year': {
          Person.FEMALE: _('Was born in {f}'),
          Person.MALE: _('Was born in {m}'),
      },
      f'{AUTO_EVENT_BURIED}': {
          Person.FEMALE: _('Buried{f}'),
          Person.MALE: _('Buried{m}'),
      },
      f'{AUTO_EVENT_BURIED}_date': {
          Person.FEMALE: _('Buried on {f}'),
          Person.MALE: _('Buried on {m}'),
      },
      f'{AUTO_EVENT_DIED}_date': {
          Person.FEMALE: _('Died on {f}'),
          Person.MALE: _('Died on {m}'),
      },
      f'{AUTO_EVENT_DIED}_year': {
          Person.FEMALE: _('Died in {f}'),
          Person.MALE: _('Died in {m}'),
      },
      f'{AUTO_EVENT_HAD_CHILD}_date': AUTO_EVENT_HAD_CHILD_TEMPLATES,
      f'{AUTO_EVENT_HAD_CHILD}_year': AUTO_EVENT_HAD_CHILD_TEMPLATES,
      f'{AUTO_EVENT_HAD_COUSIN}_date': AUTO_EVENT_HAD_COUSIN_TEMPLATES,
      f'{AUTO_EVENT_HAD_COUSIN}_year': AUTO_EVENT_HAD_COUSIN_TEMPLATES,
      f'{AUTO_EVENT_HAD_GRANDCHILD}_date': AUTO_EVENT_HAD_GRANDCHILD_TEMPLATES,
      f'{AUTO_EVENT_HAD_GRANDCHILD}_year': AUTO_EVENT_HAD_GRANDCHILD_TEMPLATES,

      f'{AUTO_EVENT_HAD_GREAT_GRANDCHILD}_date': (
          AUTO_EVENT_HAD_GREAT_GRANDCHILD_TEMPLATES),
      f'{AUTO_EVENT_HAD_GREAT_GRANDCHILD}_year': (
          AUTO_EVENT_HAD_GREAT_GRANDCHILD_TEMPLATES),

      f'{AUTO_EVENT_HAD_GREAT_GREAT_GRANDCHILD}_date': (
          AUTO_EVENT_HAD_GREAT_GREAT_GRANDCHILD_TEMPLATES),
      f'{AUTO_EVENT_HAD_GREAT_GREAT_GRANDCHILD}_year': (
          AUTO_EVENT_HAD_GREAT_GREAT_GRANDCHILD_TEMPLATES),

      f'{AUTO_EVENT_HAD_NEPHEW_OR_NIECE}_date': AUTO_EVENT_HAD_NEPHEW_OR_NIECE_TEMPLATES,
      f'{AUTO_EVENT_HAD_NEPHEW_OR_NIECE}_year': AUTO_EVENT_HAD_NEPHEW_OR_NIECE_TEMPLATES,

      f'{AUTO_EVENT_HAD_SIBLING}_date': AUTO_EVENT_HAD_SIBLING_TEMPLATES,
      f'{AUTO_EVENT_HAD_SIBLING}_year': AUTO_EVENT_HAD_SIBLING_TEMPLATES,
      f'{EVENT_STARTED}_date': {
          Person.FEMALE: AVAILABLE_EVENTS[EVENT_STARTED],
          Person.MALE: AVAILABLE_EVENTS[EVENT_STARTED]
      },
      f'{EVENT_STARTED}_year': {
          Person.FEMALE: AVAILABLE_EVENTS[EVENT_STARTED],
          Person.MALE: AVAILABLE_EVENTS[EVENT_STARTED]
      },
      f'{EVENT_CHANGED}_date': {
          Person.FEMALE: AVAILABLE_EVENTS[EVENT_CHANGED],
          Person.MALE: AVAILABLE_EVENTS[EVENT_CHANGED]
      },
      f'{EVENT_CHANGED}_year': {
          Person.FEMALE: AVAILABLE_EVENTS[EVENT_CHANGED],
          Person.MALE: AVAILABLE_EVENTS[EVENT_CHANGED]
      },
  }
