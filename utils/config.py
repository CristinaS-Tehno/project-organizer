"""
Application configuration
"""
from pathlib import Path

# Database configuration
DATABASE_CONNECTION_STRING = (
    'Driver={ODBC Driver 17 for SQL Server};'
    'Server=localhost;'
    'Database=ProjectOrganizer;'
    'Trusted_Connection=yes;'
)

# Folder configuration
PROJECTS_ROOT_PATH = Path.home() / "Documents" / "Projects"

# Ensure projects root exists
PROJECTS_ROOT_PATH.mkdir(parents=True, exist_ok=True)

# UI Configuration
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
WINDOW_TITLE = "Project Organizer - Manage Your Projects"
