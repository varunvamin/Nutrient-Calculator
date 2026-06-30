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
