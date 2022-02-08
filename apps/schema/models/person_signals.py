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
  entry = Entry.auto_create(instance, Entry.AUTO_EVENT_BORN)
  entry.location_uid = person.birth_place_uid
  entry.occurred = person.birth_date
  entry.occurred_year = person.birth_year
  entry.save()

  person.birth_place_rel.disconnect_all()
  if person.birth_place:
    person.birth_place_rel.connect(person.birth_place)

  # Death.
  if person.death_year:
    entry = Entry.auto_create(person, Entry.AUTO_EVENT_DIED)
    entry.location_uid = person.death_place_uid
    entry.occurred = person.death_date
    entry.occurred_year = person.death_year
    entry.save()

    person.death_place_rel.disconnect_all()
    if person.death_place:
      person.death_place_rel.connect(person.death_place)

    # Burial.
    entry = Entry.auto_create(person, Entry.AUTO_EVENT_BURIED)
    entry.location_uid = person.burial_place_uid
    entry.occurred = person.burial_date
    entry.save()

    person.burial_place_rel.disconnect_all()
    if person.burial_place:
      person.burial_place_rel.connect(person.burial_place)

  # Parents and their siblings.
  for parent in person.parents:
    # Daughter/son.
    Entry.add_relative(parent, Entry.AUTO_EVENT_HAD_CHILD, person)

    # Nephew/niece.
    for parent_sibling in parent.siblings:
      Entry.add_relative(parent_sibling, Entry.AUTO_EVENT_HAD_NEPHEW_OR_NIECE,
                         person)

  # Siblings.
  for sibling in person.siblings:
    Entry.add_relative(sibling, Entry.AUTO_EVENT_HAD_SIBLING, person)

  # Cousins.
  for cousin in person.cousins:
    Entry.add_relative(cousin, Entry.AUTO_EVENT_HAD_COUSIN, person)

  # Grandparents.
  for grandparent in person.grandparents:
    if not grandparent.was_alive_in(person.birth_year):
      continue
    Entry.add_relative(grandparent, Entry.AUTO_EVENT_HAD_GRANDCHILD, person)

  # Great grandparents.
  for great_grandparent in person.great_grandparents:
    if not great_grandparent.was_alive_in(person.birth_year):
      continue

    Entry.add_relative(great_grandparent, Entry.AUTO_EVENT_HAD_GREAT_GRANDCHILD,
                       person)
