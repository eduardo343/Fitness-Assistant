from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.views.i18n import set_language

urlpatterns = [
    path("i18n/setlang/", set_language, name="set_language"),
    path("", RedirectView.as_view(pattern_name="polls:index", permanent=False)),
    path("polls/", include("polls.urls")),
    path("admin/", admin.site.urls),
]
