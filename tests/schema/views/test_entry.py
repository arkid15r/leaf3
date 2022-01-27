"""Schema entry views tests."""
# pylint: disable=missing-function-docstring

from django.urls import reverse

from tests.base import TestCaseBase


class TestEntryViews(TestCaseBase):
  """Test entry views."""

  def test_login_required(self):
    entry_uid = 'entry-uid'
    entry_uid_url_names = ('entry-update', 'entry-delete')
    tree_uid_url_names = ('entry-list', 'entry-create')
    tree_uid = 'tree-uid'

    for url_name in entry_uid_url_names + tree_uid_url_names:
      if url_name in entry_uid_url_names:
        url = reverse(url_name, args=(tree_uid, entry_uid))
      else:
        url = reverse(url_name, args=(tree_uid,))

      expected_redirect_url = f'{reverse("account_login")}?next={url}'
      response = self.client.get(url)
      self.assertRedirects(response, expected_redirect_url)
