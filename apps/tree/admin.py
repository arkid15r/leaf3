"""Tree admin."""

from django.contrib import admin

from django_neomodel import admin as neo_admin

from apps.tree.models import Tree


class TreeAdmin(admin.ModelAdmin):
  """Tree model admin."""

  list_display = ('name',)
  search_fields = ('name',)


neo_admin.register(Tree, TreeAdmin)
