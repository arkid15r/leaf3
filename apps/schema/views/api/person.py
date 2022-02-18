"""Person API views."""

from django.utils.translation import gettext_lazy as _

from rest_framework.response import Response
from rest_framework.views import APIView

from apps.schema.models.person import Person
from apps.schema.serializers import person
from apps.schema.views.api.base import DataTableListBase, SerializedDataView
from apps.schema.views.base import TreeNodeMixin


class DataTableList(DataTableListBase):
  """Person list API endpoint."""

  model = Person
  name = _('Persons')
  order_by_fields = ('name', 'birth_year', 'birth_place', 'residence')
  search_fields = ('first_name', 'last_name', 'maiden_name', 'death_cause',
                   'birth_year')
  serializer_class = person.ListItemSerializer


class Item(TreeNodeMixin, SerializedDataView):
  """Person item API endpoint."""

  model = Person
  name = _('Person')
  serializer_class = person.ItemSerializer

  def get(self, request, **kwargs):
    """Return person."""

    return Response(self.serialize(self.get_object()))


class SimpleTree(TreeNodeMixin, SerializedDataView):
  """Person simple tree API endpoint."""

  model = Person
  name = _('Simple tree')
  serializer_class = person.TreeNodeSerializer

  def build_ancestor_tree(self, person):
    """Build person's ancestors tree.

    The "children" attribute of a node is required in order to get the tree
    visualized properly. Apparently it contains parents of each person.
    """

    data = self.serialize(person)
    data['children'] = []

    nodes = person.parents
    while nodes:
      node = nodes.pop(0)

      # Add ancestors.
      data['children'].append(self.build_ancestor_tree(node))

      # Add siblings.
      for sibling in node.siblings:
        data['children'].append(self.serialize(sibling))

    return data

  def build_cousin_tree(self, person, perspective='cousins'):
    """Build person's cousins tree."""

    data = self.serialize(person)
    data['children'] = []

    p_idx = 0
    for parent in person.parents:  # Add nodes for parents.
      if not parent.has_nephew_or_niece:
        continue

      if (perspective == 'nephews-nieces'
          and not parent.has_grandnephew_or_grandniece):
        continue

      data['children'].append(self.serialize(parent))
      parent_data = data['children'][p_idx]
      parent_data['children'] = []
      p_idx += 1

      ps_idx = 0
      for p_sibling in parent.siblings:  # Add nodes for parent siblings.
        if not p_sibling.has_child:
          continue
        if perspective == 'nephews-nieces' and not p_sibling.has_grandchild:
          continue

        parent_data['children'].append(self.serialize(p_sibling))
        cousin_data = parent_data['children'][ps_idx]
        cousin_data['children'] = []
        ps_idx += 1

        # Add nodes for parent siblings' children.
        psc_idx = 0
        for ps_child in p_sibling.children:
          if perspective == 'nephews-nieces' and not ps_child.has_child:
            continue

          cousin_data['children'].append(self.serialize(ps_child))

          # Add nodes for cousin's children.
          if perspective == 'nephews-nieces':
            cousin_data['children'][psc_idx]['children'] = []
            for c_child in ps_child.children:
              cousin_data['children'][psc_idx]['children'].append(
                  self.serialize(c_child))

          psc_idx += 1

    return data

  def build_descendant_tree(self, person):
    """Build person's descendants tree."""

    data = self.serialize(person)
    data['children'] = []

    nodes = person.children
    while nodes:
      node = nodes.pop(0)

      # Add descendants.
      data['children'].append(self.build_descendant_tree(node))

    return data

  def build_newphew_niece_tree(self, person):
    """Build person's nephews/nieces tree."""

    data = self.serialize(person)
    data['children'] = []

    s_idx = 0
    for sibling in person.siblings:  # Add nodes for siblings.
      if not sibling.has_child:
        continue

      data['children'].append(self.serialize(sibling))
      sibling_data = data['children'][s_idx]
      sibling_data['children'] = []
      s_idx += 1

      for s_child in sibling.children:  # Add nodes for siblings' children.
        sibling_data['children'].append(self.serialize(s_child))

    return data

  def build_second_cousin_tree(self, person):
    """Build person's second cousins tree."""

    data = self.serialize(person)
    data['children'] = []

    # Add nodes for parents.
    p_idx = 0
    for parent in person.parents:
      if not parent.has_cousin_nephew_or_niece:
        continue

      data['children'].append(self.serialize(parent))
      parent_data = data['children'][p_idx]
      parent_data['children'] = []
      p_idx += 1

      # Add nodes for grandparents.
      gp_idx = 0
      for grandparent in parent.parents:
        if not grandparent.has_nephew_or_niece:
          continue

        parent_data['children'].append(self.serialize(grandparent))
        grandparent_data = parent_data['children'][gp_idx]
        grandparent_data['children'] = []
        gp_idx += 1

        # Add nodes for grandparent siblings' children.
        gps_idx = 0
        for gp_sibling in grandparent.siblings:
          if not gp_sibling.has_grandchild:
            continue

          grandparent_data['children'].append(self.serialize(gp_sibling))
          second_cousin_parent_data = grandparent_data['children'][gps_idx]
          second_cousin_parent_data['children'] = []
          gps_idx += 1

          # Add nodes for grandparent siblings' grandchildren.
          gpc_idx = 0
          for gps_child in gp_sibling.children:
            if not gps_child.has_child:
              continue

            second_cousin_parent_data['children'].append(
                self.serialize(gps_child))
            second_cousin_data = second_cousin_parent_data['children'][gpc_idx]
            second_cousin_data['children'] = []
            gpc_idx += 1

            for second_cousin in gps_child.children:
              second_cousin_data['children'].append(
                  self.serialize(second_cousin))

    return data

  def get(self, request, **kwargs):
    """Return tree."""

    nodes = []
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
    elif view == 'second-cousins':
      nodes = self.build_second_cousin_tree(self.get_object())

    return Response(nodes)
