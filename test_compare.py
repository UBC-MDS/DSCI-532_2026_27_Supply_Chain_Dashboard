import sys
from pathlib import Path
import pytest
from compare import compare


def test_compare_significant_improvement():
    """
    Verifies that a 25% cost reduction is classified correctly
    """
    result = compare(current=75, baseline=100, higher_is_better=False)
    assert result["label"] == "significantly below avg"
    assert result["theme"] == "success"


def test_compare_stable_threshold():
    """
    Verifies the threshold for 'stable' vs 'slightly above'
    """
    result = compare(current=100.5, baseline=100, higher_is_better=True)
    assert result["label"] == "stable"
    assert result["theme"] == "secondary"


def test_compare_danger_drop():
    """
    Verifies that a significant drop includes the ' avg' suffix
    """
    result = compare(current=70, baseline=85, higher_is_better=True)
    assert result["label"] == "significantly below avg"
    assert result["theme"] == "danger"
