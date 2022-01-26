"""Entity views."""

from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from apps.schema.forms.entity import EntityForm
from apps.schema.models.entity import Entity
from apps.schema.views.base import TreeMixin, TreeNodeMixin, TreeNodesMixin


class Create(TreeMixin, CreateView):
  """Entity create view."""

  form_class = EntityForm
  model = Entity
  template_name = 'schema/entity/create.html'

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

    return reverse('entity-list', args=(self.kwargs['tree_uid'],))


class List(TreeNodesMixin, ListView):
  """Entity list view."""

  model = Entity
  ordering = 'created'
  paginate_by = 5
  template_name = 'schema/entity/list.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['tree'] = self.tree

    return context


class Edit(TreeNodeMixin, UpdateView):
  """Entity edit view."""

  form_class = EntityForm
  model = Entity
  template_name = 'schema/entity/edit.html'

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

    return reverse('entity-list', args=(self.kwargs['tree_uid'],))


class Delete(TreeNodeMixin, DeleteView):
  """Entity delete view."""

  model = Entity
  template_name = 'schema/entity/delete.html'

  def get_success_url(self):
    """Generate redirect URL."""

    return reverse('entity-list', args=(self.kwargs['tree_uid'],))
