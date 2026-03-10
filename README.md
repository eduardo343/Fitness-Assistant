# Fitness Assistant

Aplicacion Django para recomendar ejercicios y calcular IMC.

## Desarrollo local

1. Crea o activa tu entorno virtual.
2. Instala dependencias con `pip install -r requirements.txt`.
3. Ejecuta `python manage.py migrate`.
4. Carga el seed local con `python manage.py seed_exercises`.
5. Inicia el servidor con `python manage.py runserver`.

## Despliegue en Vercel

El proyecto ya incluye:

- `api/wsgi.py` como entrypoint serverless para Django.
- `vercel.json` con rewrite global a la funcion Python.
- `buildCommand` que ejecuta migraciones, seed base y `collectstatic`.
- configuracion de produccion para `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` y sesiones firmadas en cookies.

### Variables de entorno recomendadas

- `DJANGO_SECRET_KEY`: obligatoria en produccion.
- `DJANGO_ALLOWED_HOSTS`: lista separada por comas para dominios adicionales.
- `DJANGO_CSRF_TRUSTED_ORIGINS`: lista separada por comas para origenes extra.
- `ENABLE_ADMIN`: deja `false` si usas la base SQLite empaquetada como solo lectura.

### Nota sobre base de datos

Por defecto el despliegue usa `db.sqlite3` y lo reconstruye en build con `migrate` + `seed_exercises`. Esta configuracion funciona bien para una app de lectura o demo. Si necesitas datos persistentes o operaciones de escritura reales en produccion, cambia a una base de datos gestionada externa.
