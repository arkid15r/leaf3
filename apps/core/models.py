"""Core models."""

from django.conf import settings
from django.db import models

from shortuuid.django_fields import ShortUUIDField


class TimestampModel(models.Model):
  """Timestamp model."""

  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  class Meta:
    """Timestamp model meta."""

    abstract = True


class UIDModel(models.Model):
  """UID model."""

  uid = ShortUUIDField(alphabet=settings.SHORT_UUID_ALPHABET,
                       length=settings.SHORT_UUID_LENGTH,
                       max_length=40,
                       primary_key=True)

  class Meta:
    """UID model meta."""

    abstract = True
