import sqlite3
database= 'participants.db'

#participant functions
def db_create_participant(participant_id, meeting_id, name, email):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('''
        INSERT INTO Participants (participant_id, meeting_id, name, email) 
        VALUES (?, ?, ?, ?);
    ''', (participant_id, meeting_id, name, email))
    print('Added Participant!')

    connection.commit()
    connection.close()

def db_query_all_participants():
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('SELECT * FROM Participants')
    allParticipants = cursor.fetchall()

    for participant in allParticipants:
        print(participant)

    connection.close()
    return allParticipants

def db_query_participant_by_id(participant_id):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('SELECT * FROM Participants WHERE participant_id=?', (participant_id,))
    participant = cursor.fetchone()

    print(participant)

    connection.close()
    return participant

def db_update_participant(participant_id, name, email):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('UPDATE Participants SET name=?, email=? WHERE participant_id=?', (name, email, participant_id))

    connection.commit()
    connection.close()
    print(f'Updated Participant! {participant_id}')

def db_delete_participant(participant_id):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('DELETE FROM Participants WHERE participant_id=?', (participant_id,))

    connection.commit()
    connection.close()
    print('Deleted Participant!')