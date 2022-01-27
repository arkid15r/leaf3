"""Schema views base."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

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


class CreateViewBase(TreeMixin, CreateView):
  """Create view base."""

  def form_valid(self, form):
    """Validate form."""

    form.instance.tree_uid = self.kwargs['tree_uid']
    return super().form_valid(form)

  def get_context_data(self, **kwargs):
    """Generate context."""

    context = super().get_context_data(**kwargs)
    context.update({'tree': self.tree})

    return context

  def get_form_kwargs(self):
    """Get form kwargs."""

    kwargs = super().get_form_kwargs()
    kwargs['tree_uid'] = self.kwargs['tree_uid']

    return kwargs


class DeleteViewBase(TreeNodeMixin, DeleteView):
  """Delete view base."""


class ListViewBase(TreeNodesMixin, ListView):
  """List view base."""

  paginate_by = 10

  def get_context_data(self, **kwargs):
    """Get context."""

    context = super().get_context_data(**kwargs)
    context['tree'] = self.tree

    return context


class UpdateViewBase(TreeNodeMixin, UpdateView):
  """Update view base."""

  def get_context_data(self, **kwargs):
    """Generate context."""

    context = super().get_context_data(**kwargs)
    context.update({'tree': self.tree})

    return context

  def get_form_kwargs(self):
    """Get form kwargs."""

    kwargs = super().get_form_kwargs()
    kwargs['tree_uid'] = self.kwargs['tree_uid']

    return kwargs
