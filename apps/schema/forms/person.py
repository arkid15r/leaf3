"""Person forms."""

import copy

from django import forms
from django.db.models import BLANK_CHOICE_DASH
from django.utils.translation import gettext_lazy as _

from bootstrap_datepicker_plus.widgets import DatePickerInput

from apps.schema.forms.base import TreeFormBase
from apps.schema.models.person import Person
from apps.schema.validators import person


class PersonForm(TreeFormBase):
  """Person form."""

  birth_place_uid = forms.ChoiceField(label=_('Birth place'), required=False)
  burial_place_uid = forms.ChoiceField(label=_('Burial place'), required=False)
  death_place_uid = forms.ChoiceField(label=_('Death place'), required=False)
  gender = forms.ChoiceField(
      label=_('Gender'),
      choices=Person.GENDER_CHOICES, widget=forms.RadioSelect)
  father_uid = forms.ChoiceField(label=_('Father'), required=False)
  mother_uid = forms.ChoiceField(label=_('Mother'), required=False)
  residence_uid = forms.ChoiceField(label=_('Residence'), required=False)
  spouse_uid = forms.ChoiceField(label=_('Spouse'), required=False)

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    all_persons = self.tree.persons
    if self.instance:
      all_persons.exclude(uid=self.instance.uid)

    female_persons = copy.deepcopy(all_persons).exclude(gender=Person.MALE)
    female_persons = BLANK_CHOICE_DASH + [
        (p.uid, str(p)) for p in female_persons
    ]

    male_persons = copy.deepcopy(all_persons).exclude(gender=Person.FEMALE)
    male_persons = BLANK_CHOICE_DASH + [(p.uid, str(p)) for p in male_persons]

    locations = BLANK_CHOICE_DASH + sorted(
        [(l.uid, str(l)) for l in self.tree.locations],
        key=lambda l: l[1],
        reverse=True)

    all_persons = BLANK_CHOICE_DASH + [(p.uid, str(p)) for p in all_persons]

    self.fields['birth_place_uid'].choices = locations
    self.fields['burial_place_uid'].choices = locations
    self.fields['death_place_uid'].choices = locations
    self.fields['father_uid'].choices = male_persons
    self.fields['mother_uid'].choices = female_persons
    self.fields['residence_uid'].choices = locations
    self.fields['spouse_uid'].choices = all_persons

    self.fields['birth_year'].help_text = _('Enter birth year or - if birth year is unknown.')
    self.fields['death_year'].help_text = _('Enter death year or - if death year is unknown.')

    self.fields['birth_year'].validators.append(person.validate_year)
    self.fields['death_year'].validators.append(person.validate_year)

  def clean(self):
    """Clean data."""

    data = self.cleaned_data

    # First name, last name.
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if not first_name and not last_name:
      raise forms.ValidationError(
          _('Either first name or last name is required.'))

    # Birth.
    birth_date = data.get('birth_date')
    birth_year = data.get('birth_year')

    if birth_year == Person.EMPTY_VALUE:
      birth_year = -1
    if birth_year:
      birth_year = int(birth_year)

    if (birth_date and birth_year is not None
        and birth_date.year != birth_year):
      raise forms.ValidationError(_('The birth year and birth date year must match.'))

    # Death.
    death_date = data.get('death_date')
    death_year = data.get('death_year')

    if death_year == Person.EMPTY_VALUE:
      death_year = -1
    if death_year:
      death_year = int(death_year)

    if (death_date and death_year is not None
        and death_date.year != death_year):
      raise forms.ValidationError(
          _('The death year and death date year must match.'))

    # Burial.
    burial_date = data.get('burial_date')
    if burial_date and death_date and burial_date < death_date:
      raise forms.ValidationError(
          _('The burial date cannot be earlier than death date.'))

    return data

  class Meta:
    """Person form meta."""

    fields = (
        'last_name',
        'first_name',
        'patronymic_name',
        'maiden_name',
        'other_names',
        'gender',
        'birth_year',
        'birth_date',
        'birth_place_uid',
        'details',
        'residence_uid',
        'father_uid',
        'mother_uid',
        'spouse_uid',
        'death_year',
        'death_date',
        'death_place_uid',
        'burial_date',
        'burial_place_uid',
        'death_cause',
        'death_cause_details',
    )
    model = Person
    widgets = {
        'birth_date': DatePickerInput(format='%d/%m/%Y'),
        'burial_date': DatePickerInput(format='%d/%m/%Y'),
        'death_date': DatePickerInput(format='%d/%m/%Y'),
        'details': forms.Textarea(),
    }
