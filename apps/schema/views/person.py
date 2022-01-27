"""Person views."""

from django.utils.translation import gettext_lazy as _

from apps.schema.forms.person import PersonForm
from apps.schema.models.person import Person
from apps.schema.views.base import (CreateViewBase, DeleteViewBase,
                                    ListViewBase, UpdateViewBase)


class Create(CreateViewBase):
  """Person create view."""

  form_class = PersonForm
  model = Person
  template_name = 'schema/person/create.html'
  translations = {
      'add_person': _('Add a person'),
  }

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

    return self.tree.person_list_url


class Delete(DeleteViewBase):
  """Person delete view."""

  model = Person
  template_name = 'schema/person/delete.html'

  def get_success_url(self):
    """Generate redirect URL."""

    return self.tree.person_list_url


class List(ListViewBase):
  """Person list view."""

  model = Person
  ordering = ('dob', 'last_name', 'first_name')
  template_name = 'schema/person/list.html'


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
        'tree': self.tree
    })

    return context

  def get_success_url(self):
    """Generate redirect URL."""

    return self.tree.person_list_url
