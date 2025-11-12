# L9_EKM module
# MANDATORY GS343 FOUNDATION
import sys
sys.path.append("P:/ECHO_PRIME/MLS_CLEAN/PRODUCTION/GATEWAYS/GS343")
from comprehensive_error_database_ekm_integrated import ComprehensiveProgrammingErrorDatabase

# MANDATORY PHOENIX
sys.path.append("P:/ECHO_PRIME/MLS_CLEAN/PRODUCTION/GATEWAYS/GS343/HEALERS")
from phoenix_client_gs343 import PhoenixClient, auto_heal

from .ekm_manager import EKMManager
from .ekm_trainer import EKMTrainer

__all__ = ['EKMManager', 'EKMTrainer']
