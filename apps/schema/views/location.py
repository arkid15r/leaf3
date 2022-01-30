"""Location views."""

from django.utils.translation import gettext_lazy as _

from apps.schema.forms.location import LocationForm
from apps.schema.models.location import Location
from apps.schema.views.base import (CreateViewBase, DeleteViewBase,
                                    ListViewBase, UpdateViewBase)


class Create(CreateViewBase):
  """Location create view."""

  form_class = LocationForm
  model = Location
  template_name = 'schema/location/create.html'
  translations = {
      'add_location': _('Add a location'),
  }
  tree_uid_field = 'tree_uid'

  def get_context_data(self, **kwargs):
    """Generate context."""

    context = super().get_context_data(**kwargs)
    context.update({
        'page_header_primary_text': self.translations['add_location'],
        'page_title': self.translations['add_location'],
    })

    return context

  def get_success_url(self, **unused_kwargs):
    """Generate redirect URL."""

    return self.tree.location_list_url


class Delete(DeleteViewBase):
  """Location delete view."""

  model = Location
  template_name = 'schema/location/delete.html'

  def get_success_url(self):
    """Generate redirect URL."""

    return self.tree.location_list_url


class List(ListViewBase):
  """Location list view."""

  model = Location
  ordering = ('street', 'town', 'state', 'country')
  template_name = 'schema/location/list.html'


class Update(UpdateViewBase):
  """Location update view."""

  form_class = LocationForm
  model = Location
  template_name = 'schema/location/update.html'
  translations = {
      'edit_location': _('Edit location'),
  }

  def get_context_data(self, **kwargs):
    """Generate context."""

    context = super().get_context_data(**kwargs)
    context.update({
        'page_header_primary_text': self.translations['edit_location'],
        'page_title': self.translations['edit_location'],
    })

    return context

  def get_success_url(self):
    """Generate redirect URL."""

    return self.tree.location_list_url
