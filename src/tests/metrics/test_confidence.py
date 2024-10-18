import pandas as pd
from metrics.llm.confidence import (
    _samples_in_bin,
    _accuracy_in_bin,
    _confidence_in_bin,
    _compute_ece_from_data
)


def test_samples_in_bin(confidence_data):
    confidence_data = pd.DataFrame(confidence_data)
    result = _samples_in_bin(confidence_data, 0.8, 1.0)
    expected = 3
    assert len(result) == expected


def test_accuracy_in_bin_5(confidence_data):
    confidence_data = pd.DataFrame(confidence_data)
    result = _accuracy_in_bin(confidence_data, 0.8, 1.0)
    expected = 2/3
    assert result == expected


def test_accuracy_in_bin_4(confidence_data):
    confidence_data = pd.DataFrame(confidence_data)
    result = _accuracy_in_bin(confidence_data, 0.6, 0.8)
    expected = 3/4
    assert result == expected


def test_accuracy_in_bin_3(confidence_data):
    confidence_data = pd.DataFrame(confidence_data)
    result = _accuracy_in_bin(confidence_data, 0.4, 0.6)
    expected = 1/2
    assert result == expected


def test_confidence_in_bin_5(confidence_data):
    confidence_data = pd.DataFrame(confidence_data)
    result = _confidence_in_bin(confidence_data, 0.8, 1.0)
    expected = 0.8667
    assert round(result, 4) == expected


def test_confidence_in_bin_4(confidence_data):
    confidence_data = pd.DataFrame(confidence_data)
    result = _confidence_in_bin(confidence_data, 0.6, 0.8)
    expected = 0.6875
    assert round(result, 4) == expected


def test_confidence_in_bin_3(confidence_data):
    confidence_data = pd.DataFrame(confidence_data)
    result = _confidence_in_bin(confidence_data, 0.4, 0.6)
    expected = 0.545
    assert round(result, 3) == expected


def test_compute_ece(confidence_data):
    confidence_data = pd.DataFrame(confidence_data)
    result = _compute_ece_from_data(confidence_data, 5)
    expected = 0.1044
    assert round(result, 4) == expected
