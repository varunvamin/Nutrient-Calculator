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
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('meals', data) if isinstance(data, dict) else {}
            except json.JSONDecodeError:
                return {}
        return {}

    def _load_goals(self) -> Dict[str, float]:
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
