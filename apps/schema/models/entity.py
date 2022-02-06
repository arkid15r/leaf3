"""Entity models."""

from django.conf import settings
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from neomodel import RelationshipTo, StringProperty

from apps.schema.models.base import TreeNodeModel
from apps.schema.models.location import Location


class Entity(TreeNodeModel):
  """Entity model."""

  CATEGORY_BUSINESS = 'business'
  CATEGORY_EDUCATION = 'education'
  CATEGORY_EMPLOYMENT = 'employment'
  CATEGORY_ORGANIZATION = 'organization'

  CATEGORIES = (
      (CATEGORY_BUSINESS, _('Business')),
      (CATEGORY_EDUCATION, _('Education')),
      (CATEGORY_EMPLOYMENT, _('Employment')),
      (CATEGORY_ORGANIZATION, _('Organization')),
  )

  name = StringProperty(label=_('Name'), max_length=50, required=True)
  summary = StringProperty(label=_('Summary'), max_length=100)
  details = StringProperty(label=_('Details'), max_length=1000)
  url = StringProperty(label=_('URL'), max_length=1000)

  category_uid = StringProperty(choices=CATEGORIES)
  location_uid = StringProperty(max_length=settings.SHORT_UUID_LENGTH)

  # Relationships.
  location_rel = RelationshipTo('.location.Location', 'LOCATED')

  def __str__(self):  # pylint: disable=invalid-str-returned
    """Entity str()."""

    return self.name

  @property
  def category(self):  # pylint: disable=invalid-overridden-method
    """Return entity category."""

    for key, title in self.CATEGORIES:
      if key == self.category_uid:
        return title

  @property
  def location(self):
    """Return entity location."""

    if not self.location_uid:
      return

    try:
      return Location.nodes.get(uid=self.location_uid)
    except Location.DoesNotExist:
      pass

  @property
  def object_delete_url(self):
    """Return entity delete URL."""

    return reverse_lazy('entity-delete', args=(self.tree_uid, self.uid))

  @property
  def object_read_url(self):
    """Return entity read URL."""

    return reverse_lazy('entity', args=(self.tree_uid, self.uid))

  @property
  def object_update_url(self):
    """Return entity update URL."""

    return reverse_lazy('entity-update', args=(self.tree_uid, self.uid))

  class Meta:
    """Entity model meta."""

    app_label = 'schema'
    verbose_name = _('Entity')
    verbose_name_plural = _('Entities')
