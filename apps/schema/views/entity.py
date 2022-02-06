"""Entity views."""

from django.utils.translation import gettext_lazy as _

from apps.schema.forms.entity import EntityForm
from apps.schema.models.entity import Entity
from apps.schema.views.base import (CreateViewBase, DeleteViewBase,
                                    ListDataTableViewBase, UpdateViewBase)


class Create(CreateViewBase):
  """Entity create view."""

  form_class = EntityForm
  model = Entity
  template_name = 'schema/entity/create.html'
  translations = {
      'add_entity': _('Add an entity'),
  }
  tree_uid_field = 'tree_uid'

  def get_context_data(self, **kwargs):
    """Generate context."""

    context = super().get_context_data(**kwargs)
    context.update({
        'page_header_primary_text': self.translations['add_entity'],
        'page_header_secondary_text': self.tree,
        'page_title': self.translations['add_entity'],
    })

    return context

  def get_success_url(self, **unused_kwargs):
    """Generate redirect URL."""

    return self.tree.entity_list_url


class Delete(DeleteViewBase):
  """Entity delete view."""

  model = Entity
  template_name = 'schema/entity/delete.html'

  def get_success_url(self):
    """Generate redirect URL."""

    return self.tree.entity_list_url


class List(ListDataTableViewBase):
  """Entity list view."""

  model = Entity
  template_name = 'schema/entity/list.html'
  tree_uid_field = 'tree_uid'


class Update(UpdateViewBase):
  """Entity update view."""

  form_class = EntityForm
  model = Entity
  template_name = 'schema/entity/update.html'
  translations = {
      'edit_entry': _('Edit entity'),
  }

  def get_context_data(self, **kwargs):
    """Generate context."""

    context = super().get_context_data(**kwargs)
    context.update({
        'page_header_primary_text': self.translations['edit_entry'],
        'page_header_secondary_text': self.tree,
        'page_title': self.translations['edit_entry'],
    })

    return context

  def get_success_url(self):
    """Generate redirect URL."""

    return self.tree.entity_list_url
