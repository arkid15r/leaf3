"""Tree views."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from apps.tree.forms import TreeForm
from apps.tree.models import Tree


class Create(LoginRequiredMixin, CreateView):
  """Tree create view."""

  form_class = TreeForm
  model = Tree
  success_url = reverse_lazy('tree-dashboard')
  template_name = 'tree/add.html'

  def form_valid(self, form):
    form.instance.creator_uid = self.request.user.uid
    return super().form_valid(form)


class Dashboard(LoginRequiredMixin, ListView):
  """Dashboard view."""

  template_name = "tree/dashboard.html"

  def get_queryset(self):
    return Tree.nodes.filter(
        creator_uid=self.request.user.uid).order_by('-created')


class Delete(LoginRequiredMixin, DeleteView):
  """Tree delete view."""

  model = Tree
  success_url = reverse_lazy('tree-dashboard')
  template_name = 'tree/delete.html'


class Manage(LoginRequiredMixin, TemplateView):
  """Manage tree view."""

  template_name = "tree/manage.html"

  def get_context_data(self, **kwargs):
    """Generate context."""
    try:
      tree = Tree.nodes.get(uid=self.kwargs['pk'],
                            creator_uid=self.request.user.uid)
    except Tree.DoesNotExist:
      raise Http404

    context = super().get_context_data(**kwargs)
    context.update({'tree': tree})

    return context


class Edit(LoginRequiredMixin, UpdateView):
  """Tree edit view."""

  form_class = TreeForm
  model = Tree
  success_url = reverse_lazy('tree-dashboard')
  template_name = 'tree/edit.html'

  def get_object(self, queryset=None):
    """Get object."""

    try:
      return self.model.nodes.get(uid=self.kwargs['pk'])
    except Tree.DoesNotExist:
      raise Http404
