"""Schema entity views tests."""
# pylint: disable=missing-function-docstring

from django.urls import reverse

from tests.base import TestCaseBase


class TestEntityViews(TestCaseBase):
  """Test entity views."""

  def test_login_required(self):
    entity_uid = 'entity-uid'
    entity_uid_url_names = ('entity-update', 'entity-delete')
    tree_uid_url_names = ('entity-list', 'entity-create')
    tree_uid = 'tree-uid'

    for url_name in entity_uid_url_names + tree_uid_url_names:
      if url_name in entity_uid_url_names:
        url = reverse(url_name, args=(tree_uid, entity_uid))
      else:
        url = reverse(url_name, args=(tree_uid,))

      expected_redirect_url = f'{reverse("account_login")}?next={url}'
      response = self.client.get(url)
      self.assertRedirects(response, expected_redirect_url)
