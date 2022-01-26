"""Location models."""

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from neomodel import StringProperty

from apps.schema.models.base import TreeNodeModel


class Location(TreeNodeModel):
  """Location model."""

  street = StringProperty(label=_('Address'), max_length=50)
  town = StringProperty(label=_('Town'), max_length=50, required=True)
  area = StringProperty(label=_('Area'), max_length=50)
  state = StringProperty(label=_('State'), max_length=50)
  country = StringProperty(label=_('Country'), max_length=50)

  def __str__(self):
    """Location str()."""

    return self.detailed_address

  def join_fields(self, field_names):
    """Returns joined fields."""

    fields = []
    for field_name in field_names:
      value = getattr(self, field_name)
      if not value:
        continue
      fields.append(value)

    return ', '.join(fields)

  @property
  def short_address(self):
    """Location short address."""

    return self.join_fields(('town', 'state'))

  @property
  def detailed_address(self):
    """Location detailed address."""

    return self.join_fields(('street', 'town', 'state', 'country'))

  @property
  def long_address(self):
    """Location long address."""

    return self.join_fields(('town', 'state', 'country'))

  @property
  def full_address(self):
    """Location full address."""

    return self.join_fields(('street', 'town', 'area', 'state', 'country'))

  def get_absolute_url(self):
    """Return location absolute URL."""

    return reverse_lazy('location', args=(self.tree_uid, self.uid))

  class Meta:
    """Location model meta."""

    app_label = 'schema'
    verbose_name = _('Location')
    verbose_name_plural = _('Locations')
