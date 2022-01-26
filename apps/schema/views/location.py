"""Location views."""

from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from apps.schema.forms.location import LocationForm
from apps.schema.models.location import Location
from apps.schema.views.base import TreeMixin, TreeNodeMixin, TreeNodesMixin


class Create(TreeMixin, CreateView):
  """Location create view."""

  form_class = LocationForm
  model = Location
  template_name = 'schema/location/create.html'

  def form_valid(self, form):
    """Validate form."""

    form.instance.tree_uid = self.kwargs['tree_uid']
    return super().form_valid(form)

  def get_context_data(self, **kwargs):
    """Generate context."""

    context = super().get_context_data(**kwargs)
    context.update({'tree': self.tree})

    return context

  def get_success_url(self, **unused_kwargs):
    """Generate redirect URL."""

    return reverse('location-list', args=(self.kwargs['tree_uid'],))


class List(TreeNodesMixin, ListView):
  """Location list view."""

  model = Location
  ordering = ('street', 'city', 'state', 'country')
  paginate_by = 5
  template_name = 'schema/location/list.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['tree'] = self.tree

    return context


class Edit(TreeNodeMixin, UpdateView):
  """Location edit view."""

  form_class = LocationForm
  model = Location
  template_name = 'schema/location/edit.html'

  def get_context_data(self, **kwargs):
    """Generate context."""

    context = super().get_context_data(**kwargs)
    context.update({'tree': self.tree})

    return context

  def get_success_url(self):
    """Generate redirect URL."""

    return reverse('location-list', args=(self.kwargs['tree_uid'],))


class Delete(TreeNodeMixin, DeleteView):
  """Location delete view."""

  model = Location
  template_name = 'schema/location/delete.html'

  def get_success_url(self):
    """Generate redirect URL."""

    return reverse('location-list', args=(self.kwargs['tree_uid'],))
