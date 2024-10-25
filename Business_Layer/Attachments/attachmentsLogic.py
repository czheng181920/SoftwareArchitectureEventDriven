import sqlite3
database= 'attachments.db'

# attachment functions
def db_create_attachment(attachment_id, meeting_id, url):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    cursor.execute('PRAGMA foreign_keys = ON')
    
    print(f"attachment_id: {attachment_id}, meeting_id: {meeting_id}, attachment_url: {url}")
    cursor.execute('''
        INSERT INTO Attachments (attachment_id, meeting_id, url) 
        VALUES (?, ?, ?);
    ''', (attachment_id, meeting_id, url))
    print('Added Attachment!')

    connection.commit()
    connection.close()
    
def db_query_all_attachments():
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('SELECT * FROM Attachments')
    allAttachments = cursor.fetchall()

    for attachment in allAttachments:
        print(attachment)

    connection.close()
    return allAttachments
    
def db_query_attachment_by_id(attachment_id):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('SELECT * FROM Attachments WHERE attachment_id=?', (attachment_id,))
    attachment = cursor.fetchone()

    print(attachment)

    connection.close()
    return attachment

def db_update_attachment(attachment_id, url):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('UPDATE Attachments SET url=? WHERE attachment_id=?', (url, attachment_id))

    connection.commit()
    connection.close()
    print(f'Updated Attachment! {attachment_id}')

def db_delete_attachment(attachment_id):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('DELETE FROM Attachments WHERE attachment_id=?', (attachment_id,))

    connection.commit()
    connection.close()
    print('Deleted Attachment!')