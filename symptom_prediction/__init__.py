"""
Symptom Prediction Module
Predicts likely symptom patterns for emerging viruses based on historical pandemic data
"""

from .predictor import SymptomPredictor
from .historical_data import HISTORICAL_PANDEMICS

__all__ = ['SymptomPredictor', 'HISTORICAL_PANDEMICS']
