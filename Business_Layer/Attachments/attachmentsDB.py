import sqlite3

database= 'attachments.db'

def createTable(database):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    # Enable foreign key support in SQLite
    cursor.execute('PRAGMA foreign_keys = ON')

    # Create Attachments table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Attachments (
        attachment_id TEXT PRIMARY KEY,
        meeting_id TEXT,
        url TEXT NOT NULL
    )
    ''')

    connection.commit()
    
    # Check if tables were created
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print("Tables in the database:", tables)
    connection.close()

# Run the function only once
createTable('attachments.db')