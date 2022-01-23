"""Person models."""

from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from dateutil.relativedelta import relativedelta
from neomodel import (DateProperty, Relationship, RelationshipFrom,
                      StringProperty)

from apps.schema.models.base import ModelBase


class Person(ModelBase):
  """Person model."""

  FEMALE = 'F'
  MALE = 'M'

  GENDERS = ((FEMALE, _('Female')), (MALE, _('Male')))

  first_name = StringProperty(label=_('First name'), required=True)
  patronymic_name = StringProperty(label=_('Patronymic name'))
  last_name = StringProperty(label=_('Last name'), required=True)

  gender = StringProperty(label=_('Gender'), required=True, choices=GENDERS)
  birth_date = DateProperty(label=_('Date of birth'), index=True)
  death_date = DateProperty(label=_('Date of death'))

  death_cause = StringProperty()

  father_uid = StringProperty()
  mother_uid = StringProperty()
  spouse_uid = StringProperty()

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
    if self.death_date:
      age = relativedelta(self.death_date, self.birth_date).years
      result = _('Died in age of %(age)s years') % {'age': age}
    elif self.birth_date:
      age = relativedelta(now().date(), self.birth_date).years
      result = _('%(age)s years') % {'age': age}

    return result

  class Meta:
    """Person model meta."""

    app_label = 'schema'
