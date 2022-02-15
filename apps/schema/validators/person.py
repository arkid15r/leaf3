"""Schema user data validators."""

from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


def validate_year(value):
  """Validate that entered value is either a number or "-"."""

  validator = RegexValidator(
      r'^(-|\d{4})$',
      _('{} is not a valid value, it must be either a year or -').format(value))
  validator(value)
