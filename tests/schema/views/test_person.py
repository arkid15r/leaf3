"""Schema person views tests."""
# pylint: disable=missing-function-docstring

from django.urls import reverse

from tests.base import TestCaseBase


class TestPersonViews(TestCaseBase):
  """Test person views."""

  def test_login_required(self):
    person_uid = 'person-uid'
    person_uid_url_names = ('person-edit', 'person-delete')
    tree_uid_url_names = ('person-list', 'person-create')
    tree_uid = 'tree-uid'

    for url_name in person_uid_url_names + tree_uid_url_names:
      if url_name in person_uid_url_names:
        url = reverse(url_name, args=(tree_uid, person_uid))
      else:
        url = reverse(url_name, args=(tree_uid,))

      expected_redirect_url = f'{reverse("account_login")}?next={url}'
      response = self.client.get(url)
      self.assertRedirects(response, expected_redirect_url)
