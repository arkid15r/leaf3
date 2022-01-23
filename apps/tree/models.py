"""Tree models."""

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from apps.core.models import TimestampModel, UIDModel


class Tree(TimestampModel, UIDModel):
  """Tree model."""

  creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
  description = models.TextField(max_length=100, blank=True, null=True)
  name = models.CharField(max_length=50, null=False)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('tree-manage', args=(self.uid,))

  class Meta:
    """Tree model meta."""

    db_table = 'trees'
    verbose_name = _('Tree')
    verbose_name_plural = _('Trees')
