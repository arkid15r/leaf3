"""Person API views."""

from django.utils.translation import gettext_lazy as _

from rest_framework.response import Response
from rest_framework.views import APIView

from apps.schema.models.person import Person
from apps.schema.serializers import person
from apps.schema.views.api.base import DataTableListBase
from apps.schema.views.base import TreeNodeMixin


class DataTableList(DataTableListBase):
  """Person list API endpoint."""

  model = Person
  name = _('Persons')
  order_by_fields = ('name', 'birth_year', 'birthplace', 'residence')
  search_fields = ('first_name', 'last_name', 'maiden_name', 'cod',
                   'birth_year')
  serializer_class = person.ListItemSerializer


class Item(TreeNodeMixin, APIView):
  """Person item API endpoint."""

  model = Person
  name = _('Person')
  serializer_class = person.ItemSerializer

  def get(self, request, **kwargs):
    """Return person."""

    return Response(self.serializer_class(self.get_object()).data)


class SimpleTree(TreeNodeMixin, APIView):
  """Person simple tree API endpoint."""

  model = Person
  name = _('Simple tree')
  serializer_class = person.TreeNodeSerializer

  def build_ancestor_tree(self, person):
    """Build ancestor tree for a person. The 'children' attribute of a node is
       required in order to get the tree visualized properly. Apparently it
       contains parents of each person."""

    data = self.serializer_class(person).data
    data['children'] = []

    nodes = person.parents
    while nodes:
      node = nodes.pop(0)

      # Add ancestors.
      data['children'].append(self.build_ancestor_tree(node))

      # Add siblings.
      for sibling in node.siblings:
        data['children'].append(self.serializer_class(sibling).data)

    return data

  def build_descendant_tree(self, person):
    """Build descendant tree for a person."""

    data = self.serializer_class(person).data
    data['children'] = []

    nodes = person.children
    while nodes:
      node = nodes.pop(-1)

      # Add descendants.
      data['children'].append(self.build_descendant_tree(node))

    return data

  def get(self, request, **kwargs):
    """Return person's parent tree."""

    direction = request.query_params.get('direction')
    nodes = []

    if direction == 'ancestor':
      nodes = self.build_ancestor_tree(self.get_object())
    elif direction == 'descendant':
      nodes = self.build_descendant_tree(self.get_object())

    return Response(nodes)
