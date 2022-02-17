"""A management command to repopulate persons' timelines."""

from django.core.management.base import BaseCommand

from apps.schema.models.person import Person
from apps.tree.models import Tree


class Command(BaseCommand):
  """Repopulate persons' timelines."""

  help = ("Repopulates persons' timelines. Use --tree_uid=all to repopulate "
          "timelines in all trees.")

  def add_arguments(self, parser):
    parser.add_argument('--tree_uid', type=str)

  def handle(self, *args, **options):
    tree_uid = options['tree_uid']

    if not tree_uid:
      self.stdout.write(
          self.style.ERROR('Please specify the tree UID using --tree_uid. '
                           'Use --help for help.'))
      exit(1)

    if tree_uid == 'all':
      trees = Tree.nodes.all()
    else:
      try:
        trees = (Tree.nodes.get(uid=tree_uid),)
      except Tree.DoesNotExist:
        self.stdout.write(
            self.style.ERROR(f'Tree with UID {tree_uid} does not exist.'))
        exit(1)

    tree_count = len(trees)
    for idx, tree in enumerate(trees):
      self.stdout.write(f'{tree.name} [{idx + 1}/{tree_count}]')
      self.populate_timeline(tree.uid)

    self.stdout.write(self.style.SUCCESS('Done.'))

  def populate_timeline(self, tree_uid):
    """Populate persons' timelines with auto created entries."""

    persons = Person.nodes.filter(tree_uid=tree_uid).order_by(
        'last_name', 'first_name')
    person_count = len(persons)

    for idx, person in enumerate(persons):
      self.stdout.write(f'{person.short_name} [{idx + 1}/{person_count}]')
      person.save()
