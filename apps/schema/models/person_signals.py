"""Person signals/handlers."""

from apps.schema.models.location import Location
from apps.schema.models.person import Person


def post_save(sender, instance, created, **kwargs):
  """Person post save handler."""

  parent_uids = []
  if instance.father_uid:
    parent_uids.append(instance.father_uid)
  if instance.mother_uid:
    parent_uids.append(instance.mother_uid)

  # Parents.
  instance.parents_rel.disconnect_all()
  for parent in Person.nodes.filter(uid__in=parent_uids):
    instance.parents_rel.connect(parent)

  # Spouse.
  if instance.spouse_uid:
    spouse = Person.nodes.get(uid=instance.spouse_uid)
    if spouse.spouse_uid != instance.uid:
      spouse.spouse_uid = instance.uid
      spouse.save()

      instance.spouse_rel.disconnect_all()
      instance.spouse_rel.connect(spouse)

  # Birthplace.
  if instance.birthplace_uid:
    instance.birthplace_rel.disconnect_all()
    instance.birthplace_rel.connect(
        Location.nodes.get(uid=instance.birthplace_uid))

  # Residence.
  if instance.residence_uid:
    instance.birthplace_rel.disconnect_all()
    instance.birthplace_rel.connect(
        Location.nodes.get(uid=instance.residence_uid))
