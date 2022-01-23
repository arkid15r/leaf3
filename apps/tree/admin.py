"""Tree admin."""

from django.contrib import admin

from apps.tree.models import Tree


@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
  """Tree model admin."""

  list_display = ('name',)
  search_fields = ('name',)
