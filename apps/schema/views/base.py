"""Schema views base."""

from django.http import Http404
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from neomodel import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.schema.models.person import Person
from apps.tree.views import TreeMixin


class TreeNodeMixin(TreeMixin):
  """Tree node mixin."""

  tree_uid_field = 'tree_uid'

  def get_object(self):
    """Get object."""

    try:
      return self.model.nodes.get(tree_uid=self.tree.uid, uid=self.kwargs['pk'])
    except self.model.DoesNotExist:
      raise Http404


class TreeNodesMixin(TreeMixin):
  """Tree nodes mixin."""

  tree_uid_field = 'tree_uid'

  def get_queryset(self):
    """Get queryset."""

    return self.model.nodes.filter(tree_uid=self.tree.uid)


class CreateViewBase(TreeMixin, CreateView):
  """Create view base."""

  def form_valid(self, form):
    """Validate form."""

    form.instance.tree_uid = self.tree.uid
    return super().form_valid(form)

  def get_form_kwargs(self):
    """Get form kwargs."""

    kwargs = super().get_form_kwargs()
    kwargs['tree'] = self.tree
    return kwargs


class DeleteViewBase(TreeNodeMixin, DeleteView):
  """Delete view base."""


class ListViewBase(TreeNodesMixin, ListView):
  """List view base."""


class ListViewAPIBase(ListViewBase, APIView):
  """List view API base."""

  paginate_by = 10

  def get(self, request, format=None):
    """Return filtered and sorted objects."""

    start = 0
    length = self.paginate_by

    try:
      length = int(request.query_params.get('length'), length)
    except ValueError:
      pass

    try:
      start = int(request.query_params.get('start'), start)
    except ValueError:
      pass

    queryset = self.filter(self.get_queryset())
    data = self.sort(self.serializer_class(
        queryset, many=True).data)[start:start + length]

    return Response({
        'draw': request.query_params.get('draw'),
        'recordsTotal': len(self.get_queryset()),
        'recordsFiltered': len(self.get_queryset()),
        'data': data,
    })

  def filter(self, nodes):
    """Filter the queryset. Can only filter by model fields."""

    search_query = self.request.query_params.get('search[value]')
    if not search_query:
      return nodes

    search_words = [w.strip() for w in search_query.split()]

    # TODO(ark): a workaround for neo4j unexpected non-return of a result for
    # MATCH...WHERE person.first_name =~ '(?i).*абв.*'... queries (note that
    # MATCH...WHERE person.first_name =~ '(?i).*abc.*'... queries work fine).
    search_words = [sw.capitalize() for sw in search_words]

    # Build word filters.
    search_word_filters = []
    search_operator = 'contains'

    # Generate filter for each combination of search_word:search_field.
    for search_word in search_words:
      search_word_filter = None
      kwargs = {
          f'{search_field}__{search_operator}': search_word
          for search_field in self.search_fields
      }
      kwargs['_connector'] = Q.OR

      if search_word_filter is None:
        search_word_filter = Q(**kwargs)
      else:
        search_word_filter.add(Q(**kwargs), Q.OR)

      search_word_filters.append(search_word_filter)

    # Combine filters using AND.
    query_filter = None
    for search_word_filter in search_word_filters:
      if query_filter is None:
        query_filter = search_word_filter
      else:
        query_filter.add(search_word_filter, Q.AND)

    return nodes.filter(query_filter)

  def sort(self, object_list):
    """Sort the queryset. Can only sort by serializer fields."""

    order_by = self.request.query_params.get('order[0][column]')
    order_by_direction = self.request.query_params.get('order[0][dir]')

    try:
      order_by = self.order_by_fields[int(order_by)]
    except (IndexError, ValueError):
      order_by = None

    if not order_by:
      return object_list

    if order_by_direction == 'desc':
      key = lambda o: (o.get(order_by) is not None, o.get(order_by))
      reverse = True
    else:
      key = lambda o: (o.get(order_by) is None, o.get(order_by))
      reverse = False

    return sorted(object_list, key=key, reverse=reverse)


class UpdateViewBase(TreeNodeMixin, UpdateView):
  """Update view base."""

  def get_form_kwargs(self):
    """Get form kwargs."""

    kwargs = super().get_form_kwargs()
    kwargs['tree'] = self.tree
    return kwargs
