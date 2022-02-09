"""Location API views."""

from django.utils.translation import gettext_lazy as _

from apps.schema.models.location import Location
from apps.schema.serializers import location
from apps.schema.views.api.base import DataTableListBase


class DataTableList(DataTableListBase):
  """Location list API endpoint."""

  model = Location
  name = _('Locations')
  order_by_fields = ('summary',)
  search_fields = ('name',)
  serializer_class = location.ListItemSerializer
