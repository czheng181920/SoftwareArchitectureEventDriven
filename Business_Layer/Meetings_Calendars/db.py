import sqlite3
import uuid

database= 'calendar.db'

#create tables
def createTable(database):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    # Enable foreign key support in SQLite
    cursor.execute('PRAGMA foreign_keys = ON')

    # Create Meetings table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Meetings (
        meeting_id TEXT PRIMARY KEY,
        title TEXT NOT NULL CHECK(length(title) <= 2000),
        date_time TEXT NOT NULL,
        location TEXT NOT NULL CHECK(length(location) <= 2000),
        details TEXT CHECK(length(details) <= 10000)
    )
    ''')

    # Create Calendars table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Calendars (
        calendar_id TEXT PRIMARY KEY,
        title TEXT NOT NULL CHECK(length(title) <= 2000),
        details TEXT CHECK(length(details) <= 10000)
    )
    ''')

    # Create Meetings_Calendars (many-to-many relationship)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Meetings_Calendars (
        meeting_id TEXT,
        calendar_id TEXT,
        PRIMARY KEY (meeting_id, calendar_id),
        FOREIGN KEY (meeting_id) REFERENCES Meetings(meeting_id) ON DELETE CASCADE,
        FOREIGN KEY (calendar_id) REFERENCES Calendars(calendar_id) ON DELETE CASCADE
    )
    ''')

    # Create trigger to delete orphaned meetings when no associated calendars exist
    cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS delete_orphaned_meetings
    AFTER DELETE ON Meetings_Calendars
    FOR EACH ROW
    WHEN (SELECT COUNT(*) FROM Meetings_Calendars WHERE meeting_id = OLD.meeting_id) = 0
    BEGIN
        DELETE FROM Meetings WHERE meeting_id = OLD.meeting_id;
    END;
    ''')
    
     # Create trigger to delete orphaned calendars when no associated meetings exist
    cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS delete_orphaned_calendars
    AFTER DELETE ON Meetings_Calendars
    FOR EACH ROW
    WHEN (SELECT COUNT(*) FROM Meetings_Calendars WHERE calendar_id = OLD.calendar_id) = 0
    BEGIN
        DELETE FROM Calendars WHERE calendar_id = OLD.calendar_id;
    END;
    ''')

    connection.commit()
    
    # Check if tables were created
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='trigger';")
    triggers = cursor.fetchall()
    print("Triggers in the database:", triggers)

    print("Tables in the database:", tables)
    connection.close()

# create tables
# run only once to create tables
# createTable('calendar.db')

#print data from certain table
def getData():
    connection = sqlite3.connect(database)
    cursor = connection.cursor

    cursor.execute('SELECT * FROM test2')
    data = cursor.fetchall()

    connection.close()
    return data

#get connection
def getConnection():
    return sqlite3.connect(database)




