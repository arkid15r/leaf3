"""User models."""

from django.contrib.auth.models import AbstractUser

from apps.core.models import TimestampModel, UIDModel


class User(AbstractUser, TimestampModel, UIDModel):
  """User model."""
