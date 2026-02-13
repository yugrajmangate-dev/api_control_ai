"""
Simulation module for running epidemic simulations
Contains metrics tracking and simulation execution
"""
from .metrics import init_metrics, record_metrics
try:
    from .run import run_simulation
except ImportError:
    run_simulation = None
__all__ = [
    'init_metrics',
    'record_metrics',
    'run_simulation'
]
