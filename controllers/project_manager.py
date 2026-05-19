"""
Project Manager - Business logic layer
"""
from pathlib import Path
from models.database import Database
from models.project import Project
from utils.folder_templates import FolderTemplate
from utils.config import PROJECTS_ROOT_PATH
from datetime import datetime


class ProjectManager:
    """Manages all project operations"""

    def __init__(self):
        """Initialize project manager"""
        self.db = Database()
        self.projects_root = PROJECTS_ROOT_PATH

    def create_new_project(self, name, description, category, template, source_folder=None):
        """
        Create a new project
        
        Args:
            name: Project name
            description: Project description
            category: Project category
            template: Folder template to use
            source_folder: Optional path to folder to copy from
            
        Returns:
            Project: Created project object or None
        """
        try:
            # Create folder structure
            project_path = self.projects_root / name
            
            if project_path.exists():
                raise Exception(f"Project folder already exists: {project_path}")
            
            # Create folders based on template
            if template and template != "None":
                if not FolderTemplate.create_folder_structure(project_path, template):
                    raise Exception("Failed to create folder structure")
            else:
                # Just create the main folder
                project_path.mkdir(parents=True, exist_ok=True)
            
            # Copy folder contents if source folder provided
            if source_folder and source_folder.strip():
                source_path = Path(source_folder)
                if not FolderTemplate.copy_folder_contents(source_path, project_path):
                    raise Exception("Failed to copy folder contents")
            
            # Save to database
            project_id = self.db.create_project(
                name=name,
                description=description,
                category=category,
                path=str(project_path),
                template=template or "Custom"
            )
            
            if project_id is None:
                raise Exception("Failed to save project to database")
            
            project = Project(
                project_id=project_id,
                name=name,
                description=description,
                category=category,
                path=str(project_path),
                template=template or "Custom",
                status='active',
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            return project
        except Exception as e:
            print(f"Error creating project: {e}")
            raise

    def get_all_projects(self):
        """Get all active projects"""
        try:
            rows = self.db.get_all_projects()
            projects = []
            for row in rows:
                project = Project(
                    project_id=row[0],
                    name=row[1],
                    description=row[2],
                    category=row[3],
                    path=row[4],
                    template=row[5],
                    status=row[6],
                    created_at=row[7],
                    updated_at=row[8]
                )
                projects.append(project)
            return projects
        except Exception as e:
            print(f"Error retrieving projects: {e}")
            return []

    def search_projects(self, search_term):
        """Search projects by name or description"""
        try:
            rows = self.db.search_projects(search_term)
            projects = []
            for row in rows:
                project = Project(
                    project_id=row[0],
                    name=row[1],
                    description=row[2],
                    category=row[3],
                    path=row[4],
                    template=row[5],
                    status=row[6],
                    created_at=row[7],
                    updated_at=row[8]
                )
                projects.append(project)
            return projects
        except Exception as e:
            print(f"Error searching projects: {e}")
            return []

    def get_projects_by_category(self, category):
        """Get projects filtered by category"""
        try:
            rows = self.db.get_projects_by_category(category)
            projects = []
            for row in rows:
                project = Project(
                    project_id=row[0],
                    name=row[1],
                    description=row[2],
                    category=row[3],
                    path=row[4],
                    template=row[5],
                    status=row[6],
                    created_at=row[7],
                    updated_at=row[8]
                )
                projects.append(project)
            return projects
        except Exception as e:
            print(f"Error retrieving projects by category: {e}")
            return []

    def open_project_folder(self, project_path):
        """Open project folder in file explorer"""
        try:
            import subprocess
            import platform
            
            path = Path(project_path)
            if not path.exists():
                raise Exception(f"Project folder not found: {project_path}")
            
            if platform.system() == 'Windows':
                subprocess.Popen(['explorer', str(path)])
            elif platform.system() == 'Darwin':
                subprocess.Popen(['open', str(path)])
            else:
                subprocess.Popen(['xdg-open', str(path)])
            
            return True
        except Exception as e:
            print(f"Error opening project folder: {e}")
            return False

    def delete_project(self, project_id):
        """Archive a project"""
        return self.db.delete_project(project_id)

    def get_available_templates(self):
        """Get list of available templates"""
        templates = FolderTemplate.get_available_templates()
        templates.append("None")  # Option for no template
        return templates

    def close(self):
        """Close database connection"""
        self.db.close()
