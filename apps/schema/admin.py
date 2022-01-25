"""Schema admin."""

from django.contrib import admin

from django_neomodel import admin as neo_admin

from apps.schema.models.person import Person


class PersonAdmin(admin.ModelAdmin):
  """Person admin."""

  list_display = ('first_name', 'last_name')


neo_admin.register(Person, PersonAdmin)
