"""Person models."""

from django.conf import settings
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from dateutil.relativedelta import relativedelta
from neomodel import (DateProperty, Relationship, RelationshipFrom,
                      StringProperty)

from apps.schema.models.base import TreeNodeModel


class Person(TreeNodeModel):
  """Person model."""

  FEMALE = 'F'
  MALE = 'M'

  GENDERS = ((FEMALE, _('Female')), (MALE, _('Male')))

  first_name = StringProperty(label=_('First name'), max_length=25, required=True,)
  patronymic_name = StringProperty(label=_('Patronymic name'), max_length=25)
  last_name = StringProperty(label=_('Last name'), required=True, max_length=50)
  maiden_name = StringProperty(label=_('Maiden name'), max_length=25)

  gender = StringProperty(label=_('Gender'), required=True, choices=GENDERS)
  dob = DateProperty(label=_('Date of birth'), index=True)
  dod = DateProperty(label=_('Date of death'))

  cod = StringProperty(label=_('Cause of death'), max_length=25)

  father_uid = StringProperty(max_length=settings.SHORT_UUID_LENGTH)
  mother_uid = StringProperty(max_length=settings.SHORT_UUID_LENGTH)
  spouse_uid = StringProperty(max_length=settings.SHORT_UUID_LENGTH)

  about = StringProperty(label=_('About'), max_length=1000)

  # Relationships.
  parents_rel = RelationshipFrom('Person', 'PARENT')
  siblings_rel = Relationship('Person', 'SIBLING')
  spouse_rel = Relationship('Person', 'SPOUSE')

  def __str__(self):
    """Person str()."""

    return self.full_name

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

  class Meta:
    """Person model meta."""

    app_label = 'schema'
    verbose_name = _('Person')
    verbose_name_plural = _('Persons')
