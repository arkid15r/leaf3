"""Tree views tests."""
# pylint: disable=missing-function-docstring

from django.urls import reverse

from tests.base import TestCaseBase


class TestTreeViews(TestCaseBase):
  """Test tree views."""

  def test_login_required(self):
    tree_uid = 'tree_uid'
    tree_url_names = ('tree-dashboard', 'tree-create')
    tree_uid_url_names = ('tree-delete', 'tree-view', 'tree-update')

    for url_name in tree_url_names + tree_uid_url_names:
      if url_name in tree_uid_url_names:
        url = reverse(url_name, args=(tree_uid,))
      else:
        url = reverse(url_name)

      expected_redirect_url = f'{reverse("account_login")}?next={url}'
      response = self.client.get(url)
      self.assertRedirects(response, expected_redirect_url)
