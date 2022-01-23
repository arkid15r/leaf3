"""User app admin."""

from django.contrib import admin

from apps.user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
  """User model admin."""

  list_display = ('email', 'username')
  search_fields = ('email', 'username')
