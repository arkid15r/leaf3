"""Schema app config."""

from django.apps import AppConfig
from django.db.models.signals import post_save

from apps.schema.models import entity_signals, location_signals, person_signals
from apps.schema.models.entity import Entity
from apps.schema.models.location import Location
from apps.schema.models.person import Person


class SchemaConfig(AppConfig):
  """Schema config."""

  name = 'apps.schema'

  def ready(self):
    post_save.connect(entity_signals.post_save, sender=Entity)
    post_save.connect(location_signals.post_save, sender=Location)
    post_save.connect(person_signals.post_save, sender=Person)
