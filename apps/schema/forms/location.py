"""Location forms."""

from apps.schema.forms.base import TreeFormBase
from apps.schema.models.location import Location


class LocationForm(TreeFormBase):
  """Location form."""

  class Meta:
    """Location form meta."""

    fields = (
        'street',
        'town',
        'area',
        'state',
        'country',
    )
    model = Location
