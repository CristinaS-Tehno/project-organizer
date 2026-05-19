"""
Project data model
"""
from datetime import datetime


class Project:
    """Represents a project"""

    def __init__(self, project_id, name, description, category, path, template, 
                 status='active', created_at=None, updated_at=None):
        """
        Initialize a project
        
        Args:
            project_id: Unique project identifier
            name: Project name
            description: Project description
            category: Project category
            path: File system path to project folder
            template: Folder template used
            status: Project status (active, archived)
            created_at: Creation timestamp
            updated_at: Last update timestamp
        """
        self.project_id = project_id
        self.name = name
        self.description = description
        self.category = category
        self.path = path
        self.template = template
        self.status = status
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self):
        """Convert project to dictionary"""
        return {
            'project_id': self.project_id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'path': self.path,
            'template': self.template,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return f"<Project: {self.name} ({self.category})>"
