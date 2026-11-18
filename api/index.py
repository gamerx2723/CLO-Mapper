"""
Vercel Serverless Entrypoint for FastAPI Application
"""

import sys
import os

api_dir = os.path.dirname(os.path.abspath(__file__))
if api_dir not in sys.path:
    sys.path.insert(0, api_dir)

root_dir = os.path.dirname(api_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from backend.app import app
