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

  ERROR_CODE_DETAILS_REQUIRED = 'details_required'
  ERROR_CODE_PERSON_REQUIRED = 'person_required'

  event_uid = forms.ChoiceField(label=_('Event'))
  entity_uid = forms.ChoiceField(label=_('Entity'), required=False)
  location_uid = forms.ChoiceField(label=_('Location'), required=False)
  person_uid = forms.ChoiceField(label=_('Person'), required=False)

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    entities = Entity.nodes.filter(tree_uid=self.tree.uid)
    entities = BLANK_CHOICE_DASH + [(e.uid, str(e)) for e in entities]

    events = BLANK_CHOICE_DASH + list(Entry.EVENTS)

    locations = Location.nodes.filter(tree_uid=self.tree.uid)
    locations = BLANK_CHOICE_DASH + sorted([(l.uid, str(l)) for l in locations],
                                           key=lambda l: l[1])

    persons = Person.nodes.filter(tree_uid=self.tree.uid)
    persons = BLANK_CHOICE_DASH + [(p.uid, str(p)) for p in persons]

    self.fields['entity_uid'].choices = entities
    self.fields['event_uid'].choices = events
    self.fields['location_uid'].choices = locations
    self.fields['person_uid'].choices = persons

  def clean(self):
    entity_uid = self.cleaned_data['entity_uid']
    event = self.cleaned_data['event_uid']
    location_uid = self.cleaned_data['location_uid']
    person_uid = self.cleaned_data['person_uid']
    text = self.cleaned_data['text']

    if not any((entity_uid, location_uid, person_uid, text)):
      raise forms.ValidationError(
          _("One of the 'Person', 'Entity', 'Location' or 'Text' fields is "
            "required."), code=self.ERROR_CODE_DETAILS_REQUIRED)

    if event in (Entry.EVENT_GOT_MARRIED, Entry.EVENT_HAD_BABY):
      if not person_uid:
        self.add_error('person_uid', _('Required field'))
        raise forms.ValidationError(_(
            "The 'Person' field is required for '%(event)s' event") % {
                'event': Entry.EVENT_CHOICES[event]
            }, code=self.ERROR_CODE_PERSON_REQUIRED)

    return self.cleaned_data

  class Meta:
    """Entity form meta."""

    fields = (
        'occurred',
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
