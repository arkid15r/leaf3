"""Entry forms."""

from django import forms
from django.db.models import BLANK_CHOICE_DASH
from django.utils.translation import gettext_lazy as _

from bootstrap_datepicker_plus.widgets import DatePickerInput

from apps.schema.forms.base import TreeFormBase
from apps.schema.models.entity import Entity
from apps.schema.models.entry import Entry
from apps.schema.models.location import Location
from apps.schema.models.person import Person


class EntryForm(TreeFormBase):
  """Entry form."""

  actor_uid = forms.ChoiceField(label=_('Actor'))
  action_uid = forms.ChoiceField(label=_('Event'))
  entity_uid = forms.ChoiceField(label=_('Entity'), required=False)
  location_uid = forms.ChoiceField(label=_('Location'), required=False)
  person_uid = forms.ChoiceField(label=_('Person'), required=False)

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    actions = BLANK_CHOICE_DASH + list(Entry.ACTIONS)

    entities = Entity.nodes.filter(tree_uid=self.tree_uid)
    entities = BLANK_CHOICE_DASH + [(e.uid, str(e)) for e in entities]

    locations = Location.nodes.filter(tree_uid=self.tree_uid)
    locations = BLANK_CHOICE_DASH + sorted([(l.uid, str(l)) for l in locations],
                                           key=lambda l: l[1])

    persons = Person.nodes.filter(tree_uid=self.tree_uid)
    persons = BLANK_CHOICE_DASH + [(p.uid, str(p)) for p in persons]

    self.fields['action_uid'].choices = actions
    self.fields['actor_uid'].choices = persons
    self.fields['entity_uid'].choices = entities
    self.fields['location_uid'].choices = locations
    self.fields['person_uid'].choices = persons

  def clean(self):
    action = self.cleaned_data['action_uid']

    entity_uid = self.cleaned_data['entity_uid']
    location_uid = self.cleaned_data['location_uid']
    person_uid = self.cleaned_data['person_uid']

    if not any((entity_uid, location_uid, person_uid)):
      raise forms.ValidationError(
          _("One of the 'Person', 'Entity' or 'Location' fields is required."))

    if action == Entry.ACTION_MARRIED:
      if not person_uid:
        self.add_error('person_uid', _('Required field'))
        raise forms.ValidationError(_(
            "The 'Person' field is required for %(action)s event") % {
                'action': Entry.ACTION_MARRIED_TEXT
            })

    return self.cleaned_data

  class Meta:
    """Entity form meta."""

    fields = (
        'actor_uid',
        'occurred',
        'action_uid',
        'person_uid',
        'entity_uid',
        'location_uid',
    )
    model = Entry
    widgets = {
        'occurred': DatePickerInput(format='%d/%m/%Y'),
    }
