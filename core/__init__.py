"""
Core Systems Package
Master Launcher Ultimate - Commander Bobby Don McWilliams II

Core functionality including GS343, Phoenix, diagnostics, and management systems.
"""

__version__ = "1.0.0"
__author__ = "Commander Bobby Don McWilliams II"
__authority_level__ = "11.0"

from .gs343_foundation import GS343Foundation
from .phoenix_healer import PhoenixHealer
from .process_naming import ProcessNamingManager
from .backup_manager import BackupManager
from .quarantine_manager import QuarantineManager
from .diagnostic_system import DiagnosticSystem
from .crystal_memory import CrystalMemoryIntegration
from .token_efficiency import TokenEfficiency
from .load_balancer import LoadBalancer
from .predictive_analytics import PredictiveAnalytics
from .auto_documentation import AutoDocumentation
from .performance_optimizer import PerformanceOptimizer

__all__ = [
    'GS343Foundation',
    'PhoenixHealer',
    'ProcessNamingManager',
    'BackupManager',
    'QuarantineManager',
    'DiagnosticSystem',
    'CrystalMemoryIntegration',
    'TokenEfficiency',
    'LoadBalancer',
    'PredictiveAnalytics',
    'AutoDocumentation',
    'PerformanceOptimizer'
]
