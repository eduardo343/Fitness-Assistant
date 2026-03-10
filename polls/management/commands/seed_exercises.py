from django.core.management.base import BaseCommand

from polls.models import Exercise

EXERCISES = [
    {
        "name": "Sentadillas libres",
        "description": (
            "Movimiento base para piernas y gluteos. Mantiene la espalda neutra."
        ),
        "place": Exercise.Place.BOTH,
        "goal": Exercise.Goal.STRENGTH,
        "level": Exercise.Level.BEGINNER,
        "focus_area": "Piernas y gluteos",
        "duration_minutes": 20,
        "impact": Exercise.Impact.MODERATE,
        "content_language": Exercise.ContentLanguage.SPANISH,
        "requires_equipment": False,
        "equipment_notes": "",
    },
    {
        "name": "Flexiones de pecho",
        "description": "Trabaja pecho, hombros y triceps usando peso corporal.",
        "place": Exercise.Place.HOME,
        "goal": Exercise.Goal.GAIN_MUSCLE,
        "level": Exercise.Level.BEGINNER,
        "focus_area": "Pecho y triceps",
        "duration_minutes": 15,
        "impact": Exercise.Impact.MODERATE,
        "content_language": Exercise.ContentLanguage.SPANISH,
        "requires_equipment": False,
        "equipment_notes": "",
    },
    {
        "name": "Plancha frontal",
        "description": "Ejercicio isometrico para activar core y mejorar estabilidad.",
        "place": Exercise.Place.BOTH,
        "goal": Exercise.Goal.STRENGTH,
        "level": Exercise.Level.BEGINNER,
        "focus_area": "Core",
        "duration_minutes": 10,
        "impact": Exercise.Impact.LOW,
        "content_language": Exercise.ContentLanguage.SPANISH,
        "requires_equipment": False,
        "equipment_notes": "",
    },
    {
        "name": "Burpees",
        "description": "Ejercicio metabolico para elevar pulsaciones y quemar grasa.",
        "place": Exercise.Place.HOME,
        "goal": Exercise.Goal.LOSE_FAT,
        "level": Exercise.Level.INTERMEDIATE,
        "focus_area": "Cuerpo completo",
        "duration_minutes": 18,
        "impact": Exercise.Impact.HIGH,
        "content_language": Exercise.ContentLanguage.SPANISH,
        "requires_equipment": False,
        "equipment_notes": "",
    },
    {
        "name": "Remo con mancuernas",
        "description": "Fortalece espalda alta y dorsales con control postural.",
        "place": Exercise.Place.GYM,
        "goal": Exercise.Goal.GAIN_MUSCLE,
        "level": Exercise.Level.INTERMEDIATE,
        "focus_area": "Espalda",
        "duration_minutes": 25,
        "impact": Exercise.Impact.MODERATE,
        "content_language": Exercise.ContentLanguage.SPANISH,
        "requires_equipment": True,
        "equipment_notes": "Mancuernas",
    },
    {
        "name": "Peso muerto rumano",
        "description": "Enfocado en femorales, gluteos y cadena posterior.",
        "place": Exercise.Place.GYM,
        "goal": Exercise.Goal.STRENGTH,
        "level": Exercise.Level.INTERMEDIATE,
        "focus_area": "Pierna posterior",
        "duration_minutes": 30,
        "impact": Exercise.Impact.MODERATE,
        "content_language": Exercise.ContentLanguage.SPANISH,
        "requires_equipment": True,
        "equipment_notes": "Barra o mancuernas",
    },
    {
        "name": "Zancadas alternadas",
        "description": "Trabajo unilateral de piernas para estabilidad y potencia.",
        "place": Exercise.Place.BOTH,
        "goal": Exercise.Goal.GAIN_MUSCLE,
        "level": Exercise.Level.BEGINNER,
        "focus_area": "Piernas",
        "duration_minutes": 16,
        "impact": Exercise.Impact.MODERATE,
        "content_language": Exercise.ContentLanguage.SPANISH,
        "requires_equipment": False,
        "equipment_notes": "",
    },
    {
        "name": "Bicicleta estatica HIIT",
        "description": (
            "Intervalos cortos de alta intensidad para resistencia y perdida de grasa."
        ),
        "place": Exercise.Place.GYM,
        "goal": Exercise.Goal.ENDURANCE,
        "level": Exercise.Level.INTERMEDIATE,
        "focus_area": "Cardio",
        "duration_minutes": 22,
        "impact": Exercise.Impact.HIGH,
        "content_language": Exercise.ContentLanguage.SPANISH,
        "requires_equipment": True,
        "equipment_notes": "Bicicleta estatica",
    },
    {
        "name": "Movilidad de cadera y tobillo",
        "description": "Secuencia controlada para mejorar rango articular y tecnica.",
        "place": Exercise.Place.BOTH,
        "goal": Exercise.Goal.MOBILITY,
        "level": Exercise.Level.BEGINNER,
        "focus_area": "Movilidad",
        "duration_minutes": 12,
        "impact": Exercise.Impact.LOW,
        "content_language": Exercise.ContentLanguage.SPANISH,
        "requires_equipment": False,
        "equipment_notes": "",
    },
    {
        "name": "Dominadas asistidas",
        "description": "Fortalece espalda y brazos con apoyo de banda o maquina.",
        "place": Exercise.Place.GYM,
        "goal": Exercise.Goal.GAIN_MUSCLE,
        "level": Exercise.Level.ADVANCED,
        "focus_area": "Espalda y biceps",
        "duration_minutes": 20,
        "impact": Exercise.Impact.HIGH,
        "content_language": Exercise.ContentLanguage.SPANISH,
        "requires_equipment": True,
        "equipment_notes": "Banda elastica o maquina asistida",
    },
    {
        "name": "Marcha en sitio",
        "description": (
            "Cardio suave para activar el cuerpo con bajo impacto articular."
        ),
        "place": Exercise.Place.HOME,
        "goal": Exercise.Goal.LOSE_FAT,
        "level": Exercise.Level.BEGINNER,
        "focus_area": "Cardio ligero",
        "duration_minutes": 12,
        "impact": Exercise.Impact.LOW,
        "content_language": Exercise.ContentLanguage.SPANISH,
        "requires_equipment": False,
        "equipment_notes": "",
    },
    {
        "name": "Puente de gluteos",
        "description": "Fortalece gluteos y core sin castigar articulaciones.",
        "place": Exercise.Place.BOTH,
        "goal": Exercise.Goal.STRENGTH,
        "level": Exercise.Level.BEGINNER,
        "focus_area": "Gluteos y core",
        "duration_minutes": 14,
        "impact": Exercise.Impact.LOW,
        "content_language": Exercise.ContentLanguage.SPANISH,
        "requires_equipment": False,
        "equipment_notes": "",
    },
    {
        "name": "Remo sentado en polea",
        "description": "Trabajo de espalda controlado para ganar fuerza con tecnica.",
        "place": Exercise.Place.GYM,
        "goal": Exercise.Goal.GAIN_MUSCLE,
        "level": Exercise.Level.BEGINNER,
        "focus_area": "Espalda media",
        "duration_minutes": 18,
        "impact": Exercise.Impact.LOW,
        "content_language": Exercise.ContentLanguage.SPANISH,
        "requires_equipment": True,
        "equipment_notes": "Polea baja",
    },
    {
        "name": "Eliptica continua",
        "description": (
            "Cardio sostenido de bajo impacto para resistencia y gasto calorico."
        ),
        "place": Exercise.Place.GYM,
        "goal": Exercise.Goal.ENDURANCE,
        "level": Exercise.Level.BEGINNER,
        "focus_area": "Cardio",
        "duration_minutes": 20,
        "impact": Exercise.Impact.LOW,
        "content_language": Exercise.ContentLanguage.SPANISH,
        "requires_equipment": True,
        "equipment_notes": "Eliptica",
    },
    {
        "name": "Step-ups controlados",
        "description": "Mejora condicion y fuerza de piernas con control del ritmo.",
        "place": Exercise.Place.HOME,
        "goal": Exercise.Goal.LOSE_FAT,
        "level": Exercise.Level.BEGINNER,
        "focus_area": "Piernas y cardio",
        "duration_minutes": 16,
        "impact": Exercise.Impact.MODERATE,
        "content_language": Exercise.ContentLanguage.SPANISH,
        "requires_equipment": False,
        "equipment_notes": "Escalon estable opcional",
    },
    {
        "name": "Dead bug",
        "description": "Ejercicio de core para estabilidad lumbar y coordinacion.",
        "place": Exercise.Place.HOME,
        "goal": Exercise.Goal.STRENGTH,
        "level": Exercise.Level.BEGINNER,
        "focus_area": "Core",
        "duration_minutes": 10,
        "impact": Exercise.Impact.LOW,
        "content_language": Exercise.ContentLanguage.SPANISH,
        "requires_equipment": False,
        "equipment_notes": "",
    },
]


class Command(BaseCommand):
    help = "Carga una base inicial de ejercicios recomendados para casa y gym."

    def handle(self, *args, **options):
        created = 0
        updated = 0

        for exercise_data in EXERCISES:
            _, was_created = Exercise.objects.update_or_create(
                name=exercise_data["name"],
                defaults=exercise_data,
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed completado. Creados: {created}. Actualizados: {updated}."
            )
        )
