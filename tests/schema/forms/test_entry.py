"""Schema entry forms tests."""

# pylint: disable=missing-function-docstring
from unittest.mock import MagicMock

from apps.schema.forms.entry import EntryForm
from apps.schema.models.entry import Entry
from tests.base import TestCase


class EntryFormTests(TestCase):
  """Entry form tests."""

  def test_required_fields(self):
    form = EntryForm(tree=MagicMock(), data={'event_uid': Entry.EVENT_STARTED})

    self.assertFalse(form.is_valid())
    errors = form.errors.as_data()

    self.assertEqual(errors['__all__'][0].code,
                     EntryForm.ERROR_CODE_ONE_OF_FIELDS_REQUIRED)
