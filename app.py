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
