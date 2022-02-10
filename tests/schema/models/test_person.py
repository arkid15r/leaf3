"""Schema person model tests."""

# pylint: disable=missing-function-docstring

from apps.schema.models.person import Person
from tests.base import TestCase


class PersonModelTests(TestCase):
  """Person model tests."""

  def test_was_alive_in(self):
    person = Person()

    # Invalid argument.
    for year in (None, ''):
      self.assertFalse(person.was_alive_in(year),
                       'Must return False for invalid values.')

    # Unknown birth year.
    person.birth_year = None
    person.death_year = 2000
    for year in ('1900', '2000'):
      self.assertFalse(person.was_alive_in(year),
                       'Must return False if birth year is unknown.')

    # Unknown death year.
    person.birth_year = '1900'
    person.death_year = '-'
    for year in ('1900', '2000'):
      self.assertFalse(person.was_alive_in(year),
                       'Must return False if death year is unknown.')

    # In range.
    person.birth_year = '1900'
    person.death_year = '2000'
    for year in ('1900', '1901', '2000'):
      self.assertTrue(person.was_alive_in(year),
                      'Must return True for valid in range values.')

    # Out of range.
    for year in ('1899', '2001'):
      self.assertFalse(person.was_alive_in(year),
                       'Must return False for valid out of range values.')

    # Person was still alive.
    person.birth_year = '1900'
    person.death_year = None
    for year in ('1900', '1901', '2000'):
      self.assertTrue(person.was_alive_in(year),
                      'Must return True for valid in range values.')

    for year in ('1800', '1899'):
      self.assertFalse(person.was_alive_in(year),
                       'Must return False for valid out range values.')
