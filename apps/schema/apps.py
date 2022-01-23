"""Schema app config."""

from django.apps import AppConfig
from django.db.models.signals import post_save

from apps.schema.models import person, person_signals


class SchemaConfig(AppConfig):
  """Schema config."""

  name = 'apps.schema'

  def ready(self):
    post_save.connect(person_signals.post_save, sender=person.Person)
