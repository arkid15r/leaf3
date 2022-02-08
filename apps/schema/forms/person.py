"""Person forms."""

import copy

from django import forms
from django.db.models import BLANK_CHOICE_DASH
from django.utils.translation import gettext_lazy as _

from bootstrap_datepicker_plus.widgets import DatePickerInput

from apps.schema.forms.base import TreeFormBase
from apps.schema.models.person import Person


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

    locations = BLANK_CHOICE_DASH + [
        (l.uid, str(l)) for l in self.tree.locations
    ]

    all_persons = BLANK_CHOICE_DASH + [(p.uid, str(p)) for p in all_persons]

    self.fields['birth_place_uid'].choices = locations
    self.fields['burial_place_uid'].choices = locations
    self.fields['death_place_uid'].choices = locations
    self.fields['father_uid'].choices = male_persons
    self.fields['mother_uid'].choices = female_persons
    self.fields['residence_uid'].choices = locations
    self.fields['spouse_uid'].choices = all_persons

  class Meta:
    """Person form meta."""

    fields = (
        'last_name',
        'first_name',
        'patronymic_name',
        'maiden_name',
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
