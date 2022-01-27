"""Schema location views tests."""
# pylint: disable=missing-function-docstring

from django.urls import reverse

from tests.base import TestCaseBase


class TestLocationViews(TestCaseBase):
  """Test location views."""

  def test_login_required(self):
    location_uid = 'location-uid'
    location_uid_url_names = ('location-edit', 'location-delete')
    tree_uid_url_names = ('location-list', 'location-create')
    tree_uid = 'tree-uid'

    for url_name in location_uid_url_names + tree_uid_url_names:
      if url_name in location_uid_url_names:
        url = reverse(url_name, args=(tree_uid, location_uid))
      else:
        url = reverse(url_name, args=(tree_uid,))

      expected_redirect_url = f'{reverse("account_login")}?next={url}'
      response = self.client.get(url)
      self.assertRedirects(response, expected_redirect_url)
