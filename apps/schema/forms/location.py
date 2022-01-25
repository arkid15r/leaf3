"""Location forms."""

from django import forms

from apps.schema.models.location import Location


class LocationForm(forms.ModelForm):
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
