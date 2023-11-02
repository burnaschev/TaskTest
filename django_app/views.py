from django.db import connection
from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView
from django_app.models import MenuItem


class MenuItemPageView(TemplateView):
    template_name = "django_app/index.html"

    def get_context_data(self, **kwargs) -> dict:

        context = super().get_context_data(**kwargs)
        context['menu'] = MenuItem.objects.filter(slug='main_menu').first()
        return context

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        response = super().get(request, *args, **kwargs)

        print("Number of database queries: ", len(connection.queries))

        return response
