"""
Folder template generator
"""
from pathlib import Path
import shutil


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
    def copy_folder_contents(source_path, destination_path):
        """
        Copy all contents from source folder to destination folder
        
        Args:
            source_path: Path to source folder to copy from
            destination_path: Path to destination folder
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            source_path = Path(source_path)
            destination_path = Path(destination_path)
            
            if not source_path.exists():
                raise Exception(f"Source folder does not exist: {source_path}")
            
            if not source_path.is_dir():
                raise Exception(f"Source path is not a directory: {source_path}")
            
            # Create destination if it doesn't exist
            destination_path.mkdir(parents=True, exist_ok=True)
            
            # Copy all contents
            for item in source_path.iterdir():
                dest_item = destination_path / item.name
                if item.is_dir():
                    shutil.copytree(item, dest_item, dirs_exist_ok=True)
                else:
                    shutil.copy2(item, dest_item)
            
            print(f"✅ Copied contents from {source_path} to {destination_path}")
            return True
        except Exception as e:
            print(f"Error copying folder contents: {e}")
            return False

    @staticmethod
    def get_available_templates():
        """Get list of available templates"""
        return list(FolderTemplate.TEMPLATES.keys())
