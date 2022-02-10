"""Location models."""

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from neomodel import RelationshipTo, StringProperty

from apps.schema.models.base import TreeNodeModel


class Location(TreeNodeModel):
  """Location model."""

  CATEGORY_ADDRESS = 'street'
  CATEGORY_TOWN = 'town'
  CATEGORY_AREA = 'area'
  CATEGORY_STATE = 'state'
  CATEGORY_COUNTRY = 'country'

  CATEGORIES = {
      CATEGORY_ADDRESS: _('Address'),
      CATEGORY_TOWN: _('Town'),
      CATEGORY_AREA: _('Area'),
      CATEGORY_STATE: _('State'),
      CATEGORY_COUNTRY: _('Country'),
  }
  CATEGORY_CHOICES = tuple((key, value) for key, value in CATEGORIES.items())

  category_uid = StringProperty(choices=CATEGORY_CHOICES)
  name = StringProperty(label=_('Name'), max_length=50)
  parent_uid = StringProperty(max_length=50, required=False)

  # Relationships.
  parent_rel = RelationshipTo('.location.Location', 'LOCATED_IN')

  def __str__(self):  # pylint: disable=invalid-str-returned
    """Location str()."""

    return self.full_address

  def join_fields(self, categories):
    """Returns joined fields."""

    fields = []
    for node in self.chain:
      if categories and node.category_uid not in categories:
        continue
      fields.append(node.name)

    return ', '.join(fields)

  @property
  def chain(self):
    """Return location chain."""

    # *0..5 in relationship determines level of recursion.
    query = f"""
        MATCH (:Location {{ uid: "{self.uid}" }}) -[:LOCATED_IN *0..5]->
              (parent: Location)
        RETURN parent
    """

    nodes, unused_meta = self.cypher(query)
    return [self.inflate(node[0]) for node in nodes]

  @property
  def detailed_address(self):
    """Location detailed address."""

    return self.join_fields(('street', 'town', 'state', 'country'))

  @property
  def full_address(self):
    """Location full address."""

    return self.join_fields(('street', 'town', 'area', 'state', 'country'))

  @property
  def long_address(self):
    """Location long address."""

    return self.join_fields(('town', 'state', 'country'))

  @property
  def object_delete_url(self):
    """Return location delete URL."""

    return reverse_lazy('location-delete', args=(self.tree_uid, self.uid))

  @property
  def object_read_url(self):
    """Return location absolute URL."""

    return reverse_lazy('location', args=(self.tree_uid, self.uid))

  @property
  def object_update_url(self):
    """Return location update URL."""

    return reverse_lazy('location-update', args=(self.tree_uid, self.uid))

  @property
  def parent(self):
    """Return parent location."""

    if not self.parent_uid:
      return

    try:
      return Location.nodes.get(uid=self.parent_uid)
    except Location.DoesNotExist:
      pass

  @property
  def short_address(self):
    """Location short address."""

    return self.join_fields(('town', 'state'))

  class Meta:
    """Location model meta."""

    app_label = 'schema'
    verbose_name = _('Location')
    verbose_name_plural = _('Locations')
