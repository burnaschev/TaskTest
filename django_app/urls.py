from django.urls import path
from django_app.apps import DjangoAppConfig
from django_app.views import MenuItemPageView

app_name = DjangoAppConfig.name

urlpatterns = [
    path('menu/', MenuItemPageView.as_view(), name='index'),
]
