import os

from pathlib import Path
import sys

# GS343 Foundation Integration - MANDATORY
GS343_PATH = Path("E:/GS343/FOUNDATION")
sys.path.insert(0, str(GS343_PATH))

try:
    from gs343_foundation_core import GS343UniversalFoundation
    from phoenix_auto_heal import PhoenixAutoHeal
    GS343_AVAILABLE = True
except ImportError:
    GS343_AVAILABLE = False
    print("?? WARNING: GS343 Foundation not loaded - Limited functionality")
class Plugin:
    def __init__(self, path):
        self.path = path

    def is_docker(self):
        return os.path.exists(os.path.join(self.path, 'Dockerfile'))

    def is_python_script(self):
        return self.path.endswith('.py')

    def is_executable(self):
        return os.access(self.path, os.X_OK)
