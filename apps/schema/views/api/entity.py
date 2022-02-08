"""Entity API views."""

from django.utils.translation import gettext_lazy as _

from apps.schema.models.entity import Entity
from apps.schema.serializers import entity
from apps.schema.views.api.base import DataTableListBase


class DataTableList(DataTableListBase):
  """Entity list API endpoint."""

  model = Entity
  name = _('Entities')
  order_by_fields = ('name', 'category', 'location')
  search_fields = ('name',)
  serializer_class = entity.ListItemSerializer
