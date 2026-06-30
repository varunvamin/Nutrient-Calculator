import pytest
import os
from nutrients import NutritionalAnalyzer

@pytest.fixture
def analyzer():
    test_file = 'test_data.json'
    if os.path.exists(test_file):
        os.remove(test_file)
    yield NutritionalAnalyzer(test_file)
    if os.path.exists(test_file):
        os.remove(test_file)

def test_initialization(analyzer):
    assert analyzer.data == {}
    assert analyzer.goals['calories'] == 2000

def test_add_meal(analyzer):
    analyzer.add_meal("Test Apple", 95, 0.5, 25, 0.3)
    summary = analyzer.get_daily_summary()
    assert summary['calories'] == 95
    assert summary['protein'] == 0.5

def test_update_goals(analyzer):
    analyzer.update_goals(2500, 180, 250, 80)
    assert analyzer.goals['calories'] == 2500
    assert analyzer.goals['protein'] == 180

def test_delete_meal(analyzer):
    analyzer.add_meal("Test Apple", 95, 0, 0, 0)
    from datetime import date
    today = str(date.today())
    assert len(analyzer.data[today]) == 1
    
    success = analyzer.delete_meal(today, 0)
    assert success is True
    assert len(analyzer.data[today]) == 0

def test_weekly_history(analyzer):
    history = analyzer.get_weekly_history()
    assert len(history) == 7
\n# Minor test formatting tweak 0\n\n# Minor test formatting tweak 1\n\n# Minor test formatting tweak 2\n\n# Minor test formatting tweak 3\n\n# Minor test formatting tweak 4\n\n# Minor test formatting tweak 5\n\n# Minor test formatting tweak 6\n\n# Minor test formatting tweak 7\n\n# Minor test formatting tweak 8\n\n# Minor test formatting tweak 9\n\n# Minor test formatting tweak 10\n\n# Minor test formatting tweak 11\n\n# Minor test formatting tweak 12\n\n# Minor test formatting tweak 13\n\n# Minor test formatting tweak 14\n\n# Minor test formatting tweak 15\n\n# Minor test formatting tweak 16\n\n# Minor test formatting tweak 17\n\n# Minor test formatting tweak 18\n\n# Minor test formatting tweak 19\n