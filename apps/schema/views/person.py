"""Person views."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from apps.schema.forms.person import PersonForm
from apps.schema.models.person import Person
from apps.schema.views.base import GetTreeObjectMixin, GetTreeQuerySetMixin
from apps.tree.models import Tree


class Create(LoginRequiredMixin, GetTreeObjectMixin, CreateView):
  """Person create view."""

  form_class = PersonForm
  model = Person
  template_name = 'schema/person/create.html'

  def form_valid(self, form):
    """Validate form."""

    form.instance.tree_uid = self.kwargs['tree_uid']
    return super().form_valid(form)

  def get_context_data(self, **kwargs):
    """Generate context."""

    try:
      tree = Tree.nodes.get(creator_uid=self.request.user.uid,
                            uid=self.kwargs['tree_uid'])
    except Tree.DoesNotExist:
      raise Http404

    context = super().get_context_data(**kwargs)
    context.update({'tree': tree})

    return context

  def get_form_kwargs(self):
    """Get form kwargs."""

    kwargs = super().get_form_kwargs()
    kwargs['tree_uid'] = self.kwargs['tree_uid']

    return kwargs

  def get_success_url(self, **unused_kwargs):
    """Generate redirect URL."""

    return reverse('person-list', args=(self.kwargs['tree_uid'],))


class List(LoginRequiredMixin, GetTreeQuerySetMixin, ListView):
  """Person list view."""
  model = Person
  paginate_by = 5
  template_name = 'schema/person/list.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['tree'] = self.tree

    return context


class Edit(LoginRequiredMixin, GetTreeObjectMixin, UpdateView):
  """Person edit view."""

  form_class = PersonForm
  model = Person
  template_name = 'schema/person/edit.html'

  def get_context_data(self, **kwargs):
    """Generate context."""

    try:
      tree = Tree.nodes.get(creator_uid=self.request.user.uid,
                            uid=self.kwargs['tree_uid'])
    except Tree.DoesNotExist:
      raise Http404

    context = super().get_context_data(**kwargs)
    context.update({'tree': tree})
    print(context['form'].errors)
    return context

  def get_form_kwargs(self):
    """Get form kwargs."""

    kwargs = super().get_form_kwargs()
    kwargs['tree_uid'] = self.kwargs['tree_uid']

    return kwargs

  def get_success_url(self):
    """Generate redirect URL."""

    return reverse('person-list', args=(self.kwargs['tree_uid'],))


class Delete(LoginRequiredMixin, GetTreeObjectMixin, DeleteView):
  """Person delete view."""

  model = Person
  template_name = 'schema/person/delete.html'

  def get_success_url(self):
    """Generate redirect URL."""

    return reverse('person-list', args=(self.kwargs['tree_uid'],))
