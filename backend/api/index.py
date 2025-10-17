"""
Vercel Serverless Function Entry Point
"""
import sys
import os

# Add the backend directory to the Python path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

from app.main import app

# Export the FastAPI app for Vercel
handler = app
