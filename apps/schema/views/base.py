"""Schema views base."""

from django.http import Http404
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from apps.schema.models.person import Person
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


class TreePersonNodeMixin(TreeMixin):
  """Tree person node mixin."""

  tree_uid_field = 'tree_uid'

  def dispatch(self, request, *args, **kwargs):
    """Dispatch method."""

    if not request.user.is_authenticated:
      return super().dispatch(request, *args, **kwargs)

    try:
      self.person = Person.nodes.get(tree_uid=self.kwargs['tree_uid'],
                                     uid=kwargs.pop('person_uid'))
    except Person.DoesNotExist:
      raise Http404

    return super().dispatch(request, *args, **kwargs)

  def get_context_data(self, **kwargs):
    """Generate context."""

    context = super().get_context_data(**kwargs)
    context.update({'person': self.person})
    return context


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


class ListDataTableViewBase(TreeMixin, TemplateView):
  """List data table view base."""


class UpdateViewBase(TreeNodeMixin, UpdateView):
  """Update view base."""

  def get_form_kwargs(self):
    """Get form kwargs."""

    kwargs = super().get_form_kwargs()
    kwargs['tree'] = self.tree
    return kwargs
