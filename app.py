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
