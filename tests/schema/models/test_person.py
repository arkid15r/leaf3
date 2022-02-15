"""Schema person model tests."""

# pylint: disable=missing-function-docstring

from datetime import datetime
from unittest.mock import PropertyMock, patch

import time_machine

from apps.schema.models.person import Person
from tests.base import TestCase


class PersonModelTests(TestCase):
  """Person model tests."""

  @time_machine.travel('2020-01-02')
  def test_age__birth_date(self):
    person = Person()

    with patch.object(person, 'birth_date', datetime(2000, 1, 3)):
      self.assertEqual(person.age, 19,
                       'Must be lower on a day before the birth day.')

    with patch.object(person, 'birth_date', datetime(2000, 1, 2)):
      self.assertEqual(person.age, 20, 'Must be equal on the birth day.')

    with patch.object(person, 'birth_date', datetime(2000, 1, 1)):
      self.assertEqual(person.age, 20,
                       'Must be equal on a day after the birth day.')

  @time_machine.travel('2020-01-02')
  def test_age__birth_year(self):
    person = Person()
    person.birth_year = 2000
    person.death_year = None
    self.assertEqual(person.age, 20,
                     'Must match for a person with known birth year.')

  @time_machine.travel('2020-01-02')
  def test_age__birth_date_death_date(self):
    person = Person()
    with patch.object(person, 'birth_date', datetime(1900, 1, 2)):
      with patch.object(person, 'death_date', datetime(1980, 1, 1)):
        self.assertEqual(person.age, 79,
                         'Must be equal on a day after the birth day.')

  @time_machine.travel('2020-01-02')
  def test_age__birth_year_death_year(self):
    person = Person()
    person.birth_year = 1900
    person.death_year = 1980
    self.assertEqual(person.age, 80,
                     'Must match for a person with known birth/death years.')

  @time_machine.travel('2020-01-02')
  def test_age__birth_year_no_death_year(self):
    person = Person()
    person.birth_year = 1900
    person.death_year = Person.EMPTY_VALUE
    self.assertIsNone(person.age,
                      'Must be None for a person with unknown death year.')

  @time_machine.travel('2020-01-02')
  def test_age__no_birth_year_death_year(self):
    person = Person()
    person.birth_year = Person.EMPTY_VALUE
    person.death_year = 2000
    self.assertIsNone(person.age,
                      'Must be None for a person with unknown birth year.')

  @time_machine.travel('2020-01-02')
  def test_age__no_birth_year_no_death_year(self):
    person = Person()
    person.birth_year = Person.EMPTY_VALUE
    person.death_year = Person.EMPTY_VALUE
    self.assertIsNone(
        person.age, 'Must be None for a person with unknown birth/death years.')

  @patch.object(Person, 'children', new_callable=PropertyMock)
  @time_machine.travel('2020-01-02')
  def test_summary(self, mock_children):
    mock_children.return_value = (Person(), Person(), Person())
    person = Person()

    person.birth_year = 1899
    person.death_year = 2001
    for gender in (Person.FEMALE, Person.MALE):
      person.gender = gender
      self.assertEqual(person.summary,
                       'died in 2001 in the age of 102 years, 3 children')

    person.birth_year = None
    person.death_year = 2001
    for gender in (Person.FEMALE, Person.MALE):
      person.gender = gender
      self.assertEqual(person.summary, 'died in 2001, 3 children')

    person.birth_year = 1970
    person.death_year = None
    self.assertEqual(person.summary, '50 years, 3 children')

    person.birth_year = 1870
    person.death_year = Person.EMPTY_VALUE
    self.assertEqual(person.summary, 'born in 1870, 3 children')

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
