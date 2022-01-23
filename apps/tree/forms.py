"""Tree forms."""

from django.forms import ModelForm

from apps.tree.models import Tree


class TreeForm(ModelForm):
  """Tree form."""

  class Meta:
    model = Tree
    fields = ('name', 'description')
