from django.test import TestCase
from django.urls import reverse

from .models import Exercise
from .services.exercisedb import map_exercisedb_exercise


class RecommendationViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Exercise.objects.create(
            name="Sentadilla casa",
            description="Trabajo de pierna sin equipo",
            place=Exercise.Place.HOME,
            goal=Exercise.Goal.STRENGTH,
            level=Exercise.Level.BEGINNER,
            focus_area="Pierna",
            duration_minutes=15,
            requires_equipment=False,
        )
        Exercise.objects.create(
            name="Press banca gym",
            description="Fuerza en pecho",
            place=Exercise.Place.GYM,
            goal=Exercise.Goal.GAIN_MUSCLE,
            level=Exercise.Level.INTERMEDIATE,
            focus_area="Pecho",
            duration_minutes=30,
            requires_equipment=True,
            equipment_notes="Banco y barra",
        )
        Exercise.objects.create(
            name="Plancha avanzada",
            description="Core avanzado",
            place=Exercise.Place.BOTH,
            goal=Exercise.Goal.STRENGTH,
            level=Exercise.Level.ADVANCED,
            focus_area="Core",
            duration_minutes=10,
            requires_equipment=False,
        )

    def test_index_loads(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Exercise recommender")

    def test_index_translates_to_spanish_with_accept_language(self):
        response = self.client.get(reverse("polls:index"), HTTP_ACCEPT_LANGUAGE="es")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Recomendador de ejercicios")

    def test_home_without_equipment_filters_out_gym_machine(self):
        response = self.client.get(
            reverse("polls:index"),
            {"place": "home", "without_equipment": "on"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sentadilla casa")
        self.assertContains(response, "Plancha avanzada")
        self.assertNotContains(response, "Press banca gym")

    def test_level_filter_allows_lower_levels(self):
        response = self.client.get(reverse("polls:index"), {"level": Exercise.Level.INTERMEDIATE})
        self.assertContains(response, "Sentadilla casa")
        self.assertContains(response, "Press banca gym")
        self.assertNotContains(response, "Plancha avanzada")

    def test_recommendations_api_returns_json_payload(self):
        response = self.client.get(
            reverse("polls:recommendations_api"),
            {"goal": Exercise.Goal.STRENGTH},
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["count"], 2)
        self.assertEqual(len(payload["results"]), 2)

    def test_bmi_calculator_view_shows_result_and_goal(self):
        response = self.client.get(
            reverse("polls:bmi_calculator"),
            {"weight_kg": 80, "height_cm": 170, "place": "home"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BMI:")
        self.assertContains(response, "Overweight")
        self.assertContains(response, "Lose fat")

    def test_bmi_api_returns_expected_payload(self):
        response = self.client.get(
            reverse("polls:bmi_api"),
            {"weight_kg": 65, "height_cm": 170},
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["category_code"], "NORMAL")
        self.assertEqual(payload["recommended_goal"]["code"], Exercise.Goal.STRENGTH)

    def test_bmi_api_validates_input(self):
        response = self.client.get(
            reverse("polls:bmi_api"),
            {"weight_kg": -2, "height_cm": 0},
        )
        self.assertEqual(response.status_code, 400)
        payload = response.json()
        self.assertIn("errors", payload)


class ExerciseDbMappingTests(TestCase):
    def test_map_exercisedb_bodyweight_record(self):
        raw_exercise = {
            "name": "inverted row bent knees",
            "equipments": ["body weight"],
            "bodyParts": ["back"],
            "targetMuscles": ["upper back"],
            "instructions": [
                "Step:1 Set up a bar at waist height and lie underneath it.",
                "Step:2 Grab the bar with an overhand grip.",
            ],
            "gifUrl": "https://static.exercisedb.dev/media/VPPtusI.gif",
        }

        mapped = map_exercisedb_exercise(raw_exercise)

        self.assertIsNotNone(mapped)
        self.assertEqual(mapped["name"], "inverted row bent knees")
        self.assertEqual(mapped["place"], Exercise.Place.HOME)
        self.assertEqual(mapped["goal"], Exercise.Goal.GAIN_MUSCLE)
        self.assertFalse(mapped["requires_equipment"])

    def test_map_exercisedb_machine_record(self):
        raw_exercise = {
            "name": "machine chest press",
            "equipments": ["machine"],
            "bodyParts": ["chest"],
            "targetMuscles": ["pectorals"],
            "instructions": [
                "Step:1 Adjust the seat.",
                "Step:2 Push the handles forward.",
                "Step:3 Return slowly.",
                "Step:4 Repeat.",
                "Step:5 Keep shoulders down.",
            ],
        }

        mapped = map_exercisedb_exercise(raw_exercise)

        self.assertIsNotNone(mapped)
        self.assertEqual(mapped["place"], Exercise.Place.GYM)
        self.assertEqual(mapped["goal"], Exercise.Goal.GAIN_MUSCLE)
        self.assertTrue(mapped["requires_equipment"])
        self.assertEqual(mapped["level"], Exercise.Level.INTERMEDIATE)
