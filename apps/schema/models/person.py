"""Person models."""

from django.conf import settings
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext_lazy

from dateutil.relativedelta import relativedelta
from neomodel import (DateProperty, Relationship, RelationshipFrom,
                      RelationshipTo, StringProperty)

from apps.schema.models.base import TreeNodeModel
from apps.schema.models.db.relationships import TimeRangeRelationship
from apps.schema.models.location import Location


class Person(TreeNodeModel):
  """Person model."""

  FEMALE = 'F'
  MALE = 'M'

  GENDERS = ((FEMALE, _('Female')), (MALE, _('Male')))

  first_name = StringProperty(label=_('First name'), max_length=25, required=True)
  patronymic_name = StringProperty(label=_('Patronymic name'), max_length=25)
  last_name = StringProperty(label=_('Last name'), required=True, max_length=50)
  maiden_name = StringProperty(label=_('Maiden name'), max_length=25)

  gender = StringProperty(label=_('Gender'), required=True, choices=GENDERS)
  dob = DateProperty(label=_('Date of birth'), index=True)
  dod = DateProperty(label=_('Date of death'))

  cod = StringProperty(label=_('Cause of death'), max_length=25)
  cod_details = StringProperty(label=_('Cause of death details'), max_length=200)

  # Persons.
  father_uid = StringProperty(max_length=settings.SHORT_UUID_LENGTH)
  mother_uid = StringProperty(max_length=settings.SHORT_UUID_LENGTH)
  spouse_uid = StringProperty(max_length=settings.SHORT_UUID_LENGTH)

  details = StringProperty(label=_('Details'), max_length=10000)

  # Locations.
  birthplace_uid = StringProperty(max_length=settings.SHORT_UUID_LENGTH)
  residence_uid = StringProperty(max_length=settings.SHORT_UUID_LENGTH)

  # Relationships.
  birthplace_rel = RelationshipTo('.location.Location', 'BORN')
  residence_rel = RelationshipTo('.location.Location', 'LIVES')

  parents_rel = RelationshipFrom('.person.Person', 'PARENT')
  spouse_rel = Relationship('.person.Person', 'SPOUSE')

  marriage_rel = Relationship('.person.Person',
                              'MARRIED',
                              model=TimeRangeRelationship)
  employment_rel = RelationshipTo('.entity.Entity',
                                  'WORKED',
                                  model=TimeRangeRelationship)

  def __str__(self):
    """Person str()."""

    return self.full_name

  @property
  def birthplace(self):
    """Return birthplace location."""

    if not self.birthplace_uid:
      return

    try:
      return Location.nodes.get(uid=self.birthplace_uid)
    except Location.DoesNotExist:
      pass

  @property
  def children(self):
    """Return person's children."""

    return self.cypher(
        f'MATCH (Person {{ uid: "{self.uid}" }}) -[:PARENT]-> (children:Person) return children'
    )

  @property
  def entry_create_url(self):
    """Return entry create URL."""

    return reverse_lazy('entry-create', args=(self.tree_uid, self.uid))

  @property
  def entry_list_url(self):
    """Return entry list URL."""

    return reverse_lazy('entry-list', args=(self.tree_uid, self.uid))

  @property
  def full_name(self):
    """Return full name."""

    fields = [self.last_name, self.first_name]
    if self.patronymic_name:
      fields.append(self.patronymic_name)

    return ' '.join(fields)

  @property
  def is_female(self):
    """Return True if person's gender value is FEMALE."""

    return self.gender == self.FEMALE

  @property
  def is_male(self):
    """Return True if person's gender value is MALE."""

    return self.gender == self.MALE

  @property
  def object_delete_url(self):
    """Return person delete URL."""

    return reverse_lazy('person-delete', args=(self.tree_uid, self.uid))

  @property
  def object_read_url(self):
    """Return person delete URL."""

    return reverse_lazy('person', args=(self.tree_uid, self.uid))

  @property
  def object_update_url(self):
    """Return person update URL."""

    return reverse_lazy('person-update', args=(self.tree_uid, self.uid))

  @property
  def residence(self):
    """Return residence location."""

    if not self.residence_uid:
      return

    try:
      return Location.nodes.get(uid=self.residence_uid)
    except Location.DoesNotExist:
      pass

  @property
  def spouse(self):
    """Return spouse person."""

    if not self.spouse_uid:
      return

    try:
      return Person.nodes.get(uid=self.spouse_uid)
    except Person.DoesNotExist:
      pass

  @property
  def summary(self):
    """Return person summary information."""

    result = ''
    if self.dod:
      age = relativedelta(self.dod, self.dob).years
      if self.is_female:
        result = ngettext_lazy('died in the age of {f} year',
                               'died in the age of {f} years',
                               age).format(f=age)
      elif self.is_male:
        result = ngettext_lazy('died in the age of {m} year',
                               'died in the age of {m} years',
                               age).format(m=age)
    elif self.dob:
      age = relativedelta(now().date(), self.dob).years
      result = ngettext_lazy('{n} year', '{n} years', age).format(n=age)

    return result

  class Meta:
    """Person model meta."""

    app_label = 'schema'
    verbose_name = _('Person')
    verbose_name_plural = _('Persons')
