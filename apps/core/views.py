from django.shortcuts import redirect
from django.views.generic.base import TemplateView


class Main(TemplateView):
  """Main view."""

  template_name = "core/main.html"

  def get(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      return redirect('tree-dashboard')

    context = self.get_context_data(**kwargs)
    return self.render_to_response(context)
