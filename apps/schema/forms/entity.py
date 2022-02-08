"""Entity forms."""

from django import forms
from django.db.models import BLANK_CHOICE_DASH
from django.utils.translation import gettext_lazy as _

from apps.schema.forms.base import TreeFormBase
from apps.schema.models.entity import Entity
from apps.schema.models.location import Location


class EntityForm(TreeFormBase):
  """Entity form."""

  category_uid = forms.ChoiceField(label=_('Category'), widget=forms.Select())
  location_uid = forms.ChoiceField(label=_('Address'))

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    categories = BLANK_CHOICE_DASH + list(Entity.CATEGORY_CHOICES)

    locations = Location.nodes.filter(tree_uid=self.tree.uid)
    locations = BLANK_CHOICE_DASH + sorted([(l.uid, str(l)) for l in locations],
                                           key=lambda l: l[1])

    self.fields['category_uid'].choices = categories
    self.fields['location_uid'].choices = locations

  class Meta:
    """Entity form meta."""

    fields = (
        'name',
        'category_uid',
        'location_uid',
        'summary',
        'details',
        'url',
    )
    model = Entity
