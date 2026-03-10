# Fitness Assistant

Aplicacion Django para recomendar ejercicios y calcular IMC.

Estado actual: `demo`.

Eso significa:

- usa `sqlite` local y datos seed para lectura y exploracion;
- no esta pensado todavia para persistencia multiusuario ni panel operativo real;
- la configuracion separa `local` y `production` para evitar mezclar defaults de desarrollo con despliegue.

## Desarrollo local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
python manage.py migrate
python manage.py seed_exercises
python manage.py runserver
```

Luego abre `http://127.0.0.1:8000`.

## Calidad y pruebas

Comandos utiles para validar el proyecto localmente:

```bash
ruff check .
ruff format --check manage.py mysite api polls
mypy mysite polls
python manage.py check
python manage.py test
```

## Catalogo e idiomas

- La interfaz soporta ingles y espanol.
- Los ejercicios seed del proyecto se guardan en espanol.
- Los ejercicios importados desde ExerciseDB se guardan en ingles.
- Cuando la interfaz esta en espanol, el recomendador prioriza ejercicios en espanol si existen para esos filtros.

Para importar mas ejercicios desde ExerciseDB:

```bash
python manage.py sync_exercisedb --limit 50 --offset 0
```

## Despliegue en Vercel

El proyecto ya incluye:

- `api/wsgi.py` como entrypoint serverless para Django.
- `vercel.json` con rewrite global a la funcion Python.
- `buildCommand` que ejecuta migraciones, seed base y `collectstatic`.
- configuracion de produccion para `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` y sesiones firmadas en cookies.

## Configuracion por entorno

- `DJANGO_ENV=local` usa `mysite/settings/local.py`.
- `DJANGO_ENV=production` usa `mysite/settings/production.py`.
- `mysite/settings/base.py` contiene lo comun entre ambos.
- Si no defines `DJANGO_ENV`, el proyecto usa `local`, salvo que detecte entorno Vercel.

### Variables de entorno recomendadas

- `DJANGO_SECRET_KEY` o `SECRET_KEY`: una de las dos es obligatoria en produccion.
- `DJANGO_ALLOWED_HOSTS`: lista separada por comas para dominios adicionales.
- `DJANGO_CSRF_TRUSTED_ORIGINS`: lista separada por comas para origenes extra.
- `ENABLE_ADMIN`: deja `false` si usas la base SQLite empaquetada como solo lectura.

### Nota sobre base de datos

Por defecto el despliegue usa `db.sqlite3` y lo reconstruye en build con `migrate` + `seed_exercises`. Esta configuracion funciona bien para una app de lectura o demo. Si necesitas datos persistentes o operaciones de escritura reales en produccion, cambia a una base de datos gestionada externa.
