"""Person signals/handlers."""

from apps.schema.models.entry import Entry
from apps.schema.models.person import Person


def post_save(sender, instance, created, **kwargs):
  """Person post save handler."""

  # Parents.
  parent_uids = []
  if instance.father_uid:
    parent_uids.append(instance.father_uid)
  if instance.mother_uid:
    parent_uids.append(instance.mother_uid)

  instance.parent_rel.disconnect_all()
  for parent in Person.nodes.filter(uid__in=parent_uids):
    instance.parent_rel.connect(parent)

  # Spouse.
  instance.spouse_rel.disconnect_all()
  if instance.spouse:
    if instance.spouse.spouse_uid != instance.uid:
      instance.spouse.spouse_uid = instance.uid
      instance.spouse.save()

      instance.spouse_rel.connect(instance.spouse)

  # Birthplace.
  instance.birth_place_rel.disconnect_all()
  if instance.birth_place:
    instance.birth_place_rel.connect(instance.birth_place)

  # Residence.
  instance.residence_rel.disconnect_all()
  if instance.residence:
    instance.residence_rel.connect(instance.residence)

  # Auto created entries.
  # Birth.
  entry = Entry.auto_create(instance, Entry.AUTO_ENTRY_EVENT_BORN)
  entry.location_uid = instance.birth_place_uid
  entry.occurred = instance.dob
  entry.occurred_year = instance.birth_year
  entry.save()

  # Death.
  entry = Entry.auto_create(instance, Entry.AUTO_ENTRY_EVENT_DIED)
  entry.location_uid = instance.death_place_uid
  entry.occurred = instance.dod
  entry.occurred_year = instance.death_year
  entry.save()

  # Burial.
  entry = Entry.auto_create(instance, Entry.AUTO_ENTRY_EVENT_BURIED)
  entry.location_uid = instance.burial_place_uid
  entry.occurred = instance.dod
  entry.occurred_year = instance.death_year
  entry.save()
