"""User forms."""

from allauth.account import forms


def get_form_class(cls, exclude_fields=None):
  """Class factory."""

  class NoLabelForm(cls):
    """Remove label from form fields."""

    def __init__(self, *args, **kwargs):
      super(NoLabelForm, self).__init__(*args, **kwargs)

      for field in self.fields:
        if exclude_fields and field in exclude_fields:
          continue

        self.fields[field].label = ''

  return NoLabelForm


LoginForm = get_form_class(forms.LoginForm, exclude_fields=('remember',))
SignupForm = get_form_class(forms.SignupForm)
