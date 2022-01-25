"""Schema views base."""

from django.http import Http404

from apps.tree.models import Tree


class GetTreeObjectMixin:
  """Get tree object mixin."""

  def get_object(self):
    """Get object."""

    try:
      Tree.nodes.get(creator_uid=self.request.user.uid,
                     uid=self.kwargs['tree_uid'])
    except Tree.DoesNotExist:
      raise Http404

    try:
      return self.model.nodes.get(tree_uid=self.kwargs['tree_uid'],
                                  uid=self.kwargs['pk'])
    except self.model.DoesNotExist:
      raise Http404


class GetTreeQuerySetMixin:
  """Get tree query set mixin."""

  def get_queryset(self):
    """Get queryset."""

    try:
      self.tree = Tree.nodes.get(creator_uid=self.request.user.uid,
                                 uid=self.kwargs['tree_uid'])
    except Tree.DoesNotExist:
      raise Http404

    return self.model.nodes.filter(tree_uid=self.tree.uid)
