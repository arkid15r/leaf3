"""Entry forms."""

from django import forms
from django.db.models import BLANK_CHOICE_DASH
from django.utils.translation import gettext_lazy as _

from bootstrap_datepicker_plus.widgets import DatePickerInput

from apps.schema.forms.base import PersonFormBase
from apps.schema.models.entity import Entity
from apps.schema.models.entry import Entry
from apps.schema.models.location import Location
from apps.schema.models.person import Person


class EntryForm(PersonFormBase):
  """Entry form."""

  ERROR_CODE_ENTITY_OR_LOCATION_REQUIRED = 'entity_or_location_required'
  ERROR_CODE_ENTITY_REQUIRED = 'entity_required'
  ERROR_CODE_FIELD_REQUIRED = 'required_field'
  ERROR_CODE_ONE_OF_FIELDS_REQUIRED = 'one_of_fields_required'
  ERROR_CODE_PERSON_REQUIRED = 'person_required'

  TRANSLATIONS = {
      ERROR_CODE_ENTITY_REQUIRED: _(
          'The "Entity" field is required for "{event}" event'),
      ERROR_CODE_ENTITY_OR_LOCATION_REQUIRED: _(
          'One of the "Entity" or "Location" fields is required for "{event}" event'),
      ERROR_CODE_ONE_OF_FIELDS_REQUIRED: _(
          'One of the "Person", "Entity", "Location" or "Text" fields is '
          'required.'),
      ERROR_CODE_PERSON_REQUIRED: _(
          'The "Person" field is required for "{event}" event'),
      ERROR_CODE_FIELD_REQUIRED: _('Required field'),
  }

  event_uid = forms.ChoiceField(label=_('Event'), required=True)
  entity_uid = forms.ChoiceField(label=_('Entity'), required=False)
  location_uid = forms.ChoiceField(label=_('Location'), required=False)
  person_uid = forms.ChoiceField(label=_('Person'), required=False)

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    entities = Entity.nodes.filter(tree_uid=self.tree.uid)
    entities = BLANK_CHOICE_DASH + [(e.uid, str(e)) for e in entities]

    events = BLANK_CHOICE_DASH + sorted(Entry.AVAILABLE_EVENT_CHOICES,
                                        key=lambda e: e[1])

    locations = Location.nodes.filter(tree_uid=self.tree.uid)
    locations = BLANK_CHOICE_DASH + sorted([(l.uid, str(l)) for l in locations],
                                           key=lambda l: l[1])

    persons = Person.nodes.filter(tree_uid=self.tree.uid)
    if self.person:
      persons.exclude(uid=self.person.uid)
    persons = BLANK_CHOICE_DASH + [(p.uid, str(p)) for p in persons]

    self.fields['entity_uid'].choices = entities
    self.fields['event_uid'].choices = events
    self.fields['location_uid'].choices = locations
    self.fields['person_uid'].choices = persons

    if self.instance and self.instance.is_auto_created:
      del self.fields['event_uid']

      if self.instance.is_no_entity_event:
        del self.fields['entity_uid']
      if self.instance.is_no_person_event:
        del self.fields['person_uid']

  def clean(self):
    """Entry form clean."""

    entity_uid = self.cleaned_data.get('entity_uid')
    location_uid = self.cleaned_data.get('location_uid')
    person_uid = self.cleaned_data.get('person_uid')
    text = self.cleaned_data.get('text')

    instance = self.instance

    if (not instance.is_auto_created and not any(
        (entity_uid, location_uid, person_uid, text))):
      raise forms.ValidationError(
          self.TRANSLATIONS[self.ERROR_CODE_ONE_OF_FIELDS_REQUIRED],
          code=self.ERROR_CODE_ONE_OF_FIELDS_REQUIRED)

    return self.cleaned_data

  class Meta:
    """Entity form meta."""

    fields = (
        'occurred',
        'occurred_year',
        'event_uid',
        'person_uid',
        'entity_uid',
        'location_uid',
        'text',
    )
    model = Entry
    widgets = {
        'occurred': DatePickerInput(format='%d/%m/%Y'),
        'text': forms.Textarea(),
    }
