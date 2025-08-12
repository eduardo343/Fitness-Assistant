"""
Configuración de la aplicación Fitness Assistant
"""

import os
from pathlib import Path

# Directorios del proyecto
BASE_DIR = Path(__file__).parent.parent
SRC_DIR = BASE_DIR / "src"
DATA_DIR = BASE_DIR / "data"

# Crear directorio de datos si no existe
DATA_DIR.mkdir(exist_ok=True)

# Configuración de la aplicación
APP_CONFIG = {
    "title": "Fitness Assistant",
    "icon": "💪",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Configuración de base de datos
DATABASE_CONFIG = {
    "file_path": DATA_DIR / "fitness_data.json",
    "backup_enabled": True,
    "backup_interval": 24  # horas
}

# Configuración de visualizaciones
CHART_CONFIG = {
    "theme": "streamlit",
    "color_palette": ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"],
    "default_height": 400
}

# Ejercicios predefinidos por categoría y nivel
EXERCISE_DATABASE = {
    "fuerza": {
        "principiante": [
            {"name": "Flexiones", "sets": "3 x 8-12", "description": "Ejercicio básico de empuje"},
            {"name": "Sentadillas", "sets": "3 x 10-15", "description": "Fortalece piernas y glúteos"},
            {"name": "Plancha", "sets": "3 x 30s", "description": "Core y estabilidad"},
            {"name": "Burpees", "sets": "3 x 5-8", "description": "Ejercicio completo"},
        ],
        "intermedio": [
            {"name": "Flexiones diamante", "sets": "3 x 8-12", "description": "Mayor dificultad en tríceps"},
            {"name": "Sentadillas con salto", "sets": "3 x 10-12", "description": "Añade componente pliométrico"},
            {"name": "Mountain climbers", "sets": "3 x 20", "description": "Cardio y core"},
            {"name": "Lunges", "sets": "3 x 12 c/u", "description": "Trabajo unilateral de piernas"},
        ],
        "avanzado": [
            {"name": "Flexiones con palmada", "sets": "3 x 6-10", "description": "Potencia explosiva"},
            {"name": "Pistol squats", "sets": "3 x 5 c/u", "description": "Fuerza unilateral avanzada"},
            {"name": "Handstand push-ups", "sets": "3 x 3-8", "description": "Fuerza vertical avanzada"},
            {"name": "Single leg burpees", "sets": "3 x 6 c/u", "description": "Coordinación y fuerza"},
        ]
    },
    "cardio": {
        "principiante": [
            {"name": "Caminata rápida", "duration": "15-20 min", "intensity": "Moderada"},
            {"name": "Trote ligero", "duration": "10-15 min", "intensity": "Moderada"},
            {"name": "Jumping jacks", "duration": "3 x 30s", "intensity": "Moderada"},
            {"name": "Step ups", "duration": "3 x 45s", "intensity": "Baja-Moderada"},
        ],
        "intermedio": [
            {"name": "Correr", "duration": "20-30 min", "intensity": "Moderada-Alta"},
            {"name": "HIIT básico", "duration": "15-20 min", "intensity": "Alta"},
            {"name": "Saltar cuerda", "duration": "10-15 min", "intensity": "Alta"},
            {"name": "Sprint intervals", "duration": "15-20 min", "intensity": "Muy Alta"},
        ],
        "avanzado": [
            {"name": "HIIT avanzado", "duration": "20-30 min", "intensity": "Muy Alta"},
            {"name": "Tabata", "duration": "16-20 min", "intensity": "Máxima"},
            {"name": "Sprint hills", "duration": "20-25 min", "intensity": "Muy Alta"},
            {"name": "Plyometrics", "duration": "15-20 min", "intensity": "Alta"},
        ]
    },
    "flexibilidad": {
        "principiante": [
            {"name": "Estiramiento de cuello", "duration": "30s x 3", "type": "Estático"},
            {"name": "Estiramiento de brazos", "duration": "30s x 3", "type": "Estático"},
            {"name": "Torsiones suaves", "duration": "30s x 3", "type": "Dinámico"},
        ],
        "intermedio": [
            {"name": "Yoga básico", "duration": "20-30 min", "type": "Flujo"},
            {"name": "Estiramiento dinámico", "duration": "15-20 min", "type": "Dinámico"},
            {"name": "Pilates", "duration": "30-45 min", "type": "Control"},
        ],
        "avanzado": [
            {"name": "Yoga avanzado", "duration": "45-60 min", "type": "Flujo avanzado"},
            {"name": "Contorsiones", "duration": "30-45 min", "type": "Extremo"},
            {"name": "Flexibilidad extrema", "duration": "45-60 min", "type": "Especializado"},
        ]
    }
}

# Cálculos de calorías por actividad (calorías por minuto por 70kg)
CALORIES_PER_MINUTE = {
    "Caminar": {"Baja": 3, "Moderada": 4, "Alta": 5},
    "Trotar": {"Baja": 6, "Moderada": 8, "Alta": 10},
    "Correr": {"Baja": 8, "Moderada": 11, "Alta": 14},
    "Ciclismo": {"Baja": 4, "Moderada": 6, "Alta": 9},
    "Natación": {"Baja": 6, "Moderada": 8, "Alta": 11},
    "Yoga": {"Baja": 2, "Moderada": 3, "Alta": 4},
    "Pesas": {"Baja": 3, "Moderada": 5, "Alta": 7}
}

# Categorías de IMC
BMI_CATEGORIES = {
    (0, 18.5): {"category": "Bajo peso", "color": "#3498db", "emoji": "🔵"},
    (18.5, 25): {"category": "Peso normal", "color": "#2ecc71", "emoji": "🟢"},
    (25, 30): {"category": "Sobrepeso", "color": "#f39c12", "emoji": "🟡"},
    (30, float('inf')): {"category": "Obesidad", "color": "#e74c3c", "emoji": "🔴"}
}

# Recursos científicos
SCIENTIFIC_RESOURCES = {
    "Artículos de Investigación": [
        {
            "title": "Effects of High-Intensity Interval Training vs Moderate-Intensity Training",
            "summary": "Comparación de efectividad entre HIIT y entrenamiento moderado",
            "category": "Cardio"
        },
        {
            "title": "The Role of Protein in Muscle Recovery and Growth",
            "summary": "Importancia de la proteína en la recuperación muscular",
            "category": "Nutrición"
        },
        {
            "title": "Sleep and Exercise Performance: A Systematic Review",
            "summary": "Relación entre calidad del sueño y rendimiento deportivo",
            "category": "Recuperación"
        }
    ],
    "Guías Nutricionales": [
        {
            "title": "Macronutrientes para Deportistas",
            "summary": "Distribución óptima de carbohidratos, proteínas y grasas",
            "category": "Nutrición básica"
        },
        {
            "title": "Hidratación en el Ejercicio",
            "summary": "Estrategias de hidratación antes, durante y después del ejercicio",
            "category": "Hidratación"
        },
        {
            "title": "Suplementación Deportiva Basada en Evidencia",
            "summary": "Suplementos con respaldo científico para el rendimiento",
            "category": "Suplementos"
        }
    ],
    "Técnicas de Entrenamiento": [
        {
            "title": "Periodización del Entrenamiento de Fuerza",
            "summary": "Cómo estructurar el entrenamiento a largo plazo",
            "category": "Planificación"
        },
        {
            "title": "Técnicas de Recuperación Activa",
            "summary": "Métodos para acelerar la recuperación post-ejercicio",
            "category": "Recuperación"
        },
        {
            "title": "Prevención de Lesiones en el Deporte",
            "summary": "Estrategias para reducir el riesgo de lesiones",
            "category": "Prevención"
        }
    ]
}

# Configuración de logging
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": DATA_DIR / "fitness_app.log"
}