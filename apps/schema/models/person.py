"""Person models."""

from django.conf import settings
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from dateutil.relativedelta import relativedelta
from neomodel import (DateProperty, Relationship, RelationshipFrom,
                      RelationshipTo, StringProperty)

from apps.schema.models.base import TreeNodeModel
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

  details = StringProperty(label=_('About'), max_length=10000)

  # Locations.
  birthplace_uid = StringProperty(max_length=settings.SHORT_UUID_LENGTH)
  residence_uid = StringProperty(max_length=settings.SHORT_UUID_LENGTH)

  # Relationships.
  birthplace_rel = RelationshipTo('.location.Location', 'BORN')
  residence_rel = RelationshipTo('.location.Location', 'LIVES')

  parents_rel = RelationshipFrom('.person.Person', 'PARENT')
  spouse_rel = Relationship('.person.Person', 'MARRIED')

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

  def children(self):
    """Return person's children."""

    return self.cypher(
        f'MATCH (Person {{ uid: "{self.uid}" }}) -[:PARENT]-> (children:Person) return children'
    )

  @property
  def full_name(self):
    """Return full name."""

    fields = [self.last_name, self.first_name]
    if self.patronymic_name:
      fields.append(self.patronymic_name)

    return ' '.join(fields)

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
  def status(self):
    """Return age information."""

    result = ''
    if self.dod:
      age = relativedelta(self.dod, self.dob).years
      result = _('Died in age of %(age)s years') % {'age': age}
    elif self.dob:
      age = relativedelta(now().date(), self.dob).years
      result = _('%(age)s years') % {'age': age}

    return result

  @property
  def spouse(self):
    """Return spouse person."""

    if not self.spouse_uid:
      return

    try:
      return Person.nodes.get(uid=self.spouse_uid)
    except Person.DoesNotExist:
      pass

  class Meta:
    """Person model meta."""

    app_label = 'schema'
    verbose_name = _('Person')
    verbose_name_plural = _('Persons')
