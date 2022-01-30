"""Tree models."""

from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _

from neomodel import StringProperty

from apps.schema.models.base import TimestampModel, UIDModel
from apps.schema.models.entity import Entity
from apps.schema.models.entry import Entry
from apps.schema.models.location import Location
from apps.schema.models.person import Person


class Tree(TimestampModel, UIDModel):
  """Tree model."""

  creator_uid = StringProperty(label=_('Creator UID'))
  description = StringProperty(label=_('Description'), max_length=100)
  name = StringProperty(label=_('Name'), max_length=50, required=True)

  def __str__(self):
    return self.name

  @property
  def entities(self):
    """Return tree entity objects."""

    return Entity.nodes.filter(tree_uid=self.uid)

  @property
  def entity_create_url(self):
    """Return entity create URL."""

    return reverse_lazy('entity-create', args=(self.uid,))

  @property
  def entity_list_url(self):
    """Return entity list URL."""

    return reverse_lazy('entity-list', args=(self.uid,))

  @property
  def entries(self):
    """Return tree entry objects."""
    return Entry.nodes.filter(tree_uid=self.uid)

  @property
  def locations(self):
    """Return tree location objects."""
    return Location.nodes.filter(tree_uid=self.uid).order_by(
        'street', 'town', 'area', 'state', 'country')

  @property
  def location_create_url(self):
    """Return location create URL."""

    return reverse_lazy('location-create', args=(self.uid,))

  @property
  def location_list_url(self):
    """Return location list URL."""

    return reverse_lazy('location-list', args=(self.uid,))

  @property
  def object_read_url(self):
    """Return tree read URL."""

    return reverse('tree-view', args=(self.uid,))

  @property
  def object_delete_url(self):
    """Return tree delete URL."""

    return reverse('tree-delete', args=(self.uid,))

  @property
  def persons(self):
    """Return tree person objects."""

    return Person.nodes.filter(tree_uid=self.uid).order_by(
        'last_name', 'first_name')

  @property
  def person_create_url(self):
    """Return person create URL."""

    return reverse_lazy('person-create', args=(self.uid,))

  @property
  def person_list_url(self):
    """Return person list URL."""

    return reverse_lazy('person-list', args=(self.uid,))

  class Meta:
    """Tree model meta."""

    app_label = 'schema'
    verbose_name = _('Tree')
    verbose_name_plural = _('Trees')
