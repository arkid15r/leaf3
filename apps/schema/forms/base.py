"""Schema forms base."""

from django import forms


class TreeFormBase(forms.ModelForm):
  """Tree form base."""

  def __init__(self, *args, **kwargs):
    if 'tree_uid' in kwargs:
      self.tree_uid = kwargs.pop('tree_uid')

    super().__init__(*args, **kwargs)
