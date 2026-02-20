"""
Database initialization script
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.database.connection import init_db

if __name__ == "__main__":
    print("🚀 Initializing FinSight AI database...")
    init_db()
    print("✅ Database setup complete!")
