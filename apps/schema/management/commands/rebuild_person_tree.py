"""A management command to rebuild a person tree."""

from django.core.management.base import BaseCommand

from apps.schema.models.person import Person
from apps.tree.models import Tree


class Command(BaseCommand):
  """Rebuild person tree."""

  help = 'Rebuilds person tree.'

  def add_arguments(self, parser):
    parser.add_argument('tree_uid', type=str)

  def handle(self, *args, **options):
    tree_uid = options['tree_uid']

    try:
      tree = Tree.nodes.get(uid=tree_uid)
    except Tree.DoesNotExist:
      self.stdout.write(
          self.style.ERROR(f'Tree with UID {tree_uid} does not exist.'))
      exit(1)

    persons = Person.nodes.filter(tree_uid=tree.uid).order_by(
        'last_name', 'first_name')
    person_count = len(persons)
    for idx, person in enumerate(persons):
      self.stdout.write(f'{person.short_name} [{idx + 1}/{person_count}]')
      person.save()

    self.stdout.write(self.style.SUCCESS('Done.'))
