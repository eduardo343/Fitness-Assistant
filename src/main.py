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
                "principiante": [
                    {"name": "Sentadillas con peso corporal", "sets": "3x8-12", "desc": "Cuádriceps, glúteos, core"},
                    {"name": "Flexiones en rodillas/pared", "sets": "3x6-10", "desc": "Pecho, tríceps, deltoides"},
                    {"name": "Plancha estática", "sets": "3x20-30s", "desc": "Core, estabilidad"},
                    {"name": "Puente de glúteos", "sets": "3x10-15", "desc": "Glúteos, isquiotibiales"},
                    {"name": "Dead bug", "sets": "3x8 c/lado", "desc": "Core profundo, coordinación"},
                    {"name": "Wall sits", "sets": "3x20-30s", "desc": "Cuádriceps, resistencia"},
                    {"name": "Bird dog", "sets": "3x8 c/lado", "desc": "Core, espalda baja, equilibrio"}
                ],
                "intermedio": [
                    {"name": "Sentadillas goblet", "sets": "4x10-15", "desc": "Cuádriceps, glúteos, core"},
                    {"name": "Flexiones estándar", "sets": "4x8-15", "desc": "Pecho, tríceps, core"},
                    {"name": "Peso muerto rumano (mancuernas)", "sets": "4x8-12", "desc": "Isquiotibiales, glúteos"},
                    {"name": "Pike push-ups", "sets": "3x6-10", "desc": "Hombros, tríceps"},
                    {"name": "Lunges walking", "sets": "3x12 c/pierna", "desc": "Cuádriceps, glúteos, equilibrio"},
                    {"name": "Plancha con elevación de piernas", "sets": "3x8-10 c/lado", "desc": "Core, glúteos"},
                    {"name": "Russian twists", "sets": "3x20-30", "desc": "Oblicuos, core rotacional"},
                    {"name": "Inverted rows", "sets": "3x8-12", "desc": "Dorsales, romboides, bíceps"}
                ],
                "avanzado": [
                    {"name": "Pistol squats asistidas", "sets": "4x5-8 c/pierna", "desc": "Fuerza unilateral, equilibrio"},
                    {"name": "Archer push-ups", "sets": "4x6-10 c/lado", "desc": "Pecho unilateral, core"},
                    {"name": "Handstand progression", "sets": "4x30-60s", "desc": "Hombros, core, equilibrio"},
                    {"name": "Single-leg deadlifts", "sets": "4x8-10 c/pierna", "desc": "Isquiotibiales, glúteos, equilibrio"},
                    {"name": "L-sit progression", "sets": "4x15-30s", "desc": "Core avanzado, flexores cadera"},
                    {"name": "Muscle-ups progression", "sets": "3x3-6", "desc": "Tracción completa, transición"},
                    {"name": "Human flag progression", "sets": "3x10-20s", "desc": "Core lateral, fuerza total"},
                    {"name": "Planche progression", "sets": "4x15-30s", "desc": "Empuje avanzado, core"}
                ]
            },
            "cardio": {
                "principiante": [
                    {"name": "Caminata moderada", "duration": "20-30 min", "intensity": "60-70% FC máx", "desc": "Base aeróbica, adaptación cardiovascular"},
                    {"name": "Marcha en el lugar", "duration": "5-10 min", "intensity": "Baja", "desc": "Calentamiento, movilidad"},
                    {"name": "Step-ups lentos", "duration": "3x2 min", "intensity": "Moderada", "desc": "Cardio de bajo impacto"},
                    {"name": "Arm circles + marching", "duration": "10-15 min", "intensity": "Baja-Moderada", "desc": "Cardio sin impacto"},
                    {"name": "Tai chi básico", "duration": "15-20 min", "intensity": "Baja", "desc": "Cardio meditativo, equilibrio"},
                    {"name": "Swimming (si disponible)", "duration": "15-25 min", "intensity": "Moderada", "desc": "Cardio sin impacto, cuerpo completo"}
                ],
                "intermedio": [
                    {"name": "HIIT básico (Tabata)", "duration": "16-20 min", "intensity": "85-95% FC máx", "desc": "Mejora VO2 máx, quema grasa"},
                    {"name": "Circuit training", "duration": "25-35 min", "intensity": "70-85% FC máx", "desc": "Cardio + fuerza"},
                    {"name": "Running intervals", "duration": "25-30 min", "intensity": "Variable", "desc": "Velocidad, resistencia"},
                    {"name": "Burpees EMOM", "duration": "15-20 min", "intensity": "Alta", "desc": "Potencia, resistencia anaeróbica"},
                    {"name": "Jump rope intervals", "duration": "20-25 min", "intensity": "Moderada-Alta", "desc": "Coordinación, cardio"},
                    {"name": "Battle ropes", "duration": "15-20 min", "intensity": "Alta", "desc": "Potencia, core, cardio"}
                ],
                "avanzado": [
                    {"name": "HIIT avanzado (Sprint intervals)", "duration": "30-40 min", "intensity": "90-100% FC máx", "desc": "Potencia aeróbica máxima"},
                    {"name": "Tabata extremo", "duration": "20-32 min", "intensity": "Máxima", "desc": "Capacidad anaeróbica"},
                    {"name": "CrossFit WODs", "duration": "15-45 min", "intensity": "Variable", "desc": "Fitness funcional"},
                    {"name": "Spartan race training", "duration": "45-60 min", "intensity": "Alta", "desc": "Resistencia funcional"},
                    {"name": "Boxing combinations", "duration": "30-45 min", "intensity": "Alta", "desc": "Potencia, coordinación"},
                    {"name": "Metabolic circuits", "duration": "35-50 min", "intensity": "Very High", "desc": "EPOC máximo, quema calórica"}
                ]
            },
            "flexibilidad": {
                "principiante": [
                    {"name": "Cat-cow stretches", "duration": "2x10", "type": "Dinámico", "desc": "Movilidad espinal"},
                    {"name": "Hip circles", "duration": "10 c/dirección", "type": "Dinámico", "desc": "Movilidad cadera"},
                    {"name": "Shoulder rolls", "duration": "10 adelante/atrás", "type": "Dinámico", "desc": "Movilidad hombros"},
                    {"name": "Ankle circles", "duration": "10 c/pie", "type": "Dinámico", "desc": "Movilidad tobillo"},
                    {"name": "Gentle spinal twists", "duration": "30s c/lado", "type": "Estático", "desc": "Flexibilidad espinal"},
                    {"name": "Seated forward fold", "duration": "30-60s", "type": "Estático", "desc": "Isquiotibiales, espalda baja"},
                    {"name": "Chest doorway stretch", "duration": "30s c/brazo", "type": "Estático", "desc": "Pectorales, hombros anteriores"}
                ],
                "intermedio": [
                    {"name": "Dynamic warm-up sequence", "duration": "10-15 min", "type": "Dinámico", "desc": "Preparación completa"},
                    {"name": "Yoga flow básico", "duration": "20-30 min", "type": "Flujo", "desc": "Flexibilidad, mindfulness"},
                    {"name": "PNF stretching", "duration": "15-20 min", "type": "PNF", "desc": "Facilitación neuromuscular"},
                    {"name": "Pigeon pose variations", "duration": "2-3 min c/lado", "type": "Estático profundo", "desc": "Flexores cadera, glúteos"},
                    {"name": "Thoracic spine mobility", "duration": "10-15 min", "type": "Correctivo", "desc": "Postura, movilidad torácica"},
                    {"name": "Deep hip flexor stretches", "duration": "90s c/lado", "type": "Estático", "desc": "Flexores cadera profundos"}
                ],
                "avanzado": [
                    {"name": "Advanced yoga flows", "duration": "45-60 min", "type": "Vinyasa avanzado", "desc": "Flexibilidad extrema"},
                    {"name": "Contortion training", "duration": "60-90 min", "type": "Especializado", "desc": "Hiperflexibilidad"},
                    {"name": "Oversplits training", "duration": "30-45 min", "type": "Progresión extrema", "desc": "Flexibilidad máxima"},
                    {"name": "Backbending intensive", "duration": "45-60 min", "type": "Especializado", "desc": "Extensión espinal extrema"},
                    {"name": "Advanced PNF protocols", "duration": "30-45 min", "type": "PNF avanzado", "desc": "Técnicas neurofisiológicas"},
                    {"name": "Martial arts flexibility", "duration": "60-75 min", "type": "Funcional avanzado", "desc": "Flexibilidad dinámica extrema"}
                ]
            }
        }
    
    def generate_routine(self, workout_type, level, duration):
        exercises = self.exercises.get(workout_type, {}).get(level, [])
        routine = []
        
        # Si no hay ejercicios, usar predeterminados
        if not exercises:
            exercises = [{"name": "Ejercicio básico", "sets": "3x10", "desc": "Movimiento general"}]
        
        if duration <= 15:
            exercise_count = 3
        elif duration <= 30:
            exercise_count = 5
        elif duration <= 45:
            exercise_count = 7
        else:
            exercise_count = 8
        
        import random
        selected = random.sample(exercises, min(exercise_count, len(exercises)))
        
        for exercise_data in selected:
            if isinstance(exercise_data, dict):
                # Nuevo formato con datos científicos
                routine.append({
                    "exercise": exercise_data["name"],
                    "sets": exercise_data.get("sets", exercise_data.get("duration", "Ver descripción")),
                    "description": exercise_data.get("desc", "Ejercicio funcional")
                })
            else:
                # Formato legacy (string)
                if workout_type == "fuerza":
                    sets = "3 series x 10-15 reps"
                elif workout_type == "cardio":
                    sets = f"{duration//exercise_count} minutos"
                else:
                    sets = "30 segundos hold"
                
                routine.append({
                    "exercise": exercise_data,
                    "sets": sets,
                    "description": "Ejercicio básico"
                })
        
        return routine
    
    def render(self):
        st.subheader("🏋️‍♂️ Generador de Rutinas Científicas")
        
        # Información sobre la base científica
        with st.expander("ℹ️ Base Científica de los Ejercicios"):
            st.markdown("""
            **Rutinas basadas en:**
            - **ACSM Guidelines**: Recomendaciones del Colegio Americano de Medicina Deportiva
            - **Principios de Sobrecarga Progresiva**: Incremento gradual de intensidad
            - **Especificidad**: Ejercicios funcionales para objetivos específicos
            - **Periodización**: Progresión estructurada por niveles
            - **Evidencia en PubMed**: Ejercicios con respaldo en literatura científica
            """)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            workout_type = st.selectbox("Tipo de entrenamiento", 
                                      ["fuerza", "cardio", "flexibilidad"])
        
        with col2:
            level = st.selectbox("Nivel", ["principiante", "intermedio", "avanzado"])
        
        with col3:
            duration = st.slider("Duración (minutos)", 10, 90, 30)
        
        # Información específica del nivel seleccionado
        level_info = {
            "principiante": "🟢 **Principiante**: Adaptación neuromuscular, técnica básica, volumen moderado",
            "intermedio": "🟡 **Intermedio**: Progresiones complejas, mayor intensidad, variabilidad",
            "avanzado": "🔴 **Avanzado**: Movimientos especializados, alta intensidad, técnicas avanzadas"
        }
        
        st.info(level_info[level])
        
        if st.button("🎯 Generar Rutina Científica"):
            routine = self.generate_routine(workout_type, level, duration)
            
            st.success(f"🔬 Rutina de {workout_type.upper()} - {level.upper()} ({duration} min)")
            st.markdown("### 📋 Tu Rutina Personalizada")
            
            # Mostrar ejercicios con información científica
            for i, exercise in enumerate(routine, 1):
                with st.container():
                    col1, col2 = st.columns([3, 2])
                    
                    with col1:
                        st.markdown(f"#### {i}. {exercise['exercise']}")
                        st.write(f"**📊 Sets/Tiempo:** {exercise['sets']}")
                        
                    with col2:
                        st.write(f"**🎯 Músculos:** {exercise.get('description', 'Funcional')}")
                    
                    # Agregar tips específicos según el tipo
                    if workout_type == "fuerza":
                        st.caption("💡 **Tip**: Mantén 48-72h de descanso entre sesiones del mismo grupo muscular")
                    elif workout_type == "cardio":
                        st.caption("💡 **Tip**: Mantén tu frecuencia cardíaca en la zona objetivo")
                    else:
                        st.caption("💡 **Tip**: Mantén cada estiramiento por 15-30 segundos mínimo")
                    
                    st.divider()
            
            # Recomendaciones científicas adicionales
            st.markdown("### 🧬 Recomendaciones Científicas")
            
            recommendations = {
                "fuerza": {
                    "principiante": "• **Frecuencia**: 2-3 días/semana • **Descanso**: 2-3 min entre series • **Progresión**: +5% carga semanal",
                    "intermedio": "• **Frecuencia**: 3-4 días/semana • **Descanso**: 2-4 min entre series • **Progresión**: Periodización ondulante",
                    "avanzado": "• **Frecuencia**: 4-6 días/semana • **Descanso**: 3-5 min entre series • **Progresión**: Periodización compleja"
                },
                "cardio": {
                    "principiante": "• **Intensidad**: 60-70% FC máx • **Progresión**: +10% volumen/semana • **Recuperación**: 1 día completo",
                    "intermedio": "• **Intensidad**: 70-85% FC máx • **HIIT**: 2-3x/semana • **Recuperación**: Activa recomendada",
                    "avanzado": "• **Intensidad**: 85-95% FC máx • **Periodización**: Bloques especializados • **Monitoreo**: HRV recomendado"
                },
                "flexibilidad": {
                    "principiante": "• **Frecuencia**: Diaria • **Duración**: 15-30s por estiramiento • **Momento**: Post-ejercicio",
                    "intermedio": "• **PNF**: 2-3x/semana • **Duración**: 30-60s • **Progresión**: ROM gradual",
                    "avanzado": "• **Especialización**: Diaria • **Técnicas**: PNF + estático • **Duración**: 60-120s"
                }
            }
            
            st.info(recommendations[workout_type][level])
            
            # Guardar rutina con clave única
            save_key = f"save_routine_{workout_type}_{level}_{duration}_{len(routine)}"
            if st.button("💾 Guardar Rutina Científica", key=save_key):
                db = DatabaseManager()
                workout = {
                    "date": datetime.now().isoformat(),
                    "type": workout_type,
                    "level": level,
                    "duration": duration,
                    "exercises": routine,
                    "scientific_basis": True
                }
                db.add_workout(workout)
                st.success("✅ Rutina científica guardada con éxito!")
                st.balloons()

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
    
    # Inicializar session state para navegación
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Dashboard"
    
    # Título principal
    st.markdown('<h1 class="main-header">💪 Fitness Assistant</h1>', 
                unsafe_allow_html=True)
    
    # Sidebar con navegación
    st.sidebar.title("Navegación")
    
    # Lista de páginas disponibles
    pages = [
        "Dashboard",
        "Calculadora IMC", 
        "Generador de Rutinas",
        "Planificador de Cardio",
        "Seguimiento de Progreso",
        "Recursos Científicos"
    ]
    
    # Selectbox que se sincroniza con session_state
    page = st.sidebar.selectbox(
        "Selecciona una opción:", 
        pages,
        index=pages.index(st.session_state.current_page)
    )
    
    # Actualizar session_state si cambió desde el sidebar
    if page != st.session_state.current_page:
        st.session_state.current_page = page
    
    # Renderizar páginas usando session_state
    current_page = st.session_state.current_page
    
    if current_page == "Dashboard":
        st.write("¡Bienvenido a tu asistente fitness personal!")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🏋️‍♂️ Crear Rutina", key="nav_rutina", use_container_width=True):
                st.session_state.current_page = "Generador de Rutinas"
                st.rerun()
        
        with col2:
            if st.button("🏃‍♂️ Planear Cardio", key="nav_cardio", use_container_width=True):
                st.session_state.current_page = "Planificador de Cardio"
                st.rerun()
        
        with col3:
            if st.button("📊 Ver Progreso", key="nav_progreso", use_container_width=True):
                st.session_state.current_page = "Seguimiento de Progreso"
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
        
        # Accesos rápidos adicionales
        st.markdown("---")
        st.subheader("🚀 Más Herramientas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Calcular IMC", key="nav_imc", use_container_width=True):
                st.session_state.current_page = "Calculadora IMC"
                st.rerun()
        
        with col2:
            if st.button("📚 Ver Recursos", key="nav_recursos", use_container_width=True):
                st.session_state.current_page = "Recursos Científicos"
                st.rerun()
        
        # Información adicional
        st.markdown("---")
        st.info("💡 **Tip:** También puedes navegar usando el menú de la izquierda o estos botones para acceder rápidamente a cada sección.")
    
    elif current_page == "Calculadora IMC":
        BMICalculator().render()
    
    elif current_page == "Generador de Rutinas":
        RoutineGenerator().render()
    
    elif current_page == "Planificador de Cardio":
        CardioPlanner().render()
    
    elif current_page == "Seguimiento de Progreso":
        ProgressTracker().render()
    
    elif current_page == "Recursos Científicos":
        ScientificResources().render()

if __name__ == "__main__":
    main()