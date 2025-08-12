import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import json
import os

# Configuración de la página
st.set_page_config(
    page_title="Fitness Assistant",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
def create_custom_css():
    return """
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #FF6B6B;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .exercise-card {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    </style>
    """

# Clase para manejar datos (simulando base de datos)
class DatabaseManager:
    def __init__(self):
        self.data_file = "fitness_data.json"
        self.load_data()
    
    def load_data(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    self.data = json.load(f)
            else:
                self.data = {
                    "workouts": [],
                    "progress": [],
                    "user_profile": {}
                }
        except:
            self.data = {
                "workouts": [],
                "progress": [],
                "user_profile": {}
            }
    
    def save_data(self):
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.data, f, default=str)
        except Exception as e:
            st.error(f"Error guardando datos: {e}")
    
    def add_workout(self, workout):
        self.data["workouts"].append(workout)
        self.save_data()
    
    def add_progress(self, progress):
        self.data["progress"].append(progress)
        self.save_data()
    
    def get_workouts(self):
        return self.data["workouts"]
    
    def get_progress(self):
        return self.data["progress"]

# Calculadora de IMC
class BMICalculator:
    @staticmethod
    def calculate_bmi(weight, height):
        bmi = weight / (height ** 2)
        return round(bmi, 2)
    
    @staticmethod
    def get_bmi_category(bmi):
        if bmi < 18.5:
            return "Bajo peso", "🔵"
        elif bmi < 25:
            return "Peso normal", "🟢"
        elif bmi < 30:
            return "Sobrepeso", "🟡"
        else:
            return "Obesidad", "🔴"
    
    def render(self):
        st.subheader("📊 Calculadora de IMC")
        
        col1, col2 = st.columns(2)
        
        with col1:
            weight = st.number_input("Peso (kg)", min_value=30.0, max_value=300.0, value=70.0)
        
        with col2:
            height = st.number_input("Altura (m)", min_value=1.0, max_value=2.5, value=1.70)
        
        if st.button("Calcular IMC"):
            bmi = self.calculate_bmi(weight, height)
            category, emoji = self.get_bmi_category(bmi)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("IMC", f"{bmi}")
            
            with col2:
                st.metric("Categoría", f"{emoji} {category}")
            
            with col3:
                ideal_weight = 22 * (height ** 2)
                st.metric("Peso ideal aprox.", f"{ideal_weight:.1f} kg")

# Generador de rutinas
class RoutineGenerator:
    def __init__(self):
        self.exercises = {
            "fuerza": {
                "principiante": ["Flexiones", "Sentadillas", "Plancha", "Burpees"],
                "intermedio": ["Flexiones diamante", "Sentadillas con salto", "Mountain climbers", "Lunges"],
                "avanzado": ["Flexiones con palmada", "Pistol squats", "Handstand push-ups", "Single leg burpees"]
            },
            "cardio": {
                "principiante": ["Caminata rápida", "Trote ligero", "Jumping jacks", "Step ups"],
                "intermedio": ["Correr", "HIIT básico", "Saltar cuerda", "Sprint intervals"],
                "avanzado": ["HIIT avanzado", "Tabata", "Sprint hills", "Plyometrics"]
            },
            "flexibilidad": {
                "principiante": ["Estiramiento de cuello", "Estiramiento de brazos", "Torsiones suaves"],
                "intermedio": ["Yoga básico", "Estiramiento dinámico", "Pilates"],
                "avanzado": ["Yoga avanzado", "Contorsiones", "Flexibilidad extrema"]
            }
        }
    
    def generate_routine(self, workout_type, level, duration):
        exercises = self.exercises.get(workout_type, {}).get(level, [])
        routine = []
        
        # Si no hay ejercicios, usar predeterminados
        if not exercises:
            exercises = ["Ejercicio básico", "Movimiento funcional", "Actividad general"]
        
        if duration <= 15:
            exercise_count = 3
        elif duration <= 30:
            exercise_count = 5
        else:
            exercise_count = 7
        
        import random
        selected = random.choices(exercises, k=min(exercise_count, len(exercises)))
        
        for i, exercise in enumerate(selected):
            if workout_type == "fuerza":
                sets = "3 series x 10-15 reps"
            elif workout_type == "cardio":
                sets = f"{duration//exercise_count} minutos"
            else:
                sets = "30 segundos hold"
            
            routine.append({"exercise": exercise, "sets": sets})
        
        return routine
    
    def render(self):
        st.subheader("🏋️‍♂️ Generador de Rutinas")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            workout_type = st.selectbox("Tipo de entrenamiento", 
                                      ["fuerza", "cardio", "flexibilidad"])
        
        with col2:
            level = st.selectbox("Nivel", ["principiante", "intermedio", "avanzado"])
        
        with col3:
            duration = st.slider("Duración (minutos)", 10, 60, 30)
        
        if st.button("Generar Rutina"):
            routine = self.generate_routine(workout_type, level, duration)
            
            st.success(f"Rutina de {workout_type} - {level} ({duration} min)")
            
            # Mostrar ejercicios con mejor formato
            for i, exercise in enumerate(routine, 1):
                with st.container():
                    st.markdown(f"### {i}. {exercise['exercise']}")
                    st.write(f"**Sets:** {exercise['sets']}")
                    st.divider()
            
            # Guardar rutina con clave única
            save_key = f"save_routine_{workout_type}_{level}_{duration}"
            if st.button("Guardar Rutina", key=save_key):
                db = DatabaseManager()
                workout = {
                    "date": datetime.now().isoformat(),
                    "type": workout_type,
                    "level": level,
                    "duration": duration,
                    "exercises": routine
                }
                db.add_workout(workout)
                st.success("Rutina guardada!")

# Planificador de cardio
class CardioPlanner:
    def render(self):
        st.subheader("🏃‍♂️ Planificador de Cardio")
        
        col1, col2 = st.columns(2)
        
        with col1:
            activity = st.selectbox("Actividad", 
                                  ["Caminar", "Trotar", "Correr", "Ciclismo", "Natación"])
            duration = st.number_input("Duración (minutos)", 10, 180, 30)
        
        with col2:
            intensity = st.selectbox("Intensidad", ["Baja", "Moderada", "Alta"])
            weight = st.number_input("Tu peso (kg)", 50, 150, 70)
        
        # Cálculo aproximado de calorías
        calories_per_min = {
            "Caminar": {"Baja": 3, "Moderada": 4, "Alta": 5},
            "Trotar": {"Baja": 6, "Moderada": 8, "Alta": 10},
            "Correr": {"Baja": 8, "Moderada": 11, "Alta": 14},
            "Ciclismo": {"Baja": 4, "Moderada": 6, "Alta": 9},
            "Natación": {"Baja": 6, "Moderada": 8, "Alta": 11}
        }
        
        estimated_calories = calories_per_min[activity][intensity] * duration * (weight/70)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Calorías estimadas", f"{estimated_calories:.0f}")
        
        with col2:
            st.metric("Duración", f"{duration} min")
        
        with col3:
            st.metric("Intensidad", intensity)
        
        if st.button("Registrar Sesión de Cardio"):
            db = DatabaseManager()
            cardio_session = {
                "date": datetime.now().isoformat(),
                "activity": activity,
                "duration": duration,
                "intensity": intensity,
                "calories": estimated_calories
            }
            db.add_progress(cardio_session)
            st.success("Sesión de cardio registrada!")

# Recursos científicos
class ScientificResources:
    def render(self):
        st.subheader("📚 Recursos Científicos")
        
        resources = {
            "Artículos de Investigación": [
                "Effects of High-Intensity Interval Training vs Moderate-Intensity Training",
                "The Role of Protein in Muscle Recovery and Growth",
                "Sleep and Exercise Performance: A Systematic Review"
            ],
            "Guías Nutricionales": [
                "Macronutrientes para Deportistas",
                "Hidratación en el Ejercicio",
                "Suplementación Deportiva Basada en Evidencia"
            ],
            "Técnicas de Entrenamiento": [
                "Periodización del Entrenamiento de Fuerza",
                "Técnicas de Recuperación Activa",
                "Prevención de Lesiones en el Deporte"
            ]
        }
        
        for category, items in resources.items():
            with st.expander(category):
                for item in items:
                    st.markdown(f"• {item}")
                    if st.button(f"Leer más sobre: {item}", key=f"read_{item}"):
                        st.info("Redirigiendo a recursos externos...")

# Seguimiento de progreso
class ProgressTracker:
    def render(self):
        st.subheader("📈 Seguimiento de Progreso")
        
        db = DatabaseManager()
        progress_data = db.get_progress()
        workouts = db.get_workouts()
        
        if not progress_data and not workouts:
            st.info("No hay datos de progreso aún. ¡Empieza a registrar tus entrenamientos!")
            return
        
        # Métricas generales
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Entrenamientos totales", len(workouts))
        
        with col2:
            total_calories = sum([p.get('calories', 0) for p in progress_data])
            st.metric("Calorías quemadas", f"{total_calories:.0f}")
        
        with col3:
            if progress_data:
                avg_duration = sum([p.get('duration', 0) for p in progress_data]) / len(progress_data)
                st.metric("Duración promedio", f"{avg_duration:.0f} min")
        
        # Gráficos
        if progress_data:
            df = pd.DataFrame(progress_data)
            df['date'] = pd.to_datetime(df['date'])
            
            fig = px.line(df, x='date', y='calories', 
                         title='Calorías Quemadas por Sesión')
            st.plotly_chart(fig, use_container_width=True)

# Aplicación principal
def main():
    # CSS personalizado
    st.markdown(create_custom_css(), unsafe_allow_html=True)
    
    # Título principal
    st.markdown('<h1 class="main-header">💪 Fitness Assistant</h1>', 
                unsafe_allow_html=True)
    
    # Sidebar con navegación
    st.sidebar.title("Navegación")
    page = st.sidebar.selectbox("Selecciona una opción:", [
        "Dashboard",
        "Calculadora IMC", 
        "Generador de Rutinas",
        "Planificador de Cardio",
        "Seguimiento de Progreso",
        "Recursos Científicos"
    ])
    
    # Renderizar páginas
    if page == "Dashboard":
        st.write("¡Bienvenido a tu asistente fitness personal!")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🏋️‍♂️ Crear Rutina"):
                st.rerun()  # Esto forzará un rerun pero necesitamos cambiar la página
        
        with col2:
            if st.button("🏃‍♂️ Planear Cardio"):
                st.rerun()
        
        with col3:
            if st.button("📊 Ver Progreso"):
                st.rerun()
        
        # Mostrar información adicional en el dashboard
        st.markdown("---")
        st.subheader("📈 Resumen Rápido")
        
        # Mostrar estadísticas básicas
        db = DatabaseManager()
        workouts = db.get_workouts()
        progress = db.get_progress()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Entrenamientos", len(workouts))
        
        with col2:
            total_calories = sum([p.get('calories', 0) for p in progress])
            st.metric("Calorías quemadas", f"{total_calories:.0f}")
        
        with col3:
            if progress:
                avg_duration = sum([p.get('duration', 0) for p in progress]) / len(progress)
                st.metric("Duración promedio", f"{avg_duration:.0f} min")
            else:
                st.metric("Duración promedio", "0 min")
        
        with col4:
            this_week = len([w for w in workouts if w.get('date', '') > (datetime.now() - pd.Timedelta(days=7)).isoformat()])
            st.metric("Esta semana", f"{this_week}")
        
        # Accesos rápidos con texto
        st.markdown("---")
        st.subheader("🚀 Accesos Rápidos")
        st.info("💡 **Tip:** Usa el menú de la izquierda para navegar entre las diferentes secciones de la aplicación.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**🏋️‍♂️ Generador de Rutinas**")
            st.write("Crea rutinas personalizadas según tu nivel y tiempo disponible")
            
            st.markdown("**📊 Calculadora de IMC**") 
            st.write("Calcula tu índice de masa corporal y obtén recomendaciones")
        
        with col2:
            st.markdown("**🏃‍♂️ Planificador de Cardio**")
            st.write("Planifica sesiones de cardio y calcula calorías quemadas")
            
            st.markdown("**📚 Recursos Científicos**")
            st.write("Accede a información basada en evidencia científica")
    
    elif page == "Calculadora IMC":
        BMICalculator().render()
    
    elif page == "Generador de Rutinas":
        RoutineGenerator().render()
    
    elif page == "Planificador de Cardio":
        CardioPlanner().render()
    
    elif page == "Seguimiento de Progreso":
        ProgressTracker().render()
    
    elif page == "Recursos Científicos":
        ScientificResources().render()

if __name__ == "__main__":
    main()