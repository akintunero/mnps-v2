from models import get_db, create_tables

# This file is kept simple - all database logic is in models.py
# Just re-export the functions for easy importing

__all__ = ["get_db", "create_tables"]
