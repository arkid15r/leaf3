"""Person forms."""

from django import forms
from django.db.models import BLANK_CHOICE_DASH
from django.utils.translation import gettext_lazy as _

from bootstrap_datepicker_plus.widgets import DatePickerInput

from apps.schema.forms.base import TreeFormBase
from apps.schema.models.location import Location
from apps.schema.models.person import Person


class PersonForm(TreeFormBase):
  """Person form."""

  birthplace_uid = forms.ChoiceField(label=_('Birthplace'), required=False)
  gender = forms.ChoiceField(label=_('Gender'), choices=Person.GENDERS, widget=forms.RadioSelect)
  father_uid = forms.ChoiceField(label=_('Father'), required=False)
  mother_uid = forms.ChoiceField(label=_('Mother'), required=False)
  residence_uid = forms.ChoiceField(label=_('Residence'), required=False)
  spouse_uid = forms.ChoiceField(label=_('Spouse'), required=False)

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    persons = Person.nodes.filter(tree_uid=self.tree_uid)
    if self.instance:
      persons.exclude(uid=self.instance.uid)

    persons = BLANK_CHOICE_DASH + [(p.uid, str(p)) for p in persons]
    locations = BLANK_CHOICE_DASH + [
        (l.uid, str(l)) for l in Location.nodes.filter(tree_uid=self.tree_uid)
    ]

    self.fields['birthplace_uid'].choices = locations
    self.fields['father_uid'].choices = persons
    self.fields['mother_uid'].choices = persons
    self.fields['residence_uid'].choices = locations
    self.fields['spouse_uid'].choices = persons

  class Meta:
    """Person form meta."""

    fields = (
        'last_name',
        'first_name',
        'patronymic_name',
        'maiden_name',
        'gender',
        'dob',
        'dod',
        'cod',
        'details',
        'birthplace_uid',
        'residence_uid',
        'father_uid',
        'mother_uid',
        'spouse_uid',
    )
    model = Person
    widgets = {
        'details': forms.Textarea(),
        'dob': DatePickerInput(format='%d/%m/%Y'),
        'dod': DatePickerInput(format='%d/%m/%Y'),
    }
