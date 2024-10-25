# All of these functions are placeholders for the actual implementation.
# Must also edit cli.py to import the user input for the required functions
import sqlite3

database = 'calendar.db'

def db_create_meeting(meeting_id, title, date_time, location, details):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('''
        INSERT INTO Meetings (meeting_id, title, date_time, location, details) 
        VALUES (?, ?, ?, ?, ?);
    ''', (meeting_id, title, date_time, location, details))
    print('Added Meeting!')

    connection.commit()
    connection.close()

def db_query_all_meetings():
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('SELECT * FROM Meetings')
    allMeetings = cursor.fetchall()

    print('All Meetings:')
    for meeting in allMeetings:
        print(meeting)

    connection.close()
    return allMeetings

def db_query_meeting_by_id(meeting_id):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('SELECT * FROM Meetings WHERE meeting_id=?', (meeting_id,))
    allMeetings = cursor.fetchall()
    
    print('Meeting found:')
    for meeting in allMeetings:
        print(meeting)

    connection.close()
    return allMeetings

def db_update_meeting(meeting_id, title, date_time, location, details):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    # print all inputs to make sure they are correct
    print(f"meeting_id: {meeting_id}, title: {title}, date_time: {date_time}, location: {location}, details: {details}")
    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('UPDATE Meetings SET title=?, date_time=?, location=?, details=? WHERE meeting_id=?', 
                   (title, date_time, location, details, meeting_id))
    
    print(f'Meeting updated: {meeting_id}')
    
    connection.commit()
    connection.close()

def db_delete_meeting(meeting_id):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('DELETE FROM Meetings WHERE meeting_id=?', (meeting_id,))

    connection.commit()
    connection.close()
    print('Deleted Meeting!')
    print(f"Deleted Meeting {meeting_id}")

def db_list_calendars_by_meeting_ID(meeting_id):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('SELECT * FROM Meetings_Calendars WHERE meeting_id=?', (meeting_id,))
    allCalendars = cursor.fetchall()

    print('List of Calendar IDs that belong to this meeting:')
    for calendar in allCalendars:
        print(calendar[1])

    connection.close()
    return allCalendars

def  db_list_participants_by_meeting_ID(meeting_id):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('SELECT * FROM Participants WHERE meeting_id=?', (meeting_id,))
    allParticipants = cursor.fetchall()

    print('List of Participants that belong to this meeting:')
    for participant in allParticipants:
        print(participant)

    connection.close()
    return allParticipants
    
def db_list_attachments_by_meeting_ID(meeting_id):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('SELECT * FROM Attachments WHERE meeting_id=?', (meeting_id,))
    allAttachments = cursor.fetchall()

    print('List of Attachments that belong to this meeting:')
    for attachment in allAttachments:
        print(attachment)

    connection.close()
    return allAttachments

def db_create_calendar(calendar_id, title, details):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    cursor.execute('PRAGMA foreign_keys = ON')
    cursor.execute('''
        INSERT INTO Calendars (calendar_id, title, details) 
        VALUES (?, ?, ?);
    ''', (calendar_id, title, details))
    print('Added Calendar!')

    connection.commit()
    connection.close()

def db_find_all_calendar():
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('SELECT * FROM Calendars')
    allCalendars = cursor.fetchall()

    for meeting in allCalendars:
        print(meeting)

    connection.close()
    return allCalendars

def db_query_calendar_by_id(calendar_id):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('SELECT * FROM Calendars WHERE calendar_id=?', (calendar_id,))
    calendar = cursor.fetchone()

    print(f'Calendar found: {calendar_id}')
    print(calendar)

    connection.close()
    return calendar

def db_update_calendar(calendar_id, title, details):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('UPDATE Calendars SET title=?, details=? WHERE calendar_id=?', 
                   (title, details, calendar_id))
    
    print(f'Calendar updated: {calendar_id}')

    connection.commit()
    connection.close()

def db_delete_calendar(calendar_id):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('DELETE FROM Calendars WHERE calendar_id=?', (calendar_id,))

    connection.commit()
    connection.close()
    print('Deleted Calendar!')
    print(f'Deleted Calendar {calendar_id}')
    
def db_see_meetings_in_calendar(calendar_id):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')
    
    cursor.execute('SELECT * FROM Meetings_Calendars WHERE calendar_id=?', (calendar_id,))
    allMeetings = cursor.fetchall()
    
    
    print('List of Meeting IDs that belong to this calendar:')
    for meeting in allMeetings:
        print(meeting[0])


    connection.close()
    return allMeetings

#create a calendar-meeting relationship
def db_create_associated_calendar_meeting(meeting_id, calendar_id):

    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    cursor.execute('PRAGMA foreign_keys = ON')

    # Verify that the meeting and calendar IDs exist before the insert
    cursor.execute('SELECT * FROM Meetings WHERE meeting_id = ?', (meeting_id,))
    meeting = cursor.fetchone()
    cursor.execute('SELECT * FROM Calendars WHERE calendar_id = ?', (calendar_id,))
    calendar = cursor.fetchone()

    if meeting is None:
        raise ValueError(f"Meeting with ID {meeting_id} does not exist.")
    if calendar is None:
        raise ValueError(f"Calendar with ID {calendar_id} does not exist.")

    # Insert the association into the table
    cursor.execute('''
        INSERT INTO Meetings_Calendars (meeting_id, calendar_id) 
        VALUES (?, ?);
    ''', (meeting_id, calendar_id))

    print('Added Meeting to Calendar!')

    connection.commit()
    connection.close()

def db_delete_meeting_calendar(calendar_id, meeting_id):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('DELETE FROM Meetings_Calendars WHERE calendar_id=? AND meeting_id=?', (calendar_id, meeting_id))

    connection.commit()
    connection.close()
    print(f'Deleted Meeting {meeting_id} from Calendar {calendar_id}')

def db_meeting_list_calendar(meeting_id):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('SELECT calendar_id FROM Meetings_Calendars WHERE meeting_id=?', (meeting_id,))

    allCalendar = cursor.fetchall()
    for c in allCalendar:
        print(c)

    connection.commit()
    connection.close()
    print(f'Calendar List of Meeting {meeting_id}: ')
    return allCalendar

def db_participant_list_calendar(meeting_id):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('SELECT participant_id FROM Participants WHERE meeting_id=?', (meeting_id,))

    allParticipants = cursor.fetchall()
    for p in allParticipants:
        print(p)

    connection.commit()
    connection.close()
    print(f'Participant List of Meeting {meeting_id}: ')
    return allParticipants

def db_attachment_list_calendar(meeting_id):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('SELECT attachment_id FROM Attachments WHERE meeting_id=?', (meeting_id,))

    allParticipants = cursor.fetchall()
    for p in allParticipants:
        print(p)

    connection.commit()
    connection.close()
    print(f'Attachments List of Meeting {meeting_id}: ')
    return allParticipants

def db_calendar_list_meeting(calendar_id):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('SELECT meeting_id FROM Meetings_Calendars WHERE calendar_id=?', (calendar_id,))

    allMeetings = cursor.fetchall()

    print(f'Meeting List for Calendar {calendar_id}: ')
    for m in allMeetings:
        print(m)

    connection.commit()
    connection.close()
    return allMeetings
    



    