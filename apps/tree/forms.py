"""Tree forms."""

from django import forms

from apps.tree.models import Tree


class TreeForm(forms.ModelForm):
  """Tree form."""

  class Meta:
    """Tree form meta."""

    fields = (
        'name',
        'description',
    )
    model = Tree
