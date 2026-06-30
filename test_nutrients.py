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
