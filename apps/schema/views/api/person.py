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
  order_by_fields = ('name', 'birth_year', 'birth_place', 'residence')
  search_fields = ('first_name', 'last_name', 'maiden_name', 'death_cause',
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
    """Build person's ancestors tree.

    The 'children' attribute of a node is required in order to get the tree
    visualized properly. Apparently it contains parents of each person.
    """

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

  def build_cousin_tree(self, person, perspective='cousins'):
    """Build person's cousins tree."""

    data = self.serializer_class(person).data
    data['children'] = []

    p_idx = 0
    for parent in person.parents:  # Add nodes for parents.
      if not parent.has_nephew_or_niece:
        continue

      if (perspective == 'nephews-nieces'
          and not parent.has_grandnephew_or_grandniece):
        continue

      data['children'].append(self.serializer_class(parent).data)
      parent_data = data['children'][p_idx]
      parent_data['children'] = []
      p_idx += 1

      ps_idx = 0
      for p_sibling in parent.siblings:  # Add nodes for parent siblings.
        if not p_sibling.has_child:
          continue

        parent_data['children'].append(self.serializer_class(p_sibling).data)
        cousin_data = parent_data['children'][ps_idx]
        cousin_data['children'] = []
        ps_idx += 1

        # Add nodes for parent siblings' children.
        psc_idx = 0
        for ps_child in p_sibling.children:
          cousin_data['children'].append(self.serializer_class(ps_child).data)

          # Add nodes for cousin's children.
          if perspective == 'nephews-nieces':
            cousin_data['children'][psc_idx]['children'] = []
            for c_child in ps_child.children:
              cousin_data['children'][psc_idx]['children'].append(
                  self.serializer_class(c_child).data)

          psc_idx += 1

    return data

  def build_descendant_tree(self, person):
    """Build person's descendants tree."""

    data = self.serializer_class(person).data
    data['children'] = []

    nodes = person.children
    while nodes:
      node = nodes.pop(0)

      # Add descendants.
      data['children'].append(self.build_descendant_tree(node))

    return data

  def build_newphew_niece_tree(self, person):
    """Build person's nephews/nieces tree."""

    data = self.serializer_class(person).data
    data['children'] = []

    s_idx = 0
    for sibling in person.siblings:  # Add nodes for siblings.
      if not sibling.has_child:
        continue

      data['children'].append(self.serializer_class(sibling).data)
      sibling_data = data['children'][s_idx]
      sibling_data['children'] = []
      s_idx += 1

      for s_child in sibling.children:  # Add nodes for siblings' children.
        sibling_data['children'].append(self.serializer_class(s_child).data)

    return data

  def get(self, request, **kwargs):
    """Return tree."""

    view = request.query_params.get('view')

    if view == 'ancestors':
      nodes = self.build_ancestor_tree(self.get_object())
    elif view == 'cousins':
      nodes = self.build_cousin_tree(self.get_object(), perspective='cousins')
    elif view == 'cousin-nephews-nieces':
      nodes = self.build_cousin_tree(self.get_object(),
                                     perspective='nephews-nieces')
    elif view == 'descendants':
      nodes = self.build_descendant_tree(self.get_object())
    elif view == 'nephews-nieces':
      nodes = self.build_newphew_niece_tree(self.get_object())
    else:
      nodes = []

    return Response(nodes)
