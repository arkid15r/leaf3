"""Person forms."""

from django import forms
from django.db.models import BLANK_CHOICE_DASH
from django.utils.translation import gettext_lazy as _

from bootstrap_datepicker_plus.widgets import DatePickerInput

from apps.schema.models.location import Location
from apps.schema.models.person import Person


class PersonForm(forms.ModelForm):
  """Person form."""

  birthplace_uid = forms.ChoiceField(label=_('Birthplace'), required=False)
  gender = forms.ChoiceField(label=_('Gender'), choices=Person.GENDERS, widget=forms.RadioSelect)
  father_uid = forms.ChoiceField(label=_('Father'), required=False)
  mother_uid = forms.ChoiceField(label=_('Mother'), required=False)
  residence_uid = forms.ChoiceField(label=_('Residence'), required=False)
  spouse_uid = forms.ChoiceField(label=_('Spouse'), required=False)

  def __init__(self, *args, **kwargs):
    tree_uid = kwargs.pop('tree_uid')
    persons = Person.nodes.filter(tree_uid=tree_uid)

    super().__init__(*args, **kwargs)

    if self.instance:
      persons.exclude(uid=self.instance.uid)

    persons = BLANK_CHOICE_DASH + [(p.uid, str(p)) for p in persons]

    self.fields['father_uid'].choices = persons
    self.fields['mother_uid'].choices = persons
    self.fields['spouse_uid'].choices = persons

    locations = Location.nodes.filter(tree_uid=tree_uid)
    locations = BLANK_CHOICE_DASH + [(l.uid, str(l)) for l in locations]

    self.fields['birthplace_uid'].choices = locations
    self.fields['residence_uid'].choices = locations

  class Meta:
    """Person form meta."""

    fields = (
        'last_name',
        'first_name',
        'patronymic_name',
        'gender',
        'dob',
        'dod',
        'cod',
        'about',
        'birthplace_uid',
        'residence_uid',
        'father_uid',
        'mother_uid',
        'spouse_uid',
    )
    model = Person
    widgets = {
        'about': forms.Textarea,
        'dob': DatePickerInput(format='%d/%m/%Y'),
        'dod': DatePickerInput(format='%d/%m/%Y'),
    }
