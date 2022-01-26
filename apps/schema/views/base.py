"""Schema views base."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

from apps.tree.models import Tree


class TreeMixin(LoginRequiredMixin):
  """Tree mixin."""

  def dispatch(self, request, *args, **kwargs):
    """Dispatch method"""

    if not request.user.is_authenticated:
      return super(TreeMixin, self).dispatch(request, *args, **kwargs)

    try:
      self.tree = Tree.nodes.get(creator_uid=self.request.user.uid,
                                 uid=self.kwargs['tree_uid'])
    except Tree.DoesNotExist:
      raise Http404

    return super(TreeMixin, self).dispatch(request, *args, **kwargs)


class TreeNodeMixin(TreeMixin):
  """Tree node mixin."""

  def get_object(self):
    """Get object."""

    try:
      return self.model.nodes.get(tree_uid=self.tree.uid, uid=self.kwargs['pk'])
    except self.model.DoesNotExist:
      raise Http404


class TreeNodesMixin(TreeMixin):
  """Tree nodes mixin."""

  def get_queryset(self):
    """Get queryset."""

    return self.model.nodes.filter(tree_uid=self.tree.uid)
