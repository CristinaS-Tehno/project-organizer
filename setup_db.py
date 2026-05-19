"""
Database setup script - Creates ProjectOrganizer database and tables
Run this script once to initialize your SQL Server database
"""
import pyodbc

print("🔧 Starting database setup...")

# Connect to SQL Server (without specifying a database)
connection_string = (
    'Driver={ODBC Driver 17 for SQL Server};'
    'Server=(local);'
    'Trusted_Connection=yes;'
)

try:
    print("📡 Connecting to SQL Server...")
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    print("✅ Connected to SQL Server!")
    
    # Create database
    print("\n📁 Creating ProjectOrganizer database...")
    cursor.execute("""
        IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'ProjectOrganizer')
        BEGIN
            CREATE DATABASE ProjectOrganizer
        END
    """)
    conn.commit()
    print("✅ Database 'ProjectOrganizer' created!")
    
    # Switch to the database
    print("\n🔀 Switching to ProjectOrganizer database...")
    cursor.execute("USE ProjectOrganizer")
    
    # Create Projects table
    print("📋 Creating Projects table...")
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
    conn.commit()
    print("✅ Table 'Projects' created!")
    
    cursor.close()
    conn.close()
    
    print("\n" + "="*50)
    print("✅ DATABASE SETUP COMPLETED SUCCESSFULLY!")
    print("="*50)
    print("\nYou can now run: python main.py")
    
except pyodbc.Error as e:
    print(f"\n❌ ERROR: {e}")
    print("\nTroubleshooting:")
    print("1. Make sure SQL Server is running")
    print("2. Check your server name with: sqlcmd -L")
    print("3. Update 'Server=(local)' in setup_db.py if needed")
