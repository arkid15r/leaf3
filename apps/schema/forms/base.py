"""Schema forms base."""

from django import forms


class TreeFormBase(forms.ModelForm):
  """Tree form base."""

  def __init__(self, *args, **kwargs):
    if 'tree' in kwargs:
      self.tree = kwargs.pop('tree')

    super().__init__(*args, **kwargs)
