"""Core models."""

from django.db import models


class TimestampModel(models.Model):
  """Timestamp model."""

  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  class Meta:
    """Timestamp model meta."""

    abstract = True


class UIDModel(models.Model):
  """UID model."""

  uid = models.UUIDField()

  class Meta:
    """UID model meta."""

    abstract = True
