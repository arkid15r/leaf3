"""Schema person forms tests."""

# pylint: disable=missing-function-docstring
import copy
from datetime import datetime
from unittest.mock import MagicMock

from dateutil.relativedelta import relativedelta

from apps.schema.forms.person import PersonForm
from apps.schema.models.person import Person
from tests.base import TestCase


class PersonFormTests(TestCase):
  """Person form tests."""

  data = {'first_name': 'First', 'gender': Person.FEMALE, 'last_name': 'Last'}

  def _test_year_invalid(self, field_name):
    data = copy.copy(self.data)

    invalid_values = ('2222-', 'year', '.', '123')
    for value in invalid_values:
      data.update({field_name: value})

      form = PersonForm(data, tree=MagicMock())
      self.assertFalse(form.is_valid())

      errors = form.errors.as_data()
      self.assertIn(
          f'{value} is not a valid value, it must be either a year or -',
          str(errors[field_name][0]))

  def _test_year_valid(self, field_name):
    data = copy.copy(self.data)

    valid_values = (Person.EMPTY_VALUE, 1800, 2222)
    for value in valid_values:
      data.update({field_name: value})

      form = PersonForm(data, tree=MagicMock())
      self.assertTrue(form.is_valid())
      self.assertFalse(form.errors)

  def _test_year_match_invalid(self, event_name):
    data = copy.copy(self.data)

    now = datetime.now()
    invalid_values = ({'date': now, 'year': '1900'}, {'date': now, 'year': '-'})
    for value in invalid_values:
      data[f'{event_name}_date'] = value['date']
      data[f'{event_name}_year'] = value['year']

      form = PersonForm(data, tree=MagicMock())
      self.assertFalse(form.is_valid())
      self.assertEqual(
          form.errors['__all__'][0],
          f'The {event_name} year and {event_name} date year must match.')

  def _test_year_match_valid(self, event_name):
    data = copy.copy(self.data)

    data[f'{event_name}_date'] = datetime.now()
    data[f'{event_name}_year'] = datetime.now().year

    form = PersonForm(data, tree=MagicMock())
    self.assertTrue(form.is_valid())
    self.assertFalse(form.errors)

  def test_birth_year__invalid(self):
    self._test_year_invalid('birth_year')
    self._test_year_valid('birth_year')

  def test_birth_year__valid(self):
    self._test_year_valid('birth_year')

  def test_death_year__invalid(self):
    self._test_year_invalid('death_year')

  def test_death_year__valid(self):
    self._test_year_valid('death_year')

  def test_birth_year_match__invalid(self):
    self._test_year_match_invalid('birth')

  def test_birth_year_match__valid(self):
    self._test_year_match_valid('birth')

  def test_death_year_match__invalid(self):
    self._test_year_match_invalid('death')

  def test_death_year_match__valid(self):
    self._test_year_match_valid('death')

  def test_first_name_last_name__invalid(self):
    data = copy.copy(self.data)

    data['first_name'] = ''
    data['last_name'] = ''
    form = PersonForm(data, tree=MagicMock())
    self.assertFalse(form.is_valid())
    self.assertEqual(form.errors['__all__'][0],
                     'Either first name or last name is required.')

  def test_first_name_last_name__valid(self):
    data = copy.copy(self.data)

    valid_values = ({
        'first_name': 'First',
        'last_name': 'Last'
    }, {
        'first_name': 'First',
        'last_name': ''
    }, {
        'first_name': '',
        'last_name': 'Last'
    })
    for value in valid_values:
      data['first_name'] = value['first_name']
      data['last_name'] = value['last_name']

      form = PersonForm(data, tree=MagicMock())
      self.assertTrue(form.is_valid())

  def test_death_date_burial_date__invalid(self):
    data = copy.copy(self.data)

    now = datetime.now()
    data['burial_date'] = now - relativedelta(days=1)
    data['death_date'] = now.date()
    data['death_year'] = now.year

    form = PersonForm(data, tree=MagicMock())
    self.assertFalse(form.is_valid())
    self.assertEqual(form.errors['__all__'][0],
                     'The burial date cannot be earlier than death date.')

  def test_death_date_burial_date__valid(self):
    data = copy.copy(self.data)

    now = datetime.now()
    data['burial_date'] = now + relativedelta(days=1)
    data['death_date'] = now.date()
    data['death_year'] = now.year

    form = PersonForm(data, tree=MagicMock())
    self.assertTrue(form.is_valid())
