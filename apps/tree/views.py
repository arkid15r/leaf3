"""Tree views."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from apps.tree.forms import TreeForm
from apps.tree.models import Tree


class TreeMixin(LoginRequiredMixin):
  """Tree mixin."""

  tree_uid_field = 'pk'

  def dispatch(self, request, *args, **kwargs):
    if not request.user.is_authenticated:
      return super().dispatch(request, *args, **kwargs)

    try:
      self.tree = Tree.nodes.get(creator_uid=self.request.user.uid,
                                 uid=kwargs.pop(self.tree_uid_field))
    except Tree.DoesNotExist:
      raise Http404

    return super().dispatch(request, *args, **kwargs)

  def get_context_data(self, **kwargs):
    """Generate context."""

    context = super().get_context_data(**kwargs)
    context.update({'tree': self.tree})
    return context


class Create(LoginRequiredMixin, CreateView):
  """Tree create view."""

  form_class = TreeForm
  model = Tree
  success_url = reverse_lazy('tree-dashboard')
  template_name = 'tree/create.html'
  translations = {
      'add_tree': _('Create a tree'),
  }

  def form_valid(self, form):
    form.instance.creator_uid = self.request.user.uid
    return super().form_valid(form)

  def get_context_data(self, **kwargs):
    """Generate context."""

    context = super().get_context_data(**kwargs)
    context.update({
        'button_submit_text': _('Create'),
        'page_header_primary_text': self.translations['add_tree'],
        'page_title': self.translations['add_tree'],
    })

    return context


class Dashboard(LoginRequiredMixin, ListView):
  """Dashboard view."""

  template_name = "tree/list.html"

  def get_queryset(self):
    return Tree.nodes.filter(
        creator_uid=self.request.user.uid).order_by('-created')


class Delete(TreeMixin, DeleteView):
  """Tree delete view."""

  model = Tree
  success_url = reverse_lazy('tree-dashboard')
  template_name = 'tree/delete.html'

  def get_object(self, queryset=None):
    """Get object."""

    try:
      return self.model.nodes.get(uid=self.kwargs['pk'])
    except self.model.DoesNotExist:
      raise Http404


class View(TreeMixin, TemplateView):
  """View tree view."""

  template_name = "tree/view.html"


class Update(TreeMixin, UpdateView):
  """Tree update view."""

  form_class = TreeForm
  model = Tree
  success_url = reverse_lazy('tree-dashboard')
  template_name = 'tree/update.html'
  translations = {
      'edit_tree': _('Edit tree'),
  }

  def get_context_data(self, **kwargs):
    """Generate context."""

    context = super().get_context_data(**kwargs)
    context.update({
        'page_header_primary_text': self.translations['edit_tree'],
        'page_title': self.translations['edit_tree'],
    })

    return context

  def get_object(self, queryset=None):
    """Get object."""

    try:
      return self.model.nodes.get(uid=self.kwargs['pk'])
    except Tree.DoesNotExist:
      raise Http404
