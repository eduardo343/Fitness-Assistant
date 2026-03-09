from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Exercise


class RecommendationForm(forms.Form):
    PLACE_CHOICES = [
        ("", _("Any place")),
        ("home", _("Home")),
        ("gym", _("Gym")),
    ]

    place = forms.ChoiceField(choices=PLACE_CHOICES, required=False, label=_("Place"))
    goal = forms.ChoiceField(
        choices=[("", _("Any goal")), *Exercise.Goal.choices],
        required=False,
        label=_("Goal"),
    )
    level = forms.ChoiceField(
        choices=[("", _("Any level")), *Exercise.Level.choices],
        required=False,
        label=_("Level"),
    )
    max_duration = forms.IntegerField(
        required=False,
        min_value=5,
        max_value=180,
        label=_("Max duration (min)"),
    )
    without_equipment = forms.BooleanField(
        required=False,
        label=_("Bodyweight only"),
    )


class BMIForm(forms.Form):
    weight_kg = forms.FloatField(
        min_value=20,
        max_value=400,
        label=_("Weight (kg)"),
    )
    height_cm = forms.FloatField(
        min_value=80,
        max_value=250,
        label=_("Height (cm)"),
    )
    place = forms.ChoiceField(
        choices=RecommendationForm.PLACE_CHOICES,
        required=False,
        label=_("Training place"),
    )
