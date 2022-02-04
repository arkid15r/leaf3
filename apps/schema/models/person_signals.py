"""Person signals/handlers."""

from apps.schema.models.location import Location
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
  if instance.spouse_uid:
    spouse = Person.nodes.get(uid=instance.spouse_uid)
    if spouse.spouse_uid != instance.uid:
      spouse.spouse_uid = instance.uid
      spouse.save()

      instance.spouse_rel.connect(spouse)

  # Birthplace.
  instance.birthplace_rel.disconnect_all()
  if instance.birthplace_uid:
    instance.birthplace_rel.connect(
        Location.nodes.get(uid=instance.birthplace_uid))

  # Residence.
  instance.residence_rel.disconnect_all()
  if instance.residence_uid:
    instance.residence_rel.connect(
        Location.nodes.get(uid=instance.residence_uid))
