"""Schema entry translation.

   Ended up with a quite cumbersome structure in order to satisfy
   Russian i18n gender/pluralization grammar requirements.
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

  # Birth.
  AUTO_EVENT_HAD_AUNT_OR_UNCLE = 'had_aunt_or_uncle'
  AUTO_EVENT_HAD_CHILD = 'had_child'
  AUTO_EVENT_HAD_COUSIN = 'had_cousin'
  AUTO_EVENT_HAD_GRANDCHILD = 'had_grandchild'
  AUTO_EVENT_HAD_GREAT_GRANDCHILD = 'had_great_grandchild'
  AUTO_EVENT_HAD_GREAT_GREAT_GRANDCHILD = 'had_great_great_grandchild'
  AUTO_EVENT_HAD_NEPHEW_OR_NIECE = 'had_nephew_or_niece'
  AUTO_EVENT_HAD_SIBLING = 'had_sibling'

  # Death.
  AUTO_EVENT_LOST_AUNT_OR_UNCLE = 'lost_aunt_or_uncle'
  AUTO_EVENT_LOST_CHILD = 'lost_child'
  AUTO_EVENT_LOST_COUSIN = 'lost_cousin'
  AUTO_EVENT_LOST_GRANDCHILD = 'lost_grandchild'
  AUTO_EVENT_LOST_GRANDPARENT = 'lost_grandparent'
  AUTO_EVENT_LOST_GREAT_GRANDCHILD = 'lost_great_grandchild'
  AUTO_EVENT_LOST_GREAT_GRANDPARENT = 'lost_great_grandparent'
  AUTO_EVENT_LOST_GREAT_GREAT_GRANDCHILD = 'lost_great_great_grandchild'
  AUTO_EVENT_LOST_GREAT_GREAT_GRANDPARENT = 'lost_great_great_grandparent'
  AUTO_EVENT_LOST_NEPHEW_OR_NIECE = 'lost_nephew_or_niece'
  AUTO_EVENT_LOST_SIBLING = 'lost_sibling'

  AUTO_ENTRY_EVENTS = {
      AUTO_EVENT_BORN: _('Born'),
      AUTO_EVENT_BURIED: _('Buried'),
      AUTO_EVENT_DIED: _('Died'),

      # Birth.
      AUTO_EVENT_HAD_AUNT_OR_UNCLE: _('Had an aunt or an uncle.'),
      AUTO_EVENT_HAD_CHILD: _('Had a child'),
      AUTO_EVENT_HAD_COUSIN: _('Had a cousin'),
      AUTO_EVENT_HAD_GRANDCHILD: _('Had a grandchild'),
      AUTO_EVENT_HAD_GREAT_GRANDCHILD: _('Had a great grandchild'),
      AUTO_EVENT_HAD_GREAT_GREAT_GRANDCHILD: _('Had a great-great grandchild'),
      AUTO_EVENT_HAD_NEPHEW_OR_NIECE: _('Had a nephew or a niece'),
      AUTO_EVENT_HAD_SIBLING: _('Had a sibling'),

      # Death.
      AUTO_EVENT_LOST_AUNT_OR_UNCLE: _('Lost an aunt or an uncle.'),
      AUTO_EVENT_LOST_CHILD: _('Lost a child'),
      AUTO_EVENT_LOST_COUSIN: _('Lost a cousin'),
      AUTO_EVENT_LOST_GRANDCHILD: _('Lost a grandchild'),
      AUTO_EVENT_LOST_GRANDPARENT: _('Lost a grandparent'),
      AUTO_EVENT_LOST_GREAT_GRANDCHILD: _('Lost a great grandchild'),
      AUTO_EVENT_LOST_GREAT_GRANDPARENT: _('Lost a great grandparent'),
      AUTO_EVENT_LOST_GREAT_GREAT_GRANDCHILD: _(
          'Lost a great-great grandchild'),
      AUTO_EVENT_LOST_GREAT_GREAT_GRANDPARENT: _(
          'Lost a great-great grandparent'),
      AUTO_EVENT_LOST_NEPHEW_OR_NIECE: _('Lost a nephew or a niece'),
      AUTO_EVENT_LOST_SIBLING: _('Lost a sibling'),
  }

  # Gender based translation.
  # Birth.
  AUTO_EVENT_HAD_AUNT_OR_UNCLE_DICT = {
      Person.FEMALE: _('A birth of an aunt'),
      Person.MALE: _('A birth of an uncle'),
  }
  AUTO_EVENT_HAD_CHILD_DICT = {
      Person.FEMALE: _('A birth of a daughter'),
      Person.MALE: _('A birth of a son'),
  }
  AUTO_EVENT_HAD_COUSIN_DICT = {
      Person.FEMALE: _('A birth of a cousin sister'),
      Person.MALE: _('A birth of a cousin brother'),
  }
  AUTO_EVENT_HAD_GRANDCHILD_DICT = {
      Person.FEMALE: _('A birth of a granddaughter'),
      Person.MALE: _('A birth of a grandson'),
  }
  AUTO_EVENT_HAD_GREAT_GRANDCHILD_DICT = {
      Person.FEMALE: _('A birth of a great granddaughter'),
      Person.MALE: _('A birth of a great grandson'),
  }
  AUTO_EVENT_HAD_GREAT_GREAT_GRANDCHILD_DICT = {
      Person.FEMALE: _('A birth of a great-great granddaughter'),
      Person.MALE: _('A birth of a great-great grandson'),
  }
  AUTO_EVENT_HAD_NEPHEW_OR_NIECE_DICT = {
      Person.FEMALE: _('A birth of a niece'),
      Person.MALE: _('A birth of a nephew'),
  }
  AUTO_EVENT_HAD_SIBLING_DICT = {
      Person.FEMALE: _('A birth of a sister'),
      Person.MALE: _('A birth of a brother'),
  }

  # Death.
  AUTO_EVENT_LOST_AUNT_OR_UNCLE_DICT = {
      Person.FEMALE: _('A death of an aunt'),
      Person.MALE: _('A death of an uncle'),
  }
  AUTO_EVENT_LOST_CHILD_DICT = {
      Person.FEMALE: _('A death of a daughter'),
      Person.MALE: _('A death of a son'),
  }
  AUTO_EVENT_LOST_COUSIN_DICT = {
      Person.FEMALE: _('A death of a cousin sister'),
      Person.MALE: _('A death of a cousin brother'),
  }
  AUTO_EVENT_LOST_GRANDCHILD_DICT = {
      Person.FEMALE: _('A death of a granddaughter'),
      Person.MALE: _('A death of a grandson'),
  }
  AUTO_EVENT_LOST_GREAT_GRANDCHILD_DICT = {
      Person.FEMALE: _('A death of a great granddaughter'),
      Person.MALE: _('A death of a great grandson'),
  }
  AUTO_EVENT_LOST_GREAT_GREAT_GRANDCHILD_DICT = {
      Person.FEMALE: _('A death of a great-great granddaughter'),
      Person.MALE: _('A death of a great-great grandson'),
  }
  AUTO_EVENT_LOST_GRANDPARENT_DICT = {
      Person.FEMALE: _('A death of a grandmother'),
      Person.MALE: _('A death of a grandfather'),
  }
  AUTO_EVENT_LOST_GREAT_GRANDPARENT_DICT = {
      Person.FEMALE: _('A death of a great grandmother'),
      Person.MALE: _('A death of a great grandfather'),
  }
  AUTO_EVENT_LOST_GREAT_GREAT_GRANDPARENT_DICT = {
      Person.FEMALE: _('A death of a great-great grandmother'),
      Person.MALE: _('A death of a great-great grandfather'),
  }
  AUTO_EVENT_LOST_NEPHEW_OR_NIECE_DICT = {
      Person.FEMALE: _('A death of a niece'),
      Person.MALE: _('A death of a nephew'),
  }
  AUTO_EVENT_LOST_SIBLING_DICT = {
      Person.FEMALE: _('A death of a sister'),
      Person.MALE: _('A death of a brother'),
  }

  ENTRY_EVENT_DICT = {
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
      f'{AUTO_EVENT_HAD_AUNT_OR_UNCLE}_date': (
          AUTO_EVENT_HAD_AUNT_OR_UNCLE_DICT),
      f'{AUTO_EVENT_HAD_AUNT_OR_UNCLE}_year': (
          AUTO_EVENT_HAD_AUNT_OR_UNCLE_DICT),

      f'{AUTO_EVENT_HAD_CHILD}_date': AUTO_EVENT_HAD_CHILD_DICT,
      f'{AUTO_EVENT_HAD_CHILD}_year': AUTO_EVENT_HAD_CHILD_DICT,

      f'{AUTO_EVENT_HAD_COUSIN}_date': AUTO_EVENT_HAD_COUSIN_DICT,
      f'{AUTO_EVENT_HAD_COUSIN}_year': AUTO_EVENT_HAD_COUSIN_DICT,

      f'{AUTO_EVENT_HAD_GRANDCHILD}_date': AUTO_EVENT_HAD_GRANDCHILD_DICT,
      f'{AUTO_EVENT_HAD_GRANDCHILD}_year': AUTO_EVENT_HAD_GRANDCHILD_DICT,

      f'{AUTO_EVENT_HAD_GREAT_GRANDCHILD}_date': (
          AUTO_EVENT_HAD_GREAT_GRANDCHILD_DICT),
      f'{AUTO_EVENT_HAD_GREAT_GRANDCHILD}_year': (
          AUTO_EVENT_HAD_GREAT_GRANDCHILD_DICT),

      f'{AUTO_EVENT_HAD_GREAT_GREAT_GRANDCHILD}_date': (
          AUTO_EVENT_HAD_GREAT_GREAT_GRANDCHILD_DICT),
      f'{AUTO_EVENT_HAD_GREAT_GREAT_GRANDCHILD}_year': (
          AUTO_EVENT_HAD_GREAT_GREAT_GRANDCHILD_DICT),

      f'{AUTO_EVENT_HAD_NEPHEW_OR_NIECE}_date': (
          AUTO_EVENT_HAD_NEPHEW_OR_NIECE_DICT),
      f'{AUTO_EVENT_HAD_NEPHEW_OR_NIECE}_year': (
          AUTO_EVENT_HAD_NEPHEW_OR_NIECE_DICT),

      f'{AUTO_EVENT_HAD_SIBLING}_date': AUTO_EVENT_HAD_SIBLING_DICT,
      f'{AUTO_EVENT_HAD_SIBLING}_year': AUTO_EVENT_HAD_SIBLING_DICT,

      f'{AUTO_EVENT_LOST_AUNT_OR_UNCLE}_date': (
          AUTO_EVENT_LOST_AUNT_OR_UNCLE_DICT),
      f'{AUTO_EVENT_LOST_AUNT_OR_UNCLE}_year': (
          AUTO_EVENT_LOST_AUNT_OR_UNCLE_DICT),

      f'{AUTO_EVENT_LOST_CHILD}_year': AUTO_EVENT_LOST_CHILD_DICT,
      f'{AUTO_EVENT_LOST_CHILD}_date': AUTO_EVENT_LOST_CHILD_DICT,

      f'{AUTO_EVENT_LOST_COUSIN}_date': AUTO_EVENT_LOST_COUSIN_DICT,
      f'{AUTO_EVENT_LOST_COUSIN}_year': AUTO_EVENT_LOST_COUSIN_DICT,

      f'{AUTO_EVENT_LOST_GRANDCHILD}_date': AUTO_EVENT_LOST_GRANDCHILD_DICT,
      f'{AUTO_EVENT_LOST_GRANDCHILD}_year': AUTO_EVENT_LOST_GRANDCHILD_DICT,

      f'{AUTO_EVENT_LOST_GREAT_GRANDCHILD}_date': (
          AUTO_EVENT_LOST_GREAT_GRANDCHILD_DICT),
      f'{AUTO_EVENT_LOST_GREAT_GRANDCHILD}_year': (
          AUTO_EVENT_LOST_GREAT_GRANDCHILD_DICT),

      f'{AUTO_EVENT_LOST_GREAT_GREAT_GRANDCHILD}_date': (
          AUTO_EVENT_LOST_GREAT_GREAT_GRANDCHILD_DICT),
      f'{AUTO_EVENT_LOST_GREAT_GREAT_GRANDCHILD}_year': (
          AUTO_EVENT_LOST_GREAT_GREAT_GRANDCHILD_DICT),

      f'{AUTO_EVENT_LOST_GRANDPARENT}_date': AUTO_EVENT_LOST_GRANDPARENT_DICT,
      f'{AUTO_EVENT_LOST_GRANDPARENT}_year': AUTO_EVENT_LOST_GRANDPARENT_DICT,

      f'{AUTO_EVENT_LOST_GREAT_GRANDPARENT}_date': (
          AUTO_EVENT_LOST_GREAT_GRANDPARENT_DICT),
      f'{AUTO_EVENT_LOST_GREAT_GRANDPARENT}_year': (
          AUTO_EVENT_LOST_GREAT_GRANDPARENT_DICT),

      f'{AUTO_EVENT_LOST_GREAT_GREAT_GRANDPARENT}_date': (
          AUTO_EVENT_LOST_GREAT_GREAT_GRANDPARENT_DICT),
      f'{AUTO_EVENT_LOST_GREAT_GREAT_GRANDPARENT}_year': (
          AUTO_EVENT_LOST_GREAT_GREAT_GRANDPARENT_DICT),

      f'{AUTO_EVENT_LOST_NEPHEW_OR_NIECE}_date': (
          AUTO_EVENT_LOST_NEPHEW_OR_NIECE_DICT),
      f'{AUTO_EVENT_LOST_NEPHEW_OR_NIECE}_year': (
          AUTO_EVENT_LOST_NEPHEW_OR_NIECE_DICT),

      f'{AUTO_EVENT_LOST_SIBLING}_date': AUTO_EVENT_LOST_SIBLING_DICT,
      f'{AUTO_EVENT_LOST_SIBLING}_year': AUTO_EVENT_LOST_SIBLING_DICT,

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
