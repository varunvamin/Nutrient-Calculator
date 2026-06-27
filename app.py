import streamlit as st
import plotly.graph_objects as go
import requests
from nutrients import NutritionalAnalyzer
import datetime

st.set_page_config(page_title="Health Buddy", page_icon="☁️", layout="wide")

# Custom CSS for Soft Pastel UI (matching reference image)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
    }
    
    /* Main Background - Soft Pastel Gradient */
    .stApp {
        background: linear-gradient(135deg, #fff1f2 0%, #fdf4ff 50%, #f0fdf4 100%);
        color: #1f2937;
    }
    
    /* Sidebar Glassmorphism */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.4) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.5);
    }
    
    /* Headers & Text */
    h1, h2, h3, h4, h5, h6, p, label {
        color: #374151 !important;
        font-weight: 700;
    }
    
    /* Input fields */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #ffffff;
        color: #1f2937;
        border: 1px solid #fce7f3;
        border-radius: 16px;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);
    }
    
    /* Pill-shaped Gradient Button */
    .stButton>button {
        background: linear-gradient(90deg, #ffcba4 0%, #ffb38a 100%);
        color: #431407 !important;
        border: none;
        border-radius: 30px;
        padding: 12px 24px;
        font-weight: 800;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 8px 20px rgba(255, 179, 138, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 25px rgba(255, 179, 138, 0.6);
        color: #431407 !important;
        border: none;
    }
    
    /* Expander cards */
    .streamlit-expanderHeader {
        background-color: #ffffff;
        border-radius: 16px;
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
    }
    div[data-testid="stExpanderDetails"] {
        background-color: #ffffff;
        border-radius: 0 0 16px 16px;
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
    }
    
    /* Form container */
    [data-testid="stForm"] {
        background-color: rgba(255,255,255,0.6);
        border: 1px solid rgba(255,255,255,0.8);
        border-radius: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.04);
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)

analyzer = NutritionalAnalyzer()

st.title("☁️ Your happy health buddy")
st.markdown("Track habits, stay active, and celebrate small wins — with a little smile along the way.")
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
    st.subheader("🔍 Food Buddy Search")
    with st.form("api_search_form"):
        search_query = st.text_input("Ask anything... (e.g., Apple, Chicken Breast)")
        search_btn = st.form_submit_button("Fetch Macros ✨")
        
    if search_btn and search_query.strip():
        with st.spinner(f"Searching database for '{search_query}'..."):
            try:
                url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={search_query}&search_simple=1&action=process&json=1&page_size=1"
                response = requests.get(url, headers={'User-Agent': 'NutrientCalculator/1.0'})
                data = response.json()
                
                if data.get('products'):
                    product = data['products'][0]
                    name = product.get('product_name', search_query.title())
                    nutriments = product.get('nutriments', {})
                    
                    cal = float(nutriments.get('energy-kcal_100g', 0))
                    pro = float(nutriments.get('proteins_100g', 0))
                    car = float(nutriments.get('carbohydrates_100g', 0))
                    fat = float(nutriments.get('fat_100g', 0))
                    
                    analyzer.add_meal(f"{name} (100g)", cal, pro, car, fat)
                    st.success(f"Successfully logged: {name} (100g)")
                    st.rerun()
                else:
                    st.warning(f"Could not find '{search_query}'. Try manual entry.")
            except Exception as e:
                st.error("Error connecting to the food database.")

    st.subheader("🍽️ Manual Entry")
    with st.form("add_meal_form", clear_on_submit=True):
        food_name = st.text_input("Custom Food Name")
        
        c1, c2, c3, c4 = st.columns(4)
        with c1: calories = st.number_input("Calories", min_value=0.0, step=10.0)
        with c2: protein = st.number_input("Protein (g)", min_value=0.0, step=1.0)
        with c3: carbs = st.number_input("Carbs (g)", min_value=0.0, step=1.0)
        with c4: fat = st.number_input("Fat (g)", min_value=0.0, step=1.0)
            
        submit_button = st.form_submit_button(label="Log Custom Meal ➕")

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
        for meal in reversed(analyzer.data[today_str]):
            with st.expander(f"**{meal['food']}** — {meal['calories']} kcal"):
                st.write(f"🥩 **Protein**: {meal['protein']}g | 🍚 **Carbs**: {meal['carbs']}g | 🥑 **Fat**: {meal['fat']}g")
    else:
        st.info("No meals logged today. Time to eat!")

with col2:
    st.subheader("📊 Your Nutrition Analysis")
    
    labels = ['Protein', 'Carbs', 'Fat']
    values = [summary['protein'], summary['carbs'], summary['fat']]
    
    if sum(values) > 0:
        fig = go.Figure(data=[go.Pie(
            labels=labels, 
            values=values, 
            hole=.6, 
            # Pastel colors matching the image vibe: Light Blue, Light Orange, Light Pink
            marker_colors=['#93c5fd', '#fdba74', '#f9a8d4'],
            textinfo='label+percent',
            hoverinfo='label+value+percent'
        )])
        fig.update_layout(
            margin=dict(t=20, b=20, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#374151', family='Nunito'),
            showlegend=False,
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Log a meal to see your macro breakdown!")

# Sidebar for Goals & Progress
st.sidebar.title("COUNT YOUR DAILY CALORIES")
st.sidebar.markdown("<br>", unsafe_allow_html=True)

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
st.sidebar.caption("Track Trends. Spot Patterns. Crush Your Goals.")
