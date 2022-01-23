"""Person forms."""

from django import forms
from django.db.models import BLANK_CHOICE_DASH
from django.utils.translation import gettext as _

from bootstrap_datepicker_plus.widgets import DatePickerInput

from apps.schema.models.person import Person


class PersonForm(forms.ModelForm):
  """Person form."""

  gender = forms.ChoiceField(choices=Person.GENDERS, widget=forms.RadioSelect())
  father_uid = forms.ChoiceField(label=_('Father'), required=False)
  mother_uid = forms.ChoiceField(label=_('Mother'), required=False)
  spouse_uid = forms.ChoiceField(label=_('Spouse'), required=False)

  def __init__(self, *args, **kwargs):
    tree_uid = kwargs.pop('tree_uid')
    persons = Person.nodes.filter(tree_uid=tree_uid)

    super().__init__(*args, **kwargs)

    if self.instance:
      persons.exclude(uid=self.instance.uid)

    self.fields['father_uid'].choices = BLANK_CHOICE_DASH + [
        (p.uid, str(p)) for p in persons
    ]
    self.fields['mother_uid'].choices = BLANK_CHOICE_DASH + [
        (p.uid, str(p)) for p in persons
    ]
    self.fields['spouse_uid'].choices = BLANK_CHOICE_DASH + [
        (p.uid, str(p)) for p in persons
    ]

    self.fields['birth_date'].widget = DatePickerInput()
    self.fields['death_date'].widget = DatePickerInput()

  class Meta:
    """Person form meta."""

    fields = (
        'first_name',
        'patronymic_name',
        'last_name',
        'gender',
        'birth_date',
        'death_date',
        'father_uid',
        'mother_uid',
        'spouse_uid',
    )
    model = Person
