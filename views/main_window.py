"""
Main application window
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QComboBox, QLabel,
    QMessageBox, QHeaderView
)
from PyQt6.QtCore import Qt
from controllers.project_manager import ProjectManager
from utils.constants import APP_NAME, APP_VERSION, PROJECT_CATEGORIES
from utils.config import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE
from views.create_project import CreateProjectDialog
from pathlib import Path


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        """Initialize main window"""
        super().__init__()
        self.project_manager = ProjectManager()
        self.init_ui()
        self.load_projects()

    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)

        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Main layout
        main_layout = QVBoxLayout(main_widget)

        # Top toolbar
        toolbar_layout = QHBoxLayout()

        # Search bar
        search_label = QLabel("Search:")
        toolbar_layout.addWidget(search_label)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by project name...")
        self.search_input.textChanged.connect(self.search_projects)
        toolbar_layout.addWidget(self.search_input)

        # Category filter
        category_label = QLabel("Category:")
        toolbar_layout.addWidget(category_label)
        self.category_combo = QComboBox()
        self.category_combo.addItem("All")
        self.category_combo.addItems(PROJECT_CATEGORIES)
        self.category_combo.currentTextChanged.connect(self.filter_by_category)
        toolbar_layout.addWidget(self.category_combo)

        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.load_projects)
        toolbar_layout.addWidget(refresh_btn)

        main_layout.addLayout(toolbar_layout)

        # Projects table
        self.projects_table = QTableWidget()
        self.projects_table.setColumnCount(6)
        self.projects_table.setHorizontalHeaderLabels(
            ["Project Name", "Description", "Category", "Template", "Created", "Status"]
        )
        self.projects_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        main_layout.addWidget(self.projects_table)

        # Bottom buttons
        button_layout = QHBoxLayout()

        create_btn = QPushButton("➕ New Project")
        create_btn.clicked.connect(self.create_new_project)
        button_layout.addWidget(create_btn)

        open_btn = QPushButton("📁 Open Folder")
        open_btn.clicked.connect(self.open_selected_project)
        button_layout.addWidget(open_btn)

        delete_btn = QPushButton("🗑️ Archive")
        delete_btn.clicked.connect(self.archive_project)
        button_layout.addWidget(delete_btn)

        main_layout.addLayout(button_layout)

        # Status bar
        self.statusBar().showMessage(f"{APP_NAME} v{APP_VERSION}")

    def load_projects(self):
        """Load all projects into the table"""
        try:
            projects = self.project_manager.get_all_projects()
            self.projects_table.setRowCount(len(projects))

            for row, project in enumerate(projects):
                self.projects_table.setItem(row, 0, QTableWidgetItem(project.name))
                self.projects_table.setItem(row, 1, QTableWidgetItem(project.description or ""))
                self.projects_table.setItem(row, 2, QTableWidgetItem(project.category or ""))
                self.projects_table.setItem(row, 3, QTableWidgetItem(project.template or ""))
                self.projects_table.setItem(row, 4, QTableWidgetItem(str(project.created_at)[:10]))
                self.projects_table.setItem(row, 5, QTableWidgetItem(project.status))

            self.statusBar().showMessage(f"Loaded {len(projects)} projects")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load projects: {str(e)}")

    def create_new_project(self):
        """Open create project dialog"""
        dialog = CreateProjectDialog(self, self.project_manager)
        if dialog.exec():
            self.load_projects()

    def search_projects(self):
        """Search projects by name"""
        search_term = self.search_input.text().strip()
        if not search_term:
            self.load_projects()
            return

        try:
            projects = self.project_manager.search_projects(search_term)
            self.projects_table.setRowCount(len(projects))

            for row, project in enumerate(projects):
                self.projects_table.setItem(row, 0, QTableWidgetItem(project.name))
                self.projects_table.setItem(row, 1, QTableWidgetItem(project.description or ""))
                self.projects_table.setItem(row, 2, QTableWidgetItem(project.category or ""))
                self.projects_table.setItem(row, 3, QTableWidgetItem(project.template or ""))
                self.projects_table.setItem(row, 4, QTableWidgetItem(str(project.created_at)[:10]))
                self.projects_table.setItem(row, 5, QTableWidgetItem(project.status))

            self.statusBar().showMessage(f"Found {len(projects)} projects")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Search failed: {str(e)}")

    def filter_by_category(self):
        """Filter projects by category"""
        category = self.category_combo.currentText()
        if category == "All":
            self.load_projects()
            return

        try:
            projects = self.project_manager.get_projects_by_category(category)
            self.projects_table.setRowCount(len(projects))

            for row, project in enumerate(projects):
                self.projects_table.setItem(row, 0, QTableWidgetItem(project.name))
                self.projects_table.setItem(row, 1, QTableWidgetItem(project.description or ""))
                self.projects_table.setItem(row, 2, QTableWidgetItem(project.category or ""))
                self.projects_table.setItem(row, 3, QTableWidgetItem(project.template or ""))
                self.projects_table.setItem(row, 4, QTableWidgetItem(str(project.created_at)[:10]))
                self.projects_table.setItem(row, 5, QTableWidgetItem(project.status))

            self.statusBar().showMessage(f"Found {len(projects)} projects in {category}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Filter failed: {str(e)}")

    def open_selected_project(self):
        """Open selected project folder"""
        current_row = self.projects_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a project first")
            return

        # Get project path from the first column
        projects = self.project_manager.get_all_projects()
        if current_row < len(projects):
            project = projects[current_row]
            if self.project_manager.open_project_folder(project.path):
                self.statusBar().showMessage(f"Opened: {project.name}")
            else:
                QMessageBox.warning(self, "Error", f"Could not open folder: {project.path}")

    def archive_project(self):
        """Archive selected project"""
        current_row = self.projects_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a project first")
            return

        projects = self.project_manager.get_all_projects()
        if current_row < len(projects):
            project = projects[current_row]
            reply = QMessageBox.question(
                self, "Confirm",
                f"Archive project '{project.name}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                if self.project_manager.delete_project(project.project_id):
                    QMessageBox.information(self, "Success", f"Project '{project.name}' archived")
                    self.load_projects()
                else:
                    QMessageBox.critical(self, "Error", "Failed to archive project")

    def closeEvent(self, event):
        """Clean up when closing application"""
        self.project_manager.close()
        event.accept()
