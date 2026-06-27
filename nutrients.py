import json
import os
from datetime import date

class NutritionalAnalyzer:
    def __init__(self, data_file='nutrition_data.json'):
        self.data_file = data_file
        self.data = self._load_data()

    def _load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def add_meal(self, food_name, calories, protein, carbs, fat):
        today = str(date.today())
        if today not in self.data:
            self.data[today] = []
            
        meal = {
            'food': food_name,
            'calories': calories,
            'protein': protein,
            'carbs': carbs,
            'fat': fat
        }
        self.data[today].append(meal)
        self._save_data()

    def get_daily_summary(self, date_str=None):
        if date_str is None:
            date_str = str(date.today())
            
        summary = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
        
        if date_str in self.data:
            for meal in self.data[date_str]:
                summary['calories'] += meal.get('calories', 0)
                summary['protein'] += meal.get('protein', 0)
                summary['carbs'] += meal.get('carbs', 0)
                summary['fat'] += meal.get('fat', 0)
                
        return summary
