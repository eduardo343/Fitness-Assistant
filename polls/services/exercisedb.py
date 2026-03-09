import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from polls.models import Exercise

BASE_URL = "https://exercisedb-api.vercel.app/api/v1/exercises"

HOME_EQUIPMENT_KEYWORDS = {
    "body weight",
    "resistance band",
    "medicine ball",
    "stability ball",
    "bosu ball",
}

GYM_EQUIPMENT_KEYWORDS = {
    "barbell",
    "dumbbell",
    "kettlebell",
    "cable",
    "machine",
    "smith machine",
    "ez barbell",
    "leverage machine",
}


def fetch_exercisedb_exercises(limit=25, offset=0, timeout=20):
    params = urlencode(
        {
            "limit": limit,
            "offset": offset,
            "sortBy": "name",
            "sortOrder": "asc",
        }
    )
    request = Request(f"{BASE_URL}?{params}", headers={"Accept": "application/json"})
    with urlopen(request, timeout=timeout) as response:  # noqa: S310
        payload = json.loads(response.read().decode("utf-8"))
    return payload.get("data", [])


def map_exercisedb_exercise(raw_exercise):
    name = raw_exercise.get("name", "").strip()
    if not name:
        return None

    equipments = [equipment.lower().strip() for equipment in raw_exercise.get("equipments", [])]
    body_parts = [part.lower().strip() for part in raw_exercise.get("bodyParts", [])]
    target_muscles = [muscle.strip() for muscle in raw_exercise.get("targetMuscles", [])]
    instructions = [instruction.strip() for instruction in raw_exercise.get("instructions", [])]

    level = _infer_level(instructions)
    return {
        "name": name[:120],
        "description": _build_description(raw_exercise, instructions),
        "place": _infer_place(equipments),
        "goal": _infer_goal(body_parts, target_muscles),
        "level": level,
        "focus_area": _build_focus_area(target_muscles, body_parts),
        "duration_minutes": _infer_duration(level),
        "requires_equipment": _requires_equipment(equipments),
        "equipment_notes": ", ".join(raw_exercise.get("equipments", [])[:3]),
        "active": True,
    }


def _build_description(raw_exercise, instructions):
    if instructions:
        return " ".join(instructions[:2])[:1000]

    fallback = raw_exercise.get("gifUrl", "")
    if fallback:
        return f"Ejercicio importado de ExerciseDB. Referencia visual: {fallback}"[:1000]
    return "Ejercicio importado de ExerciseDB."


def _infer_place(equipments):
    if not equipments:
        return Exercise.Place.BOTH

    equipment_set = set(equipments)
    has_home = any(keyword in equipment_set for keyword in HOME_EQUIPMENT_KEYWORDS)
    has_gym = any(keyword in equipment_set for keyword in GYM_EQUIPMENT_KEYWORDS)

    if has_home and not has_gym:
        return Exercise.Place.HOME
    if has_gym and not has_home:
        return Exercise.Place.GYM
    return Exercise.Place.BOTH


def _infer_goal(body_parts, target_muscles):
    body_parts_set = set(body_parts)
    target_set = {muscle.lower() for muscle in target_muscles}

    if "cardio" in body_parts_set:
        return Exercise.Goal.ENDURANCE
    if "waist" in body_parts_set:
        return Exercise.Goal.LOSE_FAT
    if {"upper back", "lats", "pectorals", "glutes", "hamstrings", "quads"} & target_set:
        return Exercise.Goal.GAIN_MUSCLE
    if {"delts", "traps", "core"} & target_set:
        return Exercise.Goal.STRENGTH
    return Exercise.Goal.STRENGTH


def _infer_level(instructions):
    count = len(instructions)
    if count <= 4:
        return Exercise.Level.BEGINNER
    if count <= 7:
        return Exercise.Level.INTERMEDIATE
    return Exercise.Level.ADVANCED


def _infer_duration(level):
    if level == Exercise.Level.BEGINNER:
        return 15
    if level == Exercise.Level.INTERMEDIATE:
        return 22
    return 30


def _build_focus_area(target_muscles, body_parts):
    if target_muscles:
        return ", ".join(target_muscles[:2])[:80]
    if body_parts:
        return ", ".join(body_parts[:2])[:80]
    return "Cuerpo completo"


def _requires_equipment(equipments):
    if not equipments:
        return False
    return set(equipments) != {"body weight"}
