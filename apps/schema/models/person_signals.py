"""Person signals/handlers."""

from apps.schema.models.entry import Entry
from apps.schema.models.person import Person


def post_save(sender, instance, created, **kwargs):
  """Person post save handler."""

  person = instance

  # Parents.
  parent_uids = []
  if person.father_uid:
    parent_uids.append(person.father_uid)
  if person.mother_uid:
    parent_uids.append(person.mother_uid)

  person.parent_rel.disconnect_all()
  for parent in Person.nodes.filter(uid__in=parent_uids):
    person.parent_rel.connect(parent)

  # Spouse.
  person.spouse_rel.disconnect_all()
  if person.spouse:
    if person.spouse.spouse_uid != person.uid:
      person.spouse.spouse_uid = person.uid
      person.spouse.save()

      person.spouse_rel.connect(person.spouse)

  # Residence.
  person.residence_rel.disconnect_all()
  if person.residence:
    person.residence_rel.connect(person.residence)

  # Auto created entries.
  # Birth.
  if person.birth_year or person.birth_place:
    entry = Entry.auto_create(instance, Entry.AUTO_EVENT_BORN)
    entry.location_uid = person.birth_place_uid
    entry.occurred = person.birth_date
    entry.occurred_year = person.birth_year
    entry.save()

    person.birth_place_rel.disconnect_all()
    if person.birth_place:
      person.birth_place_rel.connect(person.birth_place)

  # Death.
  if person.has_death_year:
    entry = Entry.auto_create(person, Entry.AUTO_EVENT_DIED)
    entry.location_uid = person.death_place_uid
    entry.occurred = person.death_date
    entry.occurred_year = person.death_year
    entry.save()

    person.death_place_rel.disconnect_all()
    if person.death_place:
      person.death_place_rel.connect(person.death_place)

    # Burial.
    if person.burial_date or person.burial_place_uid:
      entry = Entry.auto_create(person, Entry.AUTO_EVENT_BURIED)
      entry.location_uid = person.burial_place_uid
      entry.occurred = person.burial_date
      entry.save()

      person.burial_place_rel.disconnect_all()
      if person.burial_place:
        person.burial_place_rel.connect(person.burial_place)

  # Aunts/uncles.
  for aou in person.aunts_and_uncles:
    if aou.was_alive_in(person.birth_year):
      Entry.add_relative_birth(aou, Entry.AUTO_EVENT_HAD_NEPHEW_OR_NIECE,
                               person)

    if aou.was_alive_in(person.death_year):
      Entry.add_relative_death(aou, Entry.AUTO_EVENT_LOST_NEPHEW_OR_NIECE,
                               person)

  # Children.
  for child in person.children:
    if child.was_alive_in(person.death_year):
      Entry.add_relative_death(child, Entry.AUTO_EVENT_LOST_PARENT, person)

  # Cousins.
  for cousin in person.cousins:
    if cousin.was_alive_in(person.birth_year):
      Entry.add_relative_birth(cousin, Entry.AUTO_EVENT_HAD_COUSIN, person)

    if cousin.was_alive_in(person.death_year):
      Entry.add_relative_death(cousin, Entry.AUTO_EVENT_LOST_COUSIN, person)

  # Grandchildren.
  for grandchild in person.grandchildren:
    if grandchild.was_alive_in(person.death_year):
      Entry.add_relative_death(grandchild, Entry.AUTO_EVENT_LOST_GRANDPARENT,
                               person)

  # Grandparents.
  for grandparent in person.grandparents:
    if grandparent.was_alive_in(person.birth_year):
      Entry.add_relative_birth(grandparent, Entry.AUTO_EVENT_HAD_GRANDCHILD,
                               person)

    if grandparent.was_alive_in(person.death_year):
      Entry.add_relative_death(grandparent, Entry.AUTO_EVENT_LOST_GRANDCHILD,
                               person)

  # Great grandchildren.
  for g_grandchild in person.great_grandchildren:
    if g_grandchild.was_alive_in(person.death_year):
      Entry.add_relative_death(g_grandchild,
                               Entry.AUTO_EVENT_LOST_GREAT_GRANDPARENT, person)

  # Great-great grandchildren.
  for gg_grandchild in person.great_great_grandchildren:
    if gg_grandchild.was_alive_in(person.death_year):
      Entry.add_relative_death(gg_grandchild,
                               Entry.AUTO_EVENT_LOST_GREAT_GREAT_GRANDPARENT,
                               person)

  # Great grandparents.
  for g_grandparent in person.great_grandparents:
    if g_grandparent.was_alive_in(person.birth_year):
      Entry.add_relative_birth(g_grandparent,
                               Entry.AUTO_EVENT_HAD_GREAT_GRANDCHILD, person)

    if g_grandparent.was_alive_in(person.death_year):
      Entry.add_relative_death(g_grandparent,
                               Entry.AUTO_EVENT_LOST_GREAT_GRANDCHILD, person)

  # Great-great grandparents.
  for gg_grandparent in person.great_great_grandparents:
    if gg_grandparent.was_alive_in(person.birth_year):
      Entry.add_relative_birth(gg_grandparent,
                               Entry.AUTO_EVENT_HAD_GREAT_GREAT_GRANDCHILD,
                               person)

    if gg_grandparent.was_alive_in(person.death_year):
      Entry.add_relative_death(gg_grandparent,
                               Entry.AUTO_EVENT_LOST_GREAT_GREAT_GRANDCHILD,
                               person)

  # Nephews/nieces.
  for non in person.nephews_and_nieces:
    if non.was_alive_in(person.birth_year):
      Entry.add_relative_birth(non, Entry.AUTO_EVENT_HAD_AUNT_OR_UNCLE, person)

    if non.was_alive_in(person.death_year):
      Entry.add_relative_death(non, Entry.AUTO_EVENT_LOST_AUNT_OR_UNCLE, person)

  # Parents.
  for parent in person.parents:
    if parent.was_alive_in(person.birth_year):
      Entry.add_relative_birth(parent, Entry.AUTO_EVENT_HAD_CHILD, person)

    if parent.was_alive_in(person.death_year):
      Entry.add_relative_death(parent, Entry.AUTO_EVENT_LOST_CHILD, person)

  # Siblings.
  for sibling in person.siblings:
    if sibling.was_alive_in(person.birth_year):
      Entry.add_relative_birth(sibling, Entry.AUTO_EVENT_HAD_SIBLING, person)

    if sibling.was_alive_in(person.death_year):
      Entry.add_relative_death(sibling, Entry.AUTO_EVENT_LOST_SIBLING, person)
