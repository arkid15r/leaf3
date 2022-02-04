"""Schema views base."""

from django.http import Http404
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from apps.tree.views import TreeMixin


class TreeNodeMixin(TreeMixin):
  """Tree node mixin."""

  tree_uid_field = 'tree_uid'

  def get_object(self):
    """Get object."""

    try:
      return self.model.nodes.get(tree_uid=self.tree.uid, uid=self.kwargs['pk'])
    except self.model.DoesNotExist:
      raise Http404


class TreeNodesMixin(TreeMixin):
  """Tree nodes mixin."""

  tree_uid_field = 'tree_uid'

  def get_queryset(self):
    """Get queryset."""

    return self.model.nodes.filter(tree_uid=self.tree.uid)


class CreateViewBase(TreeMixin, CreateView):
  """Create view base."""

  def form_valid(self, form):
    """Validate form."""

    form.instance.tree_uid = self.tree.uid
    return super().form_valid(form)

  def get_form_kwargs(self):
    """Get form kwargs."""

    kwargs = super().get_form_kwargs()
    kwargs['tree'] = self.tree
    return kwargs


class DeleteViewBase(TreeNodeMixin, DeleteView):
  """Delete view base."""


class ListViewBase(TreeNodesMixin, ListView):
  """List view base."""


class UpdateViewBase(TreeNodeMixin, UpdateView):
  """Update view base."""

  def get_form_kwargs(self):
    """Get form kwargs."""

    kwargs = super().get_form_kwargs()
    kwargs['tree'] = self.tree
    return kwargs
