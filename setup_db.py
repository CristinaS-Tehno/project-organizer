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
    # Enable autocommit to avoid transaction issues
    conn.autocommit = True
    cursor = conn.cursor()
    print("✅ Connected to SQL Server!")
    
    # Create database
    print("\n📁 Creating ProjectOrganizer database...")
    try:
        cursor.execute("CREATE DATABASE ProjectOrganizer")
        print("✅ Database 'ProjectOrganizer' created!")
    except pyodbc.Error as e:
        if "already exists" in str(e) or "file already exists" in str(e):
            print("✅ Database 'ProjectOrganizer' already exists!")
        else:
            raise
    
    cursor.close()
    conn.close()
    
    # Create new connection to the database
    print("\n🔄 Connecting to ProjectOrganizer database...")
    db_connection_string = (
        'Driver={ODBC Driver 17 for SQL Server};'
        'Server=(local);'
        'Database=ProjectOrganizer;'
        'Trusted_Connection=yes;'
    )
    db_conn = pyodbc.connect(db_connection_string)
    db_conn.autocommit = True
    db_cursor = db_conn.cursor()
    print("✅ Connected to ProjectOrganizer database!")
    
    # Create Projects table
    print("\n📋 Creating Projects table...")
    db_cursor.execute("""
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
    print("✅ Table 'Projects' created!")
    
    db_cursor.close()
    db_conn.close()
    
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
