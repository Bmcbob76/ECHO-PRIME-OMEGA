"""
DROIDS PACKAGE
R2D2/C3PO Obscenity Interaction System
Commander Bobby Don McWilliams II - Authority 11.0
"""

from .r2d2_obscenity_engine import R2D2ObscenityEngine
from .c3po_voice_engine import C3POVoiceEngine
from .droid_interaction_system import DroidInteractionSystem, DROID_CONTEXT_MAP

__all__ = [
    'R2D2ObscenityEngine',
    'C3POVoiceEngine', 
    'DroidInteractionSystem',
    'DROID_CONTEXT_MAP'
]
