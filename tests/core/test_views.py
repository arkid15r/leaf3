"""Core views tests."""
# pylint: disable=missing-function-docstring

from django.urls import reverse

from tests.base import TestCaseBase


class TestCoreViews(TestCaseBase):
  """Test core app views."""

  def test_about_get_success(self):
    response = self.client.get(reverse('about'))
    self.assertEqual(response.status_code, 200)

  def test_main_get_success(self):
    response = self.client.get(reverse('main'))
    self.assertEqual(response.status_code, 200)
