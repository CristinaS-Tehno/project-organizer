"""
Database module for SQL Server operations
"""
import pyodbc
from datetime import datetime
from pathlib import Path


class Database:
    """Handles all database operations with SQL Server"""

    def __init__(self, connection_string=None):
        """
        Initialize database connection
        
        Args:
            connection_string: SQL Server connection string
        """
        if connection_string is None:
            self.connection_string = (
                'Driver={ODBC Driver 17 for SQL Server};'
                'Server=(local);'
                'Database=ProjectOrganizer;'
                'Trusted_Connection=yes;'
            )
        else:
            self.connection_string = connection_string
        
        self.connection = None
        self.connect()

    def connect(self):
        """Establish database connection"""
        try:
            self.connection = pyodbc.connect(self.connection_string)
            self.connection.autocommit = True
            print("Database connection established")
            return True
        except pyodbc.Error as e:
            print(f"Database connection failed: {e}")
            return False

    def initialize_database(self):
        """Create database and tables if they don't exist"""
        if not self.connection:
            self.connect()
        
        cursor = self.connection.cursor()
        
        try:
            # Create projects table
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM information_schema.tables 
                              WHERE table_name = 'Projects')
                BEGIN
                    CREATE TABLE Projects (
                        ProjectID INT PRIMARY KEY IDENTITY(1,1),
                        Name NVARCHAR(255) NOT NULL,
                        Description NVARCHAR(MAX),
                        Category NVARCHAR(100),
                        Path NVARCHAR(500) NOT NULL,
                        Template NVARCHAR(100),
                        Status NVARCHAR(50) DEFAULT 'active',
                        CreatedAt DATETIME DEFAULT GETDATE(),
                        UpdatedAt DATETIME DEFAULT GETDATE()
                    )
                END
            """)
            print("Database initialized successfully")
            return True
        except pyodbc.Error as e:
            print(f"Error initializing database: {e}")
            return False
        finally:
            cursor.close()

    def create_project(self, name, description, category, path, template):
        """Create a new project in the database"""
        if not self.connection:
            self.connect()
        
        cursor = self.connection.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO Projects (Name, Description, Category, Path, Template, Status, CreatedAt, UpdatedAt)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, description, category, path, template, 'active', datetime.now(), datetime.now()))
            
            # Get the ID of the inserted row
            cursor.execute("SELECT @@IDENTITY")
            project_id = cursor.fetchone()[0]
            print(f"Project '{name}' created in database")
            return project_id
        except pyodbc.Error as e:
            print(f"Error creating project: {e}")
            return None
        finally:
            cursor.close()

    def get_all_projects(self):
        """Retrieve all projects from database"""
        if not self.connection:
            self.connect()
        
        cursor = self.connection.cursor()
        
        try:
            cursor.execute("""
                SELECT ProjectID, Name, Description, Category, Path, Template, Status, CreatedAt, UpdatedAt
                FROM Projects
                WHERE Status = 'active'
                ORDER BY UpdatedAt DESC
            """)
            rows = cursor.fetchall()
            return rows
        except pyodbc.Error as e:
            print(f"Error retrieving projects: {e}")
            return []
        finally:
            cursor.close()

    def search_projects(self, search_term):
        """Search projects by name or description"""
        if not self.connection:
            self.connect()
        
        cursor = self.connection.cursor()
        
        try:
            cursor.execute("""
                SELECT ProjectID, Name, Description, Category, Path, Template, Status, CreatedAt, UpdatedAt
                FROM Projects
                WHERE (Name LIKE ? OR Description LIKE ?) AND Status = 'active'
                ORDER BY UpdatedAt DESC
            """, (f"%{search_term}%", f"%{search_term}%"))
            rows = cursor.fetchall()
            return rows
        except pyodbc.Error as e:
            print(f"Error searching projects: {e}")
            return []
        finally:
            cursor.close()

    def get_projects_by_category(self, category):
        """Get projects filtered by category"""
        if not self.connection:
            self.connect()
        
        cursor = self.connection.cursor()
        
        try:
            cursor.execute("""
                SELECT ProjectID, Name, Description, Category, Path, Template, Status, CreatedAt, UpdatedAt
                FROM Projects
                WHERE Category = ? AND Status = 'active'
                ORDER BY UpdatedAt DESC
            """, (category,))
            rows = cursor.fetchall()
            return rows
        except pyodbc.Error as e:
            print(f"Error retrieving projects by category: {e}")
            return []
        finally:
            cursor.close()

    def update_project(self, project_id, name=None, description=None, category=None, status=None):
        """Update project information"""
        if not self.connection:
            self.connect()
        
        cursor = self.connection.cursor()
        
        try:
            updates = []
            params = []
            
            if name:
                updates.append("Name = ?")
                params.append(name)
            if description:
                updates.append("Description = ?")
                params.append(description)
            if category:
                updates.append("Category = ?")
                params.append(category)
            if status:
                updates.append("Status = ?")
                params.append(status)
            
            updates.append("UpdatedAt = ?")
            params.append(datetime.now())
            params.append(project_id)
            
            query = f"""
                UPDATE Projects
                SET {', '.join(updates)}
                WHERE ProjectID = ?
            """
            
            cursor.execute(query, params)
            print(f"Project {project_id} updated")
            return True
        except pyodbc.Error as e:
            print(f"Error updating project: {e}")
            return False
        finally:
            cursor.close()

    def delete_project(self, project_id):
        """Archive a project (soft delete)"""
        return self.update_project(project_id, status='archived')

    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print("Database connection closed")
