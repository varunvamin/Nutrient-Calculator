import json
import os
from datetime import date
from typing import Dict, List, Optional, Any

class NutritionalAnalyzer:
    def __init__(self, data_file: str = 'nutrition_data.json'):
        self.data_file = data_file
        self.data = self._load_data()
        self.goals = self._load_goals()

    def _load_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """Loads meal history from the JSON data file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('meals', data) if isinstance(data, dict) else {}
            except json.JSONDecodeError:
                return {}
        return {}

    def _load_goals(self) -> Dict[str, float]:
        """Loads daily nutritional goals from the JSON data file or sets defaults."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict) and 'goals' in data:
                        return data['goals']
            except json.JSONDecodeError:
                pass
        return {'calories': 2000, 'protein': 150, 'carbs': 200, 'fat': 70}

    def _save_data(self) -> None:
        save_payload = {'meals': self.data, 'goals': self.goals}
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(save_payload, f, indent=4)

    def update_goals(self, calories: float, protein: float, carbs: float, fat: float) -> None:
        self.goals = {'calories': calories, 'protein': protein, 'carbs': carbs, 'fat': fat}
        self._save_data()

    def add_meal(self, food_name: str, calories: float, protein: float, carbs: float, fat: float) -> None:
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

    def delete_meal(self, date_str: str, index: int) -> bool:
        if date_str in self.data and 0 <= index < len(self.data[date_str]):
            self.data[date_str].pop(index)
            self._save_data()
            return True
        return False

    def get_daily_summary(self, date_str: Optional[str] = None) -> Dict[str, float]:
        if date_str is None:
            date_str = str(date.today())
            
        summary = {'calories': 0.0, 'protein': 0.0, 'carbs': 0.0, 'fat': 0.0}
        
        if date_str in self.data:
            for meal in self.data[date_str]:
                summary['calories'] += meal.get('calories', 0)
                summary['protein'] += meal.get('protein', 0)
                summary['carbs'] += meal.get('carbs', 0)
                summary['fat'] += meal.get('fat', 0)
                
        return summary

    def get_weekly_history(self) -> Dict[str, Dict[str, float]]:
        import datetime
        history = {}
        today = datetime.date.today()
        for i in range(6, -1, -1):
            d = today - datetime.timedelta(days=i)
            history[str(d)] = self.get_daily_summary(str(d))
        return history
