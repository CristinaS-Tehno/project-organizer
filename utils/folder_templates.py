"""
Folder template generator
"""
from pathlib import Path


class FolderTemplate:
    """Generates folder structures based on templates"""

    TEMPLATES = {
        "Basic": {
            "folders": ["Documents", "Assets", "Notes"]
        },
        "Development": {
            "folders": ["src", "docs", "tests", "assets", "config", "output"]
        },
        "Design": {
            "folders": ["Designs", "Assets", "References", "Exports", "Feedback"]
        },
        "Research": {
            "folders": ["Resources", "Data", "Analysis", "Findings", "References"]
        }
    }

    @staticmethod
    def create_folder_structure(base_path, template_name):
        """
        Create folder structure based on template
        
        Args:
            base_path: Root path for the project
            template_name: Name of the template to use
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            base_path = Path(base_path)
            base_path.mkdir(parents=True, exist_ok=True)
            
            if template_name not in FolderTemplate.TEMPLATES:
                template_name = "Basic"
            
            template = FolderTemplate.TEMPLATES[template_name]
            
            for folder in template["folders"]:
                folder_path = base_path / folder
                folder_path.mkdir(parents=True, exist_ok=True)
            
            return True
        except Exception as e:
            print(f"Error creating folder structure: {e}")
            return False

    @staticmethod
    def get_available_templates():
        """Get list of available templates"""
        return list(FolderTemplate.TEMPLATES.keys())
