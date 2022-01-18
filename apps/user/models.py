"""User models."""

from django.contrib.auth.models import AbstractUser

from apps.core.models import TimestampedModel


class User(AbstractUser, TimestampedModel):
  """User model."""
