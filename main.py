"""
Project Organizer - Main Application Entry Point
A Windows desktop application to organize project information and manage folder structures
"""
import sys
from PyQt6.QtWidgets import QApplication
from views.main_window import MainWindow


def main():
    """Initialize and run the application"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
