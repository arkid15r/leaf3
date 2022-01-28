"""Neomodel custom relationships."""

from neomodel.properties import DateProperty
from neomodel.relationship import StructuredRel


class TimeRangeRelationship(StructuredRel):
  """Time range relationship."""

  since = DateProperty(required=True)
  until = DateProperty()
