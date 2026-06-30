import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import requests
from nutrients import NutritionalAnalyzer
import datetime

st.set_page_config(page_title="Health Buddy", page_icon="☁️", layout="wide")

def load_css():
    try:
        with open('style.css', 'r', encoding='utf-8') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception:
        pass

load_css()
analyzer = NutritionalAnalyzer()

st.title("☁️ Your happy health buddy")
st.markdown("Track habits, stay active, and celebrate small wins — with a little smile along the way.")
st.markdown("---")

summary = analyzer.get_daily_summary()

# Sidebar for Goals & Progress
st.sidebar.title("DAILY PROGRESS")

def draw_progress(label, current, goal):
    st.sidebar.write(f"**{label}**: {current:.0f} / {goal}")
    progress = min(current / goal, 1.0) if goal > 0 else 0.0
    st.sidebar.progress(progress)

draw_progress("🔥 Calories (kcal)", summary['calories'], analyzer.goals['calories'])
draw_progress("🥩 Protein (g)", summary['protein'], analyzer.goals['protein'])
draw_progress("🍚 Carbs (g)", summary['carbs'], analyzer.goals['carbs'])
draw_progress("🥑 Fat (g)", summary['fat'], analyzer.goals['fat'])

with st.sidebar.expander("⚙️ Settings (Set Goals)"):
    with st.form("goals_form"):
        new_cal = st.number_input("Calories", value=int(analyzer.goals['calories']))
        new_pro = st.number_input("Protein", value=int(analyzer.goals['protein']))
        new_car = st.number_input("Carbs", value=int(analyzer.goals['carbs']))
        new_fat = st.number_input("Fat", value=int(analyzer.goals['fat']))
        if st.form_submit_button("Save Goals"):
            analyzer.update_goals(new_cal, new_pro, new_car, new_fat)
            st.success("Goals updated!")
            st.rerun()
