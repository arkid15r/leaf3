"""Core models."""

from django.db import models


class TimestampedModel(models.Model):
  """Timestamped model."""

  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  class Meta:
    """Timestamped model meta."""

    abstract = True
