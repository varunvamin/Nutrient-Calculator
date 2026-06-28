# 🥗 Nutrient Calculator - Web App

<p align="left">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
</p>

🚀 **Live App**: [https://nutrient-calculator.streamlit.app/](https://nutrient-calculator.streamlit.app/)

A modern, interactive Python-based web application designed to calculate and track daily nutritional intake. Built with Streamlit for a seamless user experience.

## ✨ Premium Features
- **REST API Integration**: Connects to the OpenFoodFacts database via `requests` to automatically fetch and log real-time nutritional data for searched foods.
- **Data Visualization**: Integrated Plotly to render interactive, real-time donut charts of daily macronutrient breakdowns.
- **Premium UI/UX**: Designed with custom CSS for a modern dark-mode aesthetic, glassmorphism elements, and sleek typography.
- **Goal Tracking**: Set and track daily macro goals (Calories, Protein, Carbs, Fat) with visual progress bars updating in real-time.
- **Data Persistence**: Saves meal data locally in JSON, organizing it seamlessly by date.

## 🛠️ Local Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/varunvamin/Nutrient-Calculator.git
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit web app:
   ```bash
   streamlit run app.py
   ```
4. Open the link provided in the terminal (usually `http://localhost:8501`) in your browser.

## 📱 Usage
- Enter the name of the food you consumed.
- Input the exact macronutrients (calories, protein, carbs, fat).
- Click **Add Meal** to save it.
- View your total daily consumption in the sidebar to track your goals!

## 📝 License
This project is open-source and available under the [MIT License](LICENSE).