"""Entry API views."""

from django.utils.translation import gettext_lazy as _

from apps.schema.models.entry import Entry
from apps.schema.serializers import entry
from apps.schema.views.api.base import DataTableListBase
from apps.schema.views.base import TreePersonNodeMixin


class DataTableList(TreePersonNodeMixin, DataTableListBase):
  """Entry list API endpoint."""

  model = Entry
  name = _('Entries')
  order_by_fields = ('occurred', 'summary')
  search_fields = ('occurred', 'summary')
  serializer_class = entry.ListItemSerializer
