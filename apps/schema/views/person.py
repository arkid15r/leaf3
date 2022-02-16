"""Person views."""

from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from apps.schema.forms.person import PersonForm
from apps.schema.models.person import Person
from apps.schema.views.base import (CreateViewBase, DeleteViewBase,
                                    TreePersonNodeMixin, UpdateViewBase)


class Create(CreateViewBase):
  """Person create view."""

  form_class = PersonForm
  model = Person
  template_name = 'schema/person/create.html'
  translations = {
      'add_person': _('Add a person'),
  }
  tree_uid_field = 'tree_uid'

  def get_context_data(self, **kwargs):
    """Generate context."""

    context = super().get_context_data(**kwargs)
    context.update({
        'page_header_primary_text': self.translations['add_person'],
        'page_header_secondary_text': self.tree,
        'page_title': self.translations['add_person'],
    })

    return context

  def get_success_url(self, **unused_kwargs):
    """Generate redirect URL."""

    return self.tree.object_read_url


class Delete(DeleteViewBase):
  """Person delete view."""

  model = Person
  template_name = 'schema/person/delete.html'

  def get_success_url(self):
    """Generate redirect URL."""

    return self.tree.object_read_url


class Update(UpdateViewBase):
  """Person update view."""

  form_class = PersonForm
  model = Person
  template_name = 'schema/person/update.html'
  translations = {
      'edit_person': _('Edit person'),
  }

  def get_context_data(self, **kwargs):
    """Generate context."""

    context = super().get_context_data(**kwargs)
    context.update({
        'page_header_primary_text': self.translations['edit_person'],
        'page_title': self.translations['edit_person'],
    })
    print(self.get_object().aunts_and_uncles)
    return context

  def get_success_url(self):
    """Generate redirect URL."""

    return self.tree.object_read_url


class View(TreePersonNodeMixin, TemplateView):
  """Person view."""

  model = Person
  template_name = 'schema/person/view.html'
