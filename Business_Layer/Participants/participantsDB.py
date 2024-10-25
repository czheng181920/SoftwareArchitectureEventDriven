import os
import sqlite3

def createTable(database):
    if not os.path.exists(database):
        print("Database file doesn't exist. Creating...")
        connection = sqlite3.connect(database)
        connection.close()

    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    # Enable foreign key support in SQLite
    cursor.execute('PRAGMA foreign_keys = ON')

    # Create Participants table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Participants (
        participant_id TEXT PRIMARY KEY,
        meeting_id TEXT NOT NULL,
        name TEXT NOT NULL CHECK(length(name) <= 600),
        email TEXT NOT NULL,
        CHECK (email LIKE '%_@__%.__%')
    );
    ''')

    connection.commit()

    # Check if tables were created
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print("Tables in the database:", tables)
    connection.close()

#Run the function only once
#createTable('participants.db')