"""Location forms."""

from django import forms
from django.db.models import BLANK_CHOICE_DASH
from django.utils.translation import gettext_lazy as _

from apps.schema.forms.base import TreeFormBase
from apps.schema.models.location import Location


class LocationForm(TreeFormBase):
  """Location form."""

  category_uid = forms.ChoiceField(label=_('Category'))
  parent_uid = forms.ChoiceField(label=_('Located in'), required=False)

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    categories = BLANK_CHOICE_DASH + list(Location.CATEGORY_CHOICES)

    locations = Location.nodes.filter(tree_uid=self.tree.uid)
    locations = BLANK_CHOICE_DASH + sorted([(l.uid, str(l)) for l in locations],
                                           key=lambda l: l[1])

    self.fields['category_uid'].choices = categories
    self.fields['parent_uid'].choices = locations

  class Meta:
    """Location form meta."""

    fields = ('name', 'category_uid', 'parent_uid')
    model = Location
