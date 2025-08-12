import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
from datetime import datetime
from io import StringIO
import random

# ------------------------------------------------
# Load CSS from an external file
# ------------------------------------------------
def load_css():
    css_file = "styles.css"
    if os.path.exists(css_file):
        with open(css_file, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ------------------------------------------------
# Database Manager with reusable methods
# ------------------------------------------------
class DatabaseManager:
    def __init__(self):
        self.data_file = "fitness_data.json"
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.data = json.load(f)
            except:
                self.data = {"workouts": [], "progress": [], "user_profile": {}}
        else:
            self.data = {"workouts": [], "progress": [], "user_profile": {}}

    def save_data(self):
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.data, f, default=str)
        except Exception as e:
            st.error(f"Error saving data: {e}")

    # CRUD operations
    def add_workout(self, workout):
        self.data["workouts"].append(workout)
        self.save_data()

    def delete_workout(self, index):
        if 0 <= index < len(self.data["workouts"]):
            self.data["workouts"].pop(index)
            self.save_data()

    def add_progress(self, progress):
        self.data["progress"].append(progress)
        self.save_data()

    # Getters
    def get_workouts(self):
        return self.data["workouts"]

    def get_progress(self):
        return self.data["progress"]

    # Stats methods
    def get_total_calories(self):
        return sum([p.get('calories', 0) for p in self.data["progress"]])

    def get_average_duration(self):
        if not self.data["progress"]:
            return 0
        return sum([p.get('duration', 0) for p in self.data["progress"]]) / len(self.data["progress"])

# ------------------------------------------------
# Weekly Stats Visualization
# ------------------------------------------------
def weekly_stats_chart(progress):
    if not progress:
        return
    df = pd.DataFrame(progress)
    df['date'] = pd.to_datetime(df['date'])
    df['week'] = df['date'].dt.strftime('%Y-%U')
    weekly_df = df.groupby('week', as_index=False)['calories'].sum()

    fig = px.bar(weekly_df, x='week', y='calories', title='Calories Burned per Week')
    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------
# CSV Export
# ------------------------------------------------
def export_data_as_csv(data, filename):
    df = pd.DataFrame(data)
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    st.download_button(
        label=f"Download {filename}",
        data=csv_buffer.getvalue(),
        file_name=filename,
        mime="text/csv"
    )

# ------------------------------------------------
# Dashboard Page
# ------------------------------------------------
def dashboard():
    st.subheader("📈 Quick Summary")
    db = DatabaseManager()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Workouts", len(db.get_workouts()))
    col2.metric("Calories Burned", f"{db.get_total_calories():.0f}")
    col3.metric("Avg Duration", f"{db.get_average_duration():.0f} min")
    col4.metric("This Week", len([w for w in db.get_workouts() if w.get('date', '') > (datetime.now() - pd.Timedelta(days=7)).isoformat()]))

    st.markdown("---")
    st.subheader("📊 Weekly Progress")
    weekly_stats_chart(db.get_progress())

    st.markdown("---")
    st.subheader("📂 Manage Workouts")
    workouts = db.get_workouts()
    if workouts:
        df = pd.DataFrame(workouts)
        st.dataframe(df)
        selected_index = st.number_input("Select workout index to delete", min_value=0, max_value=len(workouts)-1, step=1)
        if st.button("Delete Workout"):
            db.delete_workout(selected_index)
            st.success("Workout deleted!")
            st.rerun()

        export_data_as_csv(workouts, "workouts.csv")
    else:
        st.info("No workouts yet.")

    st.markdown("---")
    st.subheader("📂 Export Progress Data")
    progress = db.get_progress()
    if progress:
        export_data_as_csv(progress, "progress.csv")
    else:
        st.info("No progress data yet.")

# ------------------------------------------------
# Main App
# ------------------------------------------------
def main():
    st.set_page_config(page_title="Fitness Assistant", page_icon="💪", layout="wide")
    load_css()

    st.title("💪 Fitness Assistant")
    pages = ["Dashboard", "Other Pages Coming Soon"]
    choice = st.sidebar.selectbox("Navigation", pages)

    if choice == "Dashboard":
        dashboard()
    else:
        st.info("Other pages will be here.")

if __name__ == "__main__":
    main()
