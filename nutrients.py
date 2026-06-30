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
