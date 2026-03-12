import sys
import os

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../db-schemas'))

from database import get_db

__all__ = ['get_db']
