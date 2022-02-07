"""Entry API views."""

from django.utils.translation import gettext_lazy as _

from rest_framework.response import Response
from rest_framework.views import APIView

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

  def get_queryset(self):
    """Get queryset."""

    return self.model.nodes.filter(actor_uid=self.person.uid,
                                   tree_uid=self.tree.uid).order_by(
                                       'position', 'occurred')


class Timeline(TreePersonNodeMixin, APIView):
  """Person timeline API endpoint."""

  model = Entry
  name = _('Timeline')
  serializer_class = entry.TreeNodeSerializer

  def get(self, request, **kwargs):
    """Return person's timeline."""

    items = [{
        'occurred': e.occurred,
        'summary': e.summary,
        'uid': e.uid
    } for e in self.get_queryset()]

    items.append({
        'occurred': self.person.birth_year,
        'summary': _('Born'),
        'uid': self.person.uid,
    })

    return Response(items)
