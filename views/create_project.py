"""
Create Project dialog
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QTextEdit, QMessageBox, QFileDialog
)
from utils.constants import PROJECT_CATEGORIES


class CreateProjectDialog(QDialog):
    """Dialog for creating a new project"""

    def __init__(self, parent, project_manager):
        """
        Initialize create project dialog
        
        Args:
            parent: Parent window
            project_manager: ProjectManager instance
        """
        super().__init__(parent)
        self.project_manager = project_manager
        self.selected_source_folder = None
        self.init_ui()

    def init_ui(self):
        """Initialize dialog UI"""
        self.setWindowTitle("Create New Project")
        self.setGeometry(200, 200, 600, 500)
        self.setModal(True)

        layout = QVBoxLayout()

        # Project Name
        name_label = QLabel("Project Name:")
        layout.addWidget(name_label)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter project name...")
        layout.addWidget(self.name_input)

        # Description
        desc_label = QLabel("Description:")
        layout.addWidget(desc_label)
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Enter project description (optional)...")
        self.description_input.setMaximumHeight(80)
        layout.addWidget(self.description_input)

        # Category
        category_label = QLabel("Category:")
        layout.addWidget(category_label)
        self.category_combo = QComboBox()
        self.category_combo.addItems(PROJECT_CATEGORIES)
        layout.addWidget(self.category_combo)

        # Template
        template_label = QLabel("Folder Template:")
        layout.addWidget(template_label)
        self.template_combo = QComboBox()
        templates = self.project_manager.get_available_templates()
        self.template_combo.addItems(templates)
        layout.addWidget(self.template_combo)

        # Source Folder
        folder_label = QLabel("Copy from Folder (Optional):")
        layout.addWidget(folder_label)
        
        folder_layout = QHBoxLayout()
        self.folder_input = QLineEdit()
        self.folder_input.setPlaceholderText("Select a folder to copy from...")
        self.folder_input.setReadOnly(True)
        folder_layout.addWidget(self.folder_input)
        
        browse_btn = QPushButton("📁 Browse")
        browse_btn.clicked.connect(self.browse_folder)
        folder_layout.addWidget(browse_btn)
        
        layout.addLayout(folder_layout)

        # Buttons
        button_layout = QHBoxLayout()

        create_btn = QPushButton("✓ Create")
        create_btn.clicked.connect(self.create_project)
        button_layout.addWidget(create_btn)

        cancel_btn = QPushButton("✗ Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def browse_folder(self):
        """Open folder browser dialog"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Folder to Copy From",
            ""
        )
        if folder:
            self.selected_source_folder = folder
            self.folder_input.setText(folder)

    def create_project(self):
        """Create the project"""
        name = self.name_input.text().strip()
        description = self.description_input.toPlainText().strip()
        category = self.category_combo.currentText()
        template = self.template_combo.currentText()
        source_folder = self.selected_source_folder

        # Validation
        if not name:
            QMessageBox.warning(self, "Validation Error", "Please enter a project name")
            return

        try:
            self.project_manager.create_new_project(
                name=name,
                description=description,
                category=category,
                template=template,
                source_folder=source_folder
            )
            
            message = f"Project '{name}' created successfully!"
            if source_folder:
                message += f"\n\nFolder contents copied from:\n{source_folder}"
            
            QMessageBox.information(self, "Success", message)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create project: {str(e)}")
