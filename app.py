import streamlit as st
import plotly.graph_objects as go
from nutrients import NutritionalAnalyzer
import datetime

st.set_page_config(page_title="Premium Nutrient Tracker", page_icon="🍎", layout="wide")

# Custom CSS for Premium UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: white;
    }
    
    /* Sidebar Glassmorphism */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.7) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #f8fafc !important;
        font-weight: 600;
    }
    
    /* Input fields */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: rgba(255,255,255,0.05);
        color: white;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 8px;
    }
    
    /* Gradient Button */
    .stButton>button {
        background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(139, 92, 246, 0.4);
        border: none;
        color: white;
    }
    
    /* Expander cards */
    .streamlit-expanderHeader {
        background-color: rgba(255,255,255,0.05);
        border-radius: 8px;
        border: 1px solid rgba(255,255,255,0.05);
    }
</style>
""", unsafe_allow_html=True)

analyzer = NutritionalAnalyzer()

st.title("✨ Premium Nutrient Tracker")
st.markdown("Monitor your daily macros with real-time analytics and beautiful visualizations.")
st.markdown("---")

# Daily Goals Configuration
GOAL_CALORIES = 2000
GOAL_PROTEIN = 150
GOAL_CARBS = 200
GOAL_FAT = 70

summary = analyzer.get_daily_summary()

# Main Layout using Columns
col1, col2 = st.columns([1.5, 1], gap="large")

with col1:
    st.subheader("🍽️ Add a New Meal")
    with st.form("add_meal_form", clear_on_submit=True):
        food_name = st.text_input("Food Name", placeholder="e.g., Grilled Salmon & Quinoa")
        
        c1, c2, c3, c4 = st.columns(4)
        with c1: calories = st.number_input("Calories", min_value=0.0, step=10.0)
        with c2: protein = st.number_input("Protein (g)", min_value=0.0, step=1.0)
        with c3: carbs = st.number_input("Carbs (g)", min_value=0.0, step=1.0)
        with c4: fat = st.number_input("Fat (g)", min_value=0.0, step=1.0)
            
        submit_button = st.form_submit_button(label="Log Meal 🚀")

    if submit_button:
        if food_name.strip():
            analyzer.add_meal(food_name, calories, protein, carbs, fat)
            st.success(f"Successfully logged '{food_name}'!")
            st.rerun()
        else:
            st.error("Please enter a valid food name.")
            
    st.subheader("📅 Today's Log")
    today_str = str(datetime.date.today())
    if today_str in analyzer.data and analyzer.data[today_str]:
        # Show most recent meals first
        for meal in reversed(analyzer.data[today_str]):
            with st.expander(f"**{meal['food']}** — {meal['calories']} kcal"):
                st.write(f"🥩 **Protein**: {meal['protein']}g | 🍚 **Carbs**: {meal['carbs']}g | 🥑 **Fat**: {meal['fat']}g")
    else:
        st.info("No meals logged today. Time to eat!")

with col2:
    st.subheader("📊 Macro Breakdown")
    
    labels = ['Protein', 'Carbs', 'Fat']
    values = [summary['protein'], summary['carbs'], summary['fat']]
    
    if sum(values) > 0:
        fig = go.Figure(data=[go.Pie(
            labels=labels, 
            values=values, 
            hole=.6, 
            marker_colors=['#ef4444', '#3b82f6', '#eab308'],
            textinfo='label+percent',
            hoverinfo='label+value+percent'
        )])
        fig.update_layout(
            margin=dict(t=20, b=20, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=False,
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Log a meal to see your macro breakdown!")

# Sidebar for Goals & Progress
st.sidebar.header("🎯 Daily Goals")

def draw_progress(label, current, goal):
    st.sidebar.write(f"**{label}**: {current:.0f} / {goal}")
    progress = min(current / goal, 1.0) if goal > 0 else 0.0
    st.sidebar.progress(progress)

draw_progress("🔥 Calories (kcal)", summary['calories'], GOAL_CALORIES)
st.sidebar.markdown("<br>", unsafe_allow_html=True)
draw_progress("🥩 Protein (g)", summary['protein'], GOAL_PROTEIN)
st.sidebar.markdown("<br>", unsafe_allow_html=True)
draw_progress("🍚 Carbs (g)", summary['carbs'], GOAL_CARBS)
st.sidebar.markdown("<br>", unsafe_allow_html=True)
draw_progress("🥑 Fat (g)", summary['fat'], GOAL_FAT)

st.sidebar.markdown("---")
st.sidebar.caption("Data is saved locally in `nutrition_data.json`.")
