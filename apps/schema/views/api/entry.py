"""Entry API views."""

from django.utils.translation import gettext_lazy as _

from rest_framework.response import Response
from rest_framework.views import APIView

from apps.schema.models.entry import Entry
from apps.schema.serializers import entry
from apps.schema.views.api.base import DataTableListBase
from apps.schema.views.base import TreePersonNodeMixin


class EntryListBase(TreePersonNodeMixin):
  """Entry list base."""

  def get_queryset(self):
    """Get queryset."""

    return self.model.nodes.filter(
        actor_uid=self.person.uid,
        tree_uid=self.tree.uid).exclude(occurred_year='').order_by(
            'position', 'occurred_year', 'occurred')


class EntryList(EntryListBase, APIView):
  """Entry list base class."""

  serializer_class = entry.ItemSerializer

  def get(self, request, format=None):  # pylint: disable=redefined-builtin
    """Return filtered and sorted objects."""

    return Response(self.serializer_class(self.get_queryset(), many=True).data)


class DataTableList(EntryListBase, DataTableListBase):
  """Entry list API endpoint."""

  model = Entry
  name = _('Entries')
  order_by_fields = ('occurred', 'text')
  search_fields = ('text',)
  serializer_class = entry.ListItemSerializer


class Timeline(EntryList):
  """Person timeline API endpoint."""

  model = Entry
  name = _('Timeline')
  serializer_class = entry.ItemSerializer
