"""Entry views."""

from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from apps.schema.forms.entry import EntryForm
from apps.schema.models.entry import Entry
from apps.schema.views.base import TreeMixin, TreeNodeMixin, TreeNodesMixin


class Create(TreeMixin, CreateView):
  """Entry create view."""

  form_class = EntryForm
  model = Entry
  template_name = 'schema/entry/create.html'

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

    return reverse('entry-list', args=(self.kwargs['tree_uid'],))


class List(TreeNodesMixin, ListView):
  """Entry list view."""

  model = Entry
  ordering = 'created'
  paginate_by = 5
  template_name = 'schema/entry/list.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['tree'] = self.tree

    return context


class Edit(TreeNodeMixin, UpdateView):
  """Entry edit view."""

  form_class = EntryForm
  model = Entry
  template_name = 'schema/entry/edit.html'

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

    return reverse('entry-list', args=(self.kwargs['tree_uid'],))


class Delete(TreeNodeMixin, DeleteView):
  """Entry delete view."""

  model = Entry
  template_name = 'schema/entry/delete.html'

  def get_success_url(self):
    """Generate redirect URL."""

    return reverse('entry-list', args=(self.kwargs['tree_uid'],))
