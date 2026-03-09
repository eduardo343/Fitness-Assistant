from django.contrib import admin

from .models import Exercise


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "place",
        "goal",
        "level",
        "duration_minutes",
        "requires_equipment",
        "active",
    )
    list_filter = ("place", "goal", "level", "requires_equipment", "active")
    search_fields = ("name", "focus_area", "description")
