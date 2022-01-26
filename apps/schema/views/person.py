"""Person views."""

from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from apps.schema.forms.person import PersonForm
from apps.schema.models.person import Person
from apps.schema.views.base import TreeMixin, TreeNodeMixin, TreeNodesMixin


class Create(TreeMixin, CreateView):
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

    context = super().get_context_data(**kwargs)
    context.update({'tree': self.tree})

    return context

  def get_form_kwargs(self):
    """Get form kwargs."""

    kwargs = super().get_form_kwargs()
    kwargs['tree_uid'] = self.kwargs['tree_uid']

    return kwargs

  def get_success_url(self, **unused_kwargs):
    """Generate redirect URL."""

    return reverse('person-list', args=(self.kwargs['tree_uid'],))


class List(TreeNodesMixin, ListView):
  """Person list view."""

  model = Person
  ordering = ('dob', 'last_name', 'first_name')
  paginate_by = 5
  template_name = 'schema/person/list.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['tree'] = self.tree

    return context


class Edit(TreeNodeMixin, UpdateView):
  """Person edit view."""

  form_class = PersonForm
  model = Person
  template_name = 'schema/person/edit.html'

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

  def get_success_url(self):
    """Generate redirect URL."""

    return reverse('person-list', args=(self.kwargs['tree_uid'],))


class Delete(TreeNodeMixin, DeleteView):
  """Person delete view."""

  model = Person
  template_name = 'schema/person/delete.html'

  def get_success_url(self):
    """Generate redirect URL."""

    return reverse('person-list', args=(self.kwargs['tree_uid'],))
