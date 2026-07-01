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

tabs = st.tabs(["🍽️ Log Meals", "📈 Trends & History"])

with tabs[0]:
    col1, col2 = st.columns([1.5, 1], gap="large")
    
    with col1:
        st.subheader("🔍 Food Buddy Search")
        with st.form("api_search_form"):
            search_query = st.text_input("Ask anything... (e.g., Apple)")
            if st.form_submit_button("Fetch Macros ✨") and search_query.strip():
                try:
                    url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={search_query}&search_simple=1&action=process&json=1&page_size=1"
                    data = requests.get(url, headers={'User-Agent': 'NutrientCalculator/1.0'}).json()
                    if data.get('products'):
                        p = data['products'][0]
                        n = p.get('nutriments', {})
                        analyzer.add_meal(f"{p.get('product_name', search_query)} (100g)", 
                                          float(n.get('energy-kcal_100g', 0)), float(n.get('proteins_100g', 0)), 
                                          float(n.get('carbohydrates_100g', 0)), float(n.get('fat_100g', 0)))
                        st.rerun()
                    else:
                        st.warning("Not found.")
                except Exception:
                    st.error("API Error.")

        st.subheader("🍽️ Manual Entry")
        with st.form("manual_entry"):
            food_name = st.text_input("Food Name")
            c1, c2, c3, c4 = st.columns(4)
            with c1: cal = st.number_input("Kcal", min_value=0.0)
            with c2: pro = st.number_input("Pro(g)", min_value=0.0)
            with c3: car = st.number_input("Car(g)", min_value=0.0)
            with c4: fat = st.number_input("Fat(g)", min_value=0.0)
            if st.form_submit_button("Log Custom Meal ➕") and food_name.strip():
                analyzer.add_meal(food_name, cal, pro, car, fat)
                st.rerun()

    with col2:
        st.subheader("📊 Today's Macros")
        values = [summary['protein'], summary['carbs'], summary['fat']]
        if sum(values) > 0:
            fig = go.Figure(data=[go.Pie(labels=['Protein', 'Carbs', 'Fat'], values=values, hole=.6, 
                                         marker_colors=['#93c5fd', '#fdba74', '#f9a8d4'])])
            fig.update_layout(
                margin=dict(t=0, b=0, l=0, r=0), 
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#1a1a1a', family='Inter')
            )
            st.plotly_chart(fig, use_container_width=True)
            
        st.subheader("📅 Today's Log")
        today_str = str(datetime.date.today())
        if today_str in analyzer.data and analyzer.data[today_str]:
            for i, meal in enumerate(analyzer.data[today_str]):
                col_name, col_del = st.columns([4, 1])
                with col_name:
                    with st.expander(f"{meal['food']} - {meal['calories']} kcal"):
                        st.write(f"Pro: {meal['protein']}g | Car: {meal['carbs']}g | Fat: {meal['fat']}g")
                with col_del:
                    if st.button("❌", key=f"del_{i}"):
                        analyzer.delete_meal(today_str, i)
                        st.rerun()

with tabs[1]:
    st.subheader("📈 7-Day Trend Analysis")
    history = analyzer.get_weekly_history()
    dates = list(history.keys())
    cals = [d['calories'] for d in history.values()]
    
    fig_bar = px.bar(x=dates, y=cals, labels={'x':'Date', 'y':'Calories'}, title="Calorie Intake (Last 7 Days)")
    fig_bar.update_traces(marker_color='#fdba74')
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#1a1a1a', family='Inter'),
        xaxis=dict(showgrid=False, color='#1a1a1a'),
        yaxis=dict(showgrid=True, gridcolor='#e0e0e0', color='#1a1a1a')
    )
    st.plotly_chart(fig_bar, use_container_width=True)
