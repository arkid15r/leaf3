"""User models."""

from django.contrib.auth.models import AbstractUser

from apps.core.models import TimestampModel


class User(AbstractUser, TimestampModel):
  """User model."""
