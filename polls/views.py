from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.translation import get_language
from django.utils.translation import gettext as _

from .forms import BMIForm, RecommendationForm
from .models import Exercise

LEVEL_ORDER = {
    Exercise.Level.BEGINNER: 1,
    Exercise.Level.INTERMEDIATE: 2,
    Exercise.Level.ADVANCED: 3,
}


def _bmi_category(bmi):
    if bmi < 18.5:
        return "UNDERWEIGHT", _("Underweight")
    if bmi < 25:
        return "NORMAL", _("Healthy weight")
    if bmi < 30:
        return "OVERWEIGHT", _("Overweight")
    if bmi < 35:
        return "OBESITY_I", _("Obesity type I")
    if bmi < 40:
        return "OBESITY_II", _("Obesity type II")
    return "OBESITY_III", _("Obesity type III")


def _recommended_goal_for_bmi(category_code):
    mapping = {
        "UNDERWEIGHT": Exercise.Goal.GAIN_MUSCLE,
        "NORMAL": Exercise.Goal.STRENGTH,
        "OVERWEIGHT": Exercise.Goal.LOSE_FAT,
        "OBESITY_I": Exercise.Goal.LOSE_FAT,
        "OBESITY_II": Exercise.Goal.LOSE_FAT,
        "OBESITY_III": Exercise.Goal.LOSE_FAT,
    }
    return mapping[category_code]


def _calculate_bmi_result(weight_kg, height_cm):
    height_m = height_cm / 100
    bmi = weight_kg / (height_m * height_m)
    category_code, category_label = _bmi_category(bmi)
    healthy_min = 18.5 * (height_m * height_m)
    healthy_max = 24.9 * (height_m * height_m)
    recommended_goal = _recommended_goal_for_bmi(category_code)
    return {
        "bmi": round(bmi, 2),
        "category_code": category_code,
        "category": category_label,
        "healthy_weight_min": round(healthy_min, 1),
        "healthy_weight_max": round(healthy_max, 1),
        "recommended_goal": recommended_goal,
        "recommended_goal_label": dict(Exercise.Goal.choices)[recommended_goal],
    }


def _recommended_impacts_for_bmi(category_code):
    if category_code in {"OVERWEIGHT", "OBESITY_I", "OBESITY_II", "OBESITY_III"}:
        return [
            Exercise.Impact.LOW,
            Exercise.Impact.MODERATE,
            Exercise.Impact.HIGH,
        ]
    if category_code == "UNDERWEIGHT":
        return [
            Exercise.Impact.MODERATE,
            Exercise.Impact.LOW,
            Exercise.Impact.HIGH,
        ]
    return [
        Exercise.Impact.MODERATE,
        Exercise.Impact.LOW,
        Exercise.Impact.HIGH,
    ]


def _preferred_language_code():
    language = (get_language() or "en").lower()
    if language.startswith("es"):
        return Exercise.ContentLanguage.SPANISH
    return None


def _limit_for_preferred_language(queryset, limit):
    preferred_language = _preferred_language_code()
    if not preferred_language:
        return list(queryset[:limit])

    localized_results = list(
        queryset.filter(content_language=preferred_language)[:limit]
    )
    if localized_results:
        return localized_results
    return list(queryset[:limit])


def _get_recommendations(cleaned_data):
    queryset = Exercise.objects.filter(active=True)

    place = cleaned_data.get("place")
    if place == "home":
        queryset = queryset.filter(place__in=[Exercise.Place.HOME, Exercise.Place.BOTH])
    elif place == "gym":
        queryset = queryset.filter(place__in=[Exercise.Place.GYM, Exercise.Place.BOTH])

    goal = cleaned_data.get("goal")
    if goal:
        queryset = queryset.filter(goal=goal)

    max_duration = cleaned_data.get("max_duration")
    if max_duration:
        queryset = queryset.filter(duration_minutes__lte=max_duration)

    if cleaned_data.get("without_equipment"):
        queryset = queryset.filter(requires_equipment=False)

    selected_level = cleaned_data.get("level")
    if selected_level:
        selected_rank = LEVEL_ORDER[selected_level]
        allowed_levels = [
            level for level, rank in LEVEL_ORDER.items() if rank <= selected_rank
        ]
        queryset = queryset.filter(level__in=allowed_levels)

    return _limit_for_preferred_language(queryset, limit=12)


def _collect_exercises_by_impact(queryset, preferred_impacts, limit):
    ranked_exercises = []
    for impact in preferred_impacts:
        ranked_exercises.extend(
            list(
                queryset.filter(impact=impact).order_by(
                    "duration_minutes",
                    "name",
                )
            )
        )
    return ranked_exercises[:limit]


def _prioritize_exercises_by_impact(queryset, preferred_impacts, limit):
    preferred_language = _preferred_language_code()
    if preferred_language:
        localized_results = _collect_exercises_by_impact(
            queryset.filter(content_language=preferred_language),
            preferred_impacts,
            limit,
        )
        if localized_results:
            return localized_results

    return _collect_exercises_by_impact(queryset, preferred_impacts, limit)


def index(request):
    form = RecommendationForm(request.GET or None)
    recommendations = []

    if form.is_valid():
        recommendations = _get_recommendations(form.cleaned_data)
    else:
        form = RecommendationForm()

    context = {
        "form": form,
        "recommendations": recommendations,
        "has_filters": bool(request.GET),
    }
    return render(request, "polls/index.html", context)


def exercise_detail(request, exercise_id):
    exercise = get_object_or_404(Exercise, pk=exercise_id, active=True)
    return render(request, "polls/exercise_detail.html", {"exercise": exercise})


def recommendations_api(request):
    form = RecommendationForm(request.GET or None)
    if not form.is_valid():
        return JsonResponse({"errors": form.errors}, status=400)

    recommendations = _get_recommendations(form.cleaned_data)
    payload = [
        {
            "id": exercise.id,
            "name": exercise.name,
            "description": exercise.description,
            "place": exercise.get_place_display(),
            "goal": exercise.get_goal_display(),
            "level": exercise.get_level_display(),
            "impact": exercise.get_impact_display(),
            "focus_area": exercise.focus_area,
            "duration_minutes": exercise.duration_minutes,
            "requires_equipment": exercise.requires_equipment,
            "equipment_notes": exercise.equipment_notes,
        }
        for exercise in recommendations
    ]
    return JsonResponse({"count": len(payload), "results": payload})


def bmi_calculator(request):
    form = BMIForm(request.GET or None)
    result = None
    recommended_exercises = []

    if form.is_valid():
        result = _calculate_bmi_result(
            weight_kg=form.cleaned_data["weight_kg"],
            height_cm=form.cleaned_data["height_cm"],
        )

        exercise_queryset = Exercise.objects.filter(
            active=True,
            goal=result["recommended_goal"],
        )

        place = form.cleaned_data.get("place")
        if place == "home":
            exercise_queryset = exercise_queryset.filter(
                place__in=[Exercise.Place.HOME, Exercise.Place.BOTH]
            )
        elif place == "gym":
            exercise_queryset = exercise_queryset.filter(
                place__in=[Exercise.Place.GYM, Exercise.Place.BOTH]
            )

        # Priorizamos opciones seguras para iniciar por defecto.
        recommended_exercises = _prioritize_exercises_by_impact(
            exercise_queryset.filter(level=Exercise.Level.BEGINNER),
            _recommended_impacts_for_bmi(result["category_code"]),
            limit=6,
        )
        if not recommended_exercises:
            recommended_exercises = _prioritize_exercises_by_impact(
                exercise_queryset,
                _recommended_impacts_for_bmi(result["category_code"]),
                limit=6,
            )
    else:
        form = BMIForm()

    context = {
        "form": form,
        "result": result,
        "recommended_exercises": recommended_exercises,
        "has_filters": bool(request.GET),
    }
    return render(request, "polls/bmi_calculator.html", context)


def bmi_api(request):
    form = BMIForm(request.GET or None)
    if not form.is_valid():
        return JsonResponse({"errors": form.errors}, status=400)

    result = _calculate_bmi_result(
        weight_kg=form.cleaned_data["weight_kg"],
        height_cm=form.cleaned_data["height_cm"],
    )
    payload = {
        "bmi": result["bmi"],
        "category": result["category"],
        "category_code": result["category_code"],
        "healthy_weight_range_kg": {
            "min": result["healthy_weight_min"],
            "max": result["healthy_weight_max"],
        },
        "recommended_goal": {
            "code": result["recommended_goal"],
            "label": result["recommended_goal_label"],
        },
    }
    return JsonResponse(payload)
