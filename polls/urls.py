from django.urls import path

from . import views

app_name = "polls"

urlpatterns = [
    path("", views.index, name="index"),
    path("imc/", views.bmi_calculator, name="bmi_calculator"),
    path(
        "ejercicios/<int:exercise_id>/", views.exercise_detail, name="exercise_detail"
    ),
    path("api/imc/", views.bmi_api, name="bmi_api"),
    path("api/recommendations/", views.recommendations_api, name="recommendations_api"),
]
