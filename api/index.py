"""
Vercel Serverless Entrypoint for FastAPI Application
"""

import sys
import os

# Add root folder to sys.path so modules like backend and model are resolved
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import app
