from django.db import models
from django.utils.translation import gettext_lazy as _


class Exercise(models.Model):
    class Place(models.TextChoices):
        HOME = "HOME", _("Home")
        GYM = "GYM", _("Gym")
        BOTH = "BOTH", _("Home and gym")

    class Goal(models.TextChoices):
        LOSE_FAT = "LOSE_FAT", _("Lose fat")
        GAIN_MUSCLE = "GAIN_MUSCLE", _("Build muscle")
        STRENGTH = "STRENGTH", _("Strength")
        ENDURANCE = "ENDURANCE", _("Endurance")
        MOBILITY = "MOBILITY", _("Mobility")

    class Level(models.TextChoices):
        BEGINNER = "BEGINNER", _("Beginner")
        INTERMEDIATE = "INTERMEDIATE", _("Intermediate")
        ADVANCED = "ADVANCED", _("Advanced")

    class Impact(models.TextChoices):
        LOW = "LOW", _("Low impact")
        MODERATE = "MODERATE", _("Moderate impact")
        HIGH = "HIGH", _("High impact")

    class ContentLanguage(models.TextChoices):
        SPANISH = "es", _("Spanish")
        ENGLISH = "en", _("English")

    name = models.CharField(max_length=120, unique=True)
    description = models.TextField()
    place = models.CharField(
        max_length=8,
        choices=Place.choices,
        default=Place.BOTH,
    )
    goal = models.CharField(max_length=20, choices=Goal.choices)
    level = models.CharField(
        max_length=20,
        choices=Level.choices,
        default=Level.BEGINNER,
    )
    focus_area = models.CharField(max_length=80, default="Full body")
    duration_minutes = models.PositiveSmallIntegerField(default=20)
    impact = models.CharField(
        max_length=8,
        choices=Impact.choices,
        default=Impact.MODERATE,
    )
    content_language = models.CharField(
        max_length=2,
        choices=ContentLanguage.choices,
        default=ContentLanguage.SPANISH,
    )
    requires_equipment = models.BooleanField(default=False)
    equipment_notes = models.CharField(max_length=140, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["duration_minutes", "name"]

    def __str__(self):
        return self.name
