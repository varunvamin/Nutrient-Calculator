import streamlit as st
from nutrients import NutritionalAnalyzer
import datetime

st.set_page_config(page_title="Nutrient Calculator", page_icon="🍎", layout="centered")

# Initialize analyzer (Streamlit re-runs script on interaction, so we use session state or standard initialization)
# Since NutritionalAnalyzer reads/writes to a file, we can just instantiate it normally.
analyzer = NutritionalAnalyzer()

st.title("🍎 Nutrient Calculator")
st.markdown("Track your daily nutritional intake easily with this interactive web dashboard!")

# Sidebar for daily summary
st.sidebar.header("📊 Daily Summary")
summary = analyzer.get_daily_summary()
st.sidebar.metric(label="Total Calories", value=f"{summary['calories']} kcal")
st.sidebar.metric(label="Total Protein", value=f"{summary['protein']} g")
st.sidebar.metric(label="Total Carbs", value=f"{summary['carbs']} g")
st.sidebar.metric(label="Total Fat", value=f"{summary['fat']} g")

st.header("Add a Meal")
with st.form("add_meal_form"):
    food_name = st.text_input("Food Name", placeholder="e.g., Grilled Chicken")
    
    col1, col2 = st.columns(2)
    with col1:
        calories = st.number_input("Calories (kcal)", min_value=0.0, step=1.0)
        protein = st.number_input("Protein (g)", min_value=0.0, step=0.1)
    with col2:
        carbs = st.number_input("Carbs (g)", min_value=0.0, step=0.1)
        fat = st.number_input("Fat (g)", min_value=0.0, step=0.1)
        
    submit_button = st.form_submit_button(label="Add Meal")

if submit_button:
    if food_name.strip():
        analyzer.add_meal(food_name, calories, protein, carbs, fat)
        st.success(f"Added '{food_name}' successfully!")
        st.rerun()
    else:
        st.error("Please enter a food name.")

# Display today's meals
st.header("Today's Meals")
today_str = str(datetime.date.today())
if today_str in analyzer.data and analyzer.data[today_str]:
    meals = analyzer.data[today_str]
    for meal in meals:
        with st.expander(f"{meal['food']} ({meal['calories']} kcal)"):
            st.write(f"**Protein**: {meal['protein']} g")
            st.write(f"**Carbs**: {meal['carbs']} g")
            st.write(f"**Fat**: {meal['fat']} g")
else:
    st.info("No meals added today yet.")
