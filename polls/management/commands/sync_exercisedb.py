from urllib.error import HTTPError, URLError

from django.core.management.base import BaseCommand, CommandError

from polls.models import Exercise
from polls.services.exercisedb import (
    fetch_exercisedb_exercises,
    map_exercisedb_exercise,
)


class Command(BaseCommand):
    help = "Importa ejercicios desde ExerciseDB API al modelo local Exercise."

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit",
            type=int,
            default=50,
            help="Numero de ejercicios a solicitar (maximo sugerido por request).",
        )
        parser.add_argument(
            "--offset",
            type=int,
            default=0,
            help="Offset inicial para paginacion.",
        )

    def handle(self, *args, **options):
        limit = options["limit"]
        offset = options["offset"]

        if limit <= 0:
            raise CommandError("--limit debe ser mayor a 0.")
        if offset < 0:
            raise CommandError("--offset no puede ser negativo.")

        try:
            raw_exercises = fetch_exercisedb_exercises(limit=limit, offset=offset)
        except (HTTPError, URLError, TimeoutError) as error:
            raise CommandError(f"No se pudo consultar ExerciseDB: {error}") from error

        created = 0
        updated = 0
        skipped = 0

        for raw_exercise in raw_exercises:
            mapped = map_exercisedb_exercise(raw_exercise)
            if not mapped:
                skipped += 1
                continue

            _, was_created = Exercise.objects.update_or_create(
                name=mapped["name"],
                defaults=mapped,
            )

            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                (
                    "Sync ExerciseDB completado. "
                    f"Recibidos: {len(raw_exercises)} | "
                    f"Creados: {created} | Actualizados: {updated} | "
                    f"Omitidos: {skipped}"
                )
            )
        )
