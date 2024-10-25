import uuid
#import Data_Layer.logic as logic
import re
import requests

API_GATEWAY_URL = 'http://172.20.180.53:5001'

def main_menu():

    while True:
        print("\n \nWelcome to the Meeting Management CLI")
        print("Select an option to manage:")
        print("1. Meetings")
        print("2. Calendars")
        print("3. Participants")
        print("4. Attachments")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            manage_meetings()
        elif choice == '2':
            manage_calendars()
        elif choice == '3':
            manage_participants() 
        elif choice == '4':
            manage_attachments()
        elif choice == '5':
            exit()
        else:
            print("Invalid input. Please try again.")
            main_menu()

# Input validation
def get_input(prompt, validation_fn=None):
    while True:
        user_input = input(prompt)
        if validation_fn and not validation_fn(user_input):
            print("Invalid input. Please try again.")
        else:
            return user_input

def generate_uuid():
    return str(uuid.uuid4())


def is_valid_email(email):
    # Simple regex for validating an email
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

#chelsea
def create_meeting():
    #user can make their own meeting id
    meeting_id = get_input("Enter meeting ID (or type 'done' to finish): ")
    if meeting_id.lower() == 'done':
        meeting_id = generate_uuid()
    title = get_input("Enter meeting title: ")
    date_time = get_input("Enter meeting date and time (YYYY-MM-DD HH:MM AM/PM): ")
    location = get_input("Enter meeting location: ")
    details = get_input("Enter meeting details: ")

    # logic.db_create_meeting(meeting_id, title, date_time, location, details)

    # Send POST request to the MeetingsCalendars service via API Gateway
    response = requests.post(f"{API_GATEWAY_URL}/meetings", json={
        'meeting_id': meeting_id,
        'title': title,
        'date_time': date_time,
        'location': location,
        'details': details
    })

    if response.status_code == 201:
        print(f"Meeting created with ID: {meeting_id}")
    else:
        print(f"Failed to create meeting: {response.json().get('error', 'Unknown error')}")

    # Prompt for associated calendars
    while True:
        calendar_id = input("Enter associated calendar ID (or type 'done' to finish): ")
        if calendar_id.lower() == 'done':
            break
        # Send POST request to Participants service via API Gateway
        response = requests.post(f"{API_GATEWAY_URL}/participants", json={
            'participant_id': participant_id,
            'meeting_id': meeting_id,
            'name': name,
            'email': email
        })
        if response.status_code == 201:
            print(f"Participant {name} added with ID: {participant_id}")
        else:
            print(f"Failed to add participant: {response.json().get('error', 'Unknown error')}")
        print(f"Associated calendar {calendar_id} added.")

    # Prompt for participants
    while True:
        name = input("Enter participant name (or type 'done' to finish): ")
        if name.lower() == 'done':
            break
        email = get_input("Enter participant email: ")
        
        # validate email
        while (not is_valid_email(email)):
            print("Invalid email. Please enter a valid email.")
            email = get_input("Enter participant email: ")
        
        if not is_valid_email(email):
            print("Invalid email format. Please enter a valid email.")
            continue
        
        participant_id = str(uuid.uuid4())
        print(f"Debug: Adding participant with meeting ID {meeting_id}")
# Send POST request to Attachments service via API Gateway
        response = requests.post(f"{API_GATEWAY_URL}/attachments", json={
            'attachment_id': attachment_id,
            'meeting_id': meeting_id,
            'url': url
        })
        if response.status_code == 201:
            print(f"Participant {name} added with ID: {participant_id}")
        else:
            print(f"Failed to add attachment: {response.json().get('error', 'Unknown error')}")
            
    # Prompt for attachments
    while True:
        url = get_input("Enter attachment URL (or type 'done' to finish): ")
        if url.lower() == 'done':
            break

        attachment_id = generate_uuid()  # Generate UUID for the attachment

# Send POST request to Attachments service via API Gateway
        response = requests.post(f"{API_GATEWAY_URL}/attachments", json={
            'attachment_id': attachment_id,
            'meeting_id': meeting_id,
            'url': url
        })
        if response.status_code == 201:
            print(f"Attachment {url} added.")
        else:
            print(f"Failed to add attachment: {response.json().get('error', 'Unknown error')}")

def list_calendar_by_meeting_ID():
    meeting_id = get_input("Enter meeting ID to see the calendars that contain this meeting: ")

    try:
        # Send GET request with meeting ID as query parameter
        url = f"{API_GATEWAY_URL}/listofCalendars?meeting_id={meeting_id}"
        response = requests.get(url, headers={'Content-Type': 'application/json'})

        if response.status_code == 200:
            calendars_data = response.json()
            print("Calendars retrieved successfully:")

            # Check if the response contains data and is a list
            if isinstance(calendars_data, list) and len(calendars_data) > 0:
                for calendar in calendars_data:
                    print(f"\nCalendar ID: {calendar[0] or 'N/A'}")
                    print(f"Name: {calendar[1] or 'N/A'}")
                    print(f"Details: {calendar[2] or 'N/A'}")
            else:
                print("No calendars found for this meeting.")
        else:
            print(f"Error retrieving calendars: Status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def list_participants_by_meeting_ID():
    meeting_id = get_input("Enter meeting_id to see the participants in this meeting: ")

    try:
        # Send request to the API Gateway to get the list of participants for the meeting
        response = requests.get(f"{API_GATEWAY_URL}/meeting/{meeting_id}/participants")

        if response.ok:
            participants_data = response.json()
            if participants_data:
                print("Participants in Meeting:")
                for participant in participants_data:
                    print(f"ID: {participant.get('participant_id')}, Name: {participant.get('name')}, Email: {participant.get('email')}")
            else:
                print("No participants found for this meeting.")
        else:
            print("Error retrieving participants:", response.status_code, response.json())

    except Exception as e:
        print("An error occurred:", str(e))   
 
def list_attachments_by_meeting_ID():
    meeting_id = get_input("Enter meeting_id to see the attachments in this meeting: ")

    try:
        # Send request to the API Gateway to get the list of attachments for the meeting
        response = requests.get(f"{API_GATEWAY_URL}/meeting/{meeting_id}/attachments")

        if response.ok:
            attachments_data = response.json()
            if attachments_data:
                print("Attachments for Meeting:")
                for attachment in attachments_data:
                    print(f"ID: {attachment.get('attachment_id')}, Name: {attachment.get('name')}, URL: {attachment.get('url')}")
            else:
                print("No attachments found for this meeting.")
        else:
            print("Error retrieving attachments:", response.status_code, response.json())

    except Exception as e:
        print("An error occurred:", str(e))

def is_valid_email(email: str) -> bool:
    # Regular expression for validating an email
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    # Check if the email matches the regular expression
    if re.match(email_regex, email):
        return True
    return False

#neha
def query_all_meetings():
    try:
        # Send a GET request to the API endpoint for all meetings
        url = f"{API_GATEWAY_URL}/meetings"
        response = requests.get(url)

        if response.status_code == 200:
            meetings_data = response.json()
            print("\nAll Meetings:")

            # Iterate through each meeting and display the details
            for meeting in meetings_data:
                print(f"\nMeeting ID: {meeting[0] or 'N/A'}")
                print(f"Title: {meeting[1] or 'N/A'}")
                print(f"Date: {meeting[2] or 'N/A'}")
                print(f"Location: {meeting[3] or 'N/A'}")
                print(f"Details: {meeting[4] or 'N/A'}")
        else:
            print(f"Error retrieving meetings: Status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

#neha 
def query_meeting_by_id():
    meeting_id = get_input("Enter meeting_id of meeting to be found: ")

    # Send a GET request to the Flask API with the meeting ID
    url = f"{API_GATEWAY_URL}/meetingByID?meeting-id={meeting_id}"
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'})
        
        # Check if the request was successful
        if response.status_code == 200:
            meeting_data = response.json()

            # Display the meeting data (adjust based on your API response structure)
            if meeting_data:
                print("\nMeeting Details:")
                print(f"ID: {meeting_data[0][0]}")
                print(f"Title: {meeting_data[0][1]}")
                print(f"Date: {meeting_data[0][2]}")
                print(f"Location: {meeting_data[0][3]}")
                print(f"Details: {meeting_data[0][4]}")
            else:
                print("No meeting found with that ID.")
        else:
            print(f"Failed to retrieve meeting. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the server: {e}")

#neha
def update_meeting():
    meeting_id = get_input("Enter meeting_id of meeting to be updated: ")
    title = get_input("Enter updated meeting title: ")
    date_time = get_input("Enter updated meeting date and time (YYYY-MM-DD HH:MM AM/PM): ")
    location = get_input("Enter updated meeting location: ")
    details = get_input("Enter updated meeting details: ")

    # Create the data object
    data = {
        "meeting_id": meeting_id,
        "title": title,
        "date_time": date_time,
        "location": location,
        "details": details
    }

    # API request to update meeting
    try:
        url = f"{API_GATEWAY_URL}/updateMeeting"
        response = requests.put(url, json=data, headers={'Content-Type': 'application/json'})

        if response.status_code == 200:
            updated_meeting = response.json()
            print("Updated Meeting:", updated_meeting)
        else:
            print(f"Error updating meeting: Status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

# amala
def delete_meeting():
    # Get meeting ID from user input
    meeting_id = get_input("Enter meeting ID to delete: ")

    # Create the data object
    data = {
        "meeting_id": meeting_id
    }

    # API request to delete meeting
    try:
        url = f"{API_GATEWAY_URL}/deleteMeeting"
        response = requests.delete(url, json=data, headers={'Content-Type': 'application/json'})

        if response.status_code == 200:
            result = response.json()
            print(f"Meeting deleted successfully: {result.get('message', 'No message provided')}")
        else:
            print(f"Error deleting meeting: Status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


# amala
def create_calendar():
    calendar_id = get_input("Enter calendar ID (or type 'done' to finish): ")
    if calendar_id.lower() == 'done':
        calendar_id = generate_uuid()
    title = get_input("Enter calendar title: ")
    details = get_input("Enter details: ")

    # Prepare the data for the request
    data = {
        'calendar_id': calendar_id,
        'title': title,
        'details': details
    }

    try:
        # Make a POST request to the API Gateway
        response = requests.post(f'{API_GATEWAY_URL}/calendar', json=data, headers={
            'Content-Type': 'application/json'
        })

        if response.ok:
            calendar_response = response.json()
            print('Calendar created successfully:', calendar_response)
        else:
            print('Error creating calendar:', response.status_code, response.json())

    except Exception as error:
        print('Error:', error)


#amala
def query_all_calendars():
    try:
        # Make a GET request to the API Gateway
        response = requests.get(f'{API_GATEWAY_URL}/calendars', headers={
            'Content-Type': 'application/json'
        })

        if response.ok:
            calendars = response.json()
            print('Calendars retrieved successfully:', calendars)
            return calendars  # Return the list of calendars
        else:
            print('Error retrieving calendars:', response.status_code, response.json())
            return None  # Return None on error

    except Exception as error:
        print('Error:', error)
        return None  # Return None on exception


#amala
def query_calendar_by_id():
    calendar_id = get_input("Enter calendar_id of calendar to be found: ")

    try:
        # Make a GET request to the API Gateway for the specific calendar
        response = requests.get(f'{API_GATEWAY_URL}/calendar/{calendar_id}', headers={
            'Content-Type': 'application/json'
        })

        if response.ok:
            calendar = response.json()
            print('Calendar retrieved successfully:', calendar)
            return calendar  # Return the calendar details
        else:
            print('Error retrieving calendar:', response.status_code, response.json())
            return None  # Return None on error

    except Exception as error:
        print('Error:', error)
        return None  # Return None on exception
    
#amala
def update_calendar():
    calendar_id = get_input("Enter calendar_id of calendar to be found: ")

    title = get_input("Enter calendar title: ")
    details = get_input("Enter details: ")

    data = {
        "calendar_title": title,
        "calendar_details": details
    }
    
    try:
        # Make a PUT request to the API Gateway for the specific calendar
        response = requests.put(f'{API_GATEWAY_URL}/calendar/{calendar_id}', json=data, headers={
            'Content-Type': 'application/json'
        })

        if response.ok:
            updated_calendar = response.json()
            print('Calendar updated successfully:', updated_calendar)
            return updated_calendar  # Return the updated calendar details
        else:
            print('Error updating calendar:', response.status_code, response.json())
            return None  # Return None on error

    except Exception as error:
        print('Error:', error)
        return None  # Return None on exception

#amala
def delete_calendar():
    calendar_id = get_input("Enter calendar_id of calendar to be deleted: ")

    try:
        # Make a DELETE request to the API Gateway for the specific calendar
        response = requests.delete(f'{API_GATEWAY_URL}/calendar/{calendar_id}', headers={
            'Content-Type': 'application/json'
        })

        if response.ok:
            print('Calendar deleted successfully:', response.json())
            return response.json()  # Return the response message
        else:
            print('Error deleting calendar:', response.status_code, response.json())
            return None  # Return None on error

    except Exception as error:
        print('Error:', error)
        return None  # Return None on exception    

def see_meetings_in_calendar():
    calendar_id = get_input("Enter calendar_id of calendar to see meetings: ")
 
    try:
        # Make a GET request to the API Gateway for the specific calendar's meetings
        response = requests.get(f'{API_GATEWAY_URL}/calendar/{calendar_id}/meetings', headers={
            'Content-Type': 'application/json'
        })

        if response.ok:
            meetings = response.json()
            print('Meetings retrieved successfully:', meetings)
            return meetings  # Return the list of meetings
        else:
            print('Error retrieving meetings:', response.status_code, response.json())
            return None  # Return None on error

    except Exception as error:
        print('Error:', error)
        return None  # Return None on exception

def create_participant():
    meeting_id = get_input("Enter meeting ID: ")
    
    # Validate meeting ID
    if not logic.db_check_meeting_id(meeting_id):
        print("Invalid meeting ID. Please enter a valid meeting ID.")
        return
    
    name = get_input("Enter participant name: ")
    email = get_input("Enter participant email: ")
    while (not is_valid_email(email)):
            print("Invalid email. Please enter a valid email.")
            email = get_input("Enter participant email: ")
    
    participant_id = get_input("Enter participant ID (or type 'done' to finish): ")
    if participant_id.lower() == 'done':
       participant_id = generate_uuid()

    data = {
        "participant_id": participant_id,
        "meeting_id": meeting_id,
        "name": name,
        "email": email
    }

    # Send request to create the participant
    response = requests.post(f"{API_GATEWAY_URL}/participant", json=data)

    if response.ok:
        print("Participant created successfully:", response.json())
    else:
        print("Error creating participant:", response.status_code, response.json())

def query_all_participants():
    try:
        # Send request to the API Gateway to get all participants
        response = requests.get(f"{API_GATEWAY_URL}/participants")

        if response.ok:
            participants_data = response.json()
            if isinstance(participants_data, list) and participants_data:
                print("Participants retrieved successfully:")
                for participant in participants_data:
                    print(f"ID: {participant.get('participant_id')}, Name: {participant.get('name')}, Email: {participant.get('email')}")
            else:
                print("No participants found.")
        else:
            print("Error retrieving participants:", response.status_code, response.json())

    except Exception as e:
        print("An error occurred:", str(e))

def query_participant_by_id():
    participant_id = get_input("Enter participant ID: ")
    try:
        # Send request to the API Gateway to get the participant by ID
        response = requests.get(f"{API_GATEWAY_URL}/participant/{participant_id}")

        if response.ok:
            participant_data = response.json()
            if participant_data:
                print("Participant retrieved successfully:")
                print(f"ID: {participant_data.get('participant_id')}")
                print(f"Name: {participant_data.get('name')}")
                print(f"Email: {participant_data.get('email')}")
            else:
                print("Participant not found.")
        else:
            print("Error retrieving participant:", response.status_code, response.json())

    except Exception as e:
        print("An error occurred:", str(e))

def update_participant():
    participant_id = get_input("Enter participant ID: ")
    name = get_input("Enter new participant name: ")
    email = get_input("Enter new participant email: ")
    while (not is_valid_email(email)):
            print("Invalid email. Please enter a valid email.")
            email = get_input("Enter participant email: ")

   # Create the data object
    data = {
        "participant_id": participant_id,
        "name": name,
        "email": email
    }

    # API request to update participant
    try:
        url = f"{API_GATEWAY_URL}/updateParticipants"
        response = requests.put(url, json=data, headers={'Content-Type': 'application/json'})

        if response.status_code == 200:
            updated_participant = response.json()
            print("Participant updated successfully:", updated_participant)
        else:
            print(f"Error updating participant: Status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def delete_participant():

    participant_id = get_input("Enter participant ID to delete: ")

    # Create the data object
    data = {
        "participant_id": participant_id
    }

    # API request to delete participant
    try:
        response = requests.delete(f"{API_GATEWAY_URL}/participant/{participant_id}")

        if response.status_code == 200:
            result = response.json()
            print(f"Participant deleted successfully: {result.get('message', 'No message provided')}")
        else:
            print(f"Error deleting participant: Status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def create_attachment():
    meeting_id = get_input("Enter meeting ID: ")
    
    # Validate meeting ID
    if not logic.db_check_meeting_id(meeting_id):
        print("Invalid meeting ID. Please enter a valid meeting ID.")
        return
    
    attachment_id = get_input("Enter attachment ID (or type 'done' to generate a new ID): ")
    if attachment_id.lower() == 'done':
        attachment_id = generate_uuid()
    
    attachment_name = get_input("Enter attachment name: ")
    attachment_url = get_input("Enter attachment URL: ")

    # Prepare data for the POST request
    data = {
        'attachment_id': attachment_id,
        'name': attachment_name,
        'file': attachment_url,
        'meeting_id': meeting_id  # Include meeting ID if needed by the backend
    }

    # Make the POST request to the /attachment endpoint
    try:
        response = requests.post(f'{API_GATEWAY_URL}/attachment', json=data)  # Use API_GATEWAY_URL
        if response.ok:
            response_data = response.json()
            print('Attachment added successfully:', response_data)
        else:
            print('Error adding attachment:', response.status_code)
    except Exception as error:
        print('Error:', error)

def query_all_attachments():
    try:
        # Make a GET request to the API Gateway
        response = requests.get(f'{API_GATEWAY_URL}/attachments', headers={
            'Content-Type': 'application/json'
        })

        if response.ok:
            attachment_data = response.json()
            print('Attachments retrieved successfully:', attachment_data)

            # Check if attachment_data is a list and has data
            if isinstance(attachment_data, list) and len(attachment_data) > 0:
                for attachment in attachment_data:
                    # Create an attachment item, similar to HTML output
                    attachment_id = attachment.get('attachment_id', 'N/A')
                    attachment_name = attachment.get('name', 'N/A')
                    attachment_file = attachment.get('file', 'N/A')

                    # Print out the details
                    print(f'ID: {attachment_id}\nName: {attachment_name}\nFile: {attachment_file}\n')

            else:
                print('No attachments found.')
        else:
            print('Error retrieving attachments:', response.status_code)

    except Exception as error:
        print('Error:', error)

def query_attachment_by_id():
    attachment_id = get_input("Enter attachment ID: ")

    try:
        # Make a GET request to the API Gateway for a specific attachment ID
        response = requests.get(f'{API_GATEWAY_URL}/attachment/{attachment_id}', headers={
            'Content-Type': 'application/json'
        })

        if response.ok:
            attachment_data = response.json()
            print('Attachment retrieved successfully:', attachment_data)

            # Display attachment details
            attachment_id = attachment_data.get('attachment_id', 'N/A')
            attachment_name = attachment_data.get('name', 'N/A')
            attachment_file = attachment_data.get('file', 'N/A')

            print(f'ID: {attachment_id}\nName: {attachment_name}\nFile: {attachment_file}\n')
        else:
            print('Error retrieving attachment:', response.status_code)

    except Exception as error:
        print('Error:', error)

def update_attachment():
    attachment_id = get_input("Enter attachment ID: ")
    url = get_input("Enter new attachment url: ")

    try:
        # Prepare the data to be sent in the PUT request
        data = {
            'url': url
        }

        # Make a PUT request to the API Gateway for a specific attachment ID
        response = requests.put(f'{API_GATEWAY_URL}/attachment/{attachment_id}', json=data, headers={
            'Content-Type': 'application/json'
        })

        if response.ok:
            updated_attachment_data = response.json()
            print('Attachment updated successfully:', updated_attachment_data)
        else:
            print('Error updating attachment:', response.status_code, response.json())

    except Exception as error:
        print('Error:', error)

def delete_attachment():
    attachment_id = get_input("Enter attachment ID: ")

    try:
        # Make a DELETE request to the API Gateway for a specific attachment ID
        response = requests.delete(f'{API_GATEWAY_URL}/attachment/{attachment_id}', headers={
            'Content-Type': 'application/json'
        })

        if response.ok:
            print('Attachment deleted successfully:', response.json())
        else:
            print('Error deleting attachment:', response.status_code, response.json())

    except Exception as error:
        print('Error:', error)

#manage meetings in calendar
def delete_meeting_calendar():
    calendar_id = get_input("Enter calendar_id of calendar for meeting to be deleted: ")
    meeting_id = get_input(f"Enter meeting_id of meeting from calendar {calendar_id} to be deleted: ")

    try:
        # Send DELETE request to the API Gateway to delete the meeting from the specified calendar
        response = requests.delete(f"{API_GATEWAY_URL}/calendar/{calendar_id}/meeting/{meeting_id}")

        if response.ok:
            result = response.json()
            print("Meeting deleted successfully from the calendar:", result.get('message', 'Meeting deleted.'))
        else:
            print("Error deleting meeting from calendar:", response.status_code, response.json())

    except Exception as e:
        print("An error occurred:", str(e))

def add_meeting_calendar():
    calendar_id = get_input("Enter calendar_id of calendar for meeting to be added: ")
    meeting_id = get_input(f"Enter meeting_id of meeting from calendar {calendar_id} to be added: ")
    
    if not meeting_id or not calendar_id:
        print("Error: Meeting ID and Calendar ID are required")
        return {"error": "Meeting ID and Calendar ID are required"}, 400

    try:
        # Forward the request to the data layer
        response = requests.post(f'{API_GATEWAY_URL}/calendar/addMeeting', json={
            'meeting_id': meeting_id,
            'calendar_id': calendar_id
        })

        # Check if the request was successful
        if response.ok:
            print('Meeting added successfully:', response.json())
            return response.json(), response.status_code
        else:
            print('Error adding meeting:', response.status_code, response.json())
            return response.json(), response.status_code

    except Exception as e:
        print('Error:', str(e))
        return {"error": str(e)}, 500

#meetings and their lists
def list_of_calendars_meeting():
    meeting_id = get_input("Enter meeting_id of Calendar list: ")
    
    try:
        # Send request to the API Gateway to get the list of calendars for the meeting
        response = requests.get(f"{API_GATEWAY_URL}/meeting/{meeting_id}/calendars")

        if response.ok:
            calendars_data = response.json()
            if calendars_data:
                print("Calendars for Meeting:")
                for calendar in calendars_data:
                    print(f"ID: {calendar.get('calendar_id')}, Title: {calendar.get('title')}, Details: {calendar.get('details')}")
            else:
                print("No calendars found for this meeting.")
        else:
            print("Error retrieving calendars:", response.status_code, response.json())

    except Exception as e:
        print("An error occurred:", str(e))

def list_of_participants_meeting():
     meeting_id = get_input("Enter meeting_id of Participants list: ")
     
     try:
        # Send request to the API Gateway to get the list of participants for the meeting
        response = requests.get(f"{API_GATEWAY_URL}/meeting/{meeting_id}/participants")

        if response.ok:
            participants_data = response.json()
            if participants_data:
                print("Participants for Meeting:")
                for participant in participants_data:
                    print(f"ID: {participant.get('participant_id')}, Name: {participant.get('name')}, Email: {participant.get('email')}")
            else:
                print("No participants found for this meeting.")
        else:
            print("Error retrieving participants:", response.status_code, response.json())

     except Exception as e:
        print("An error occurred:", str(e))

def list_of_attachments_meeting():
    meeting_id = get_input("Enter meeting_id of Attachments list: ")
    try:
        # Send request to the API Gateway to get the list of attachments for the meeting
        response = requests.get(f"{API_GATEWAY_URL}/meeting/{meeting_id}/attachments")

        if response.ok:
            attachments_data = response.json()
            if attachments_data:
                print("Attachments for Meeting:")
                for attachment in attachments_data:
                    print(f"ID: {attachment.get('attachment_id')}, Name: {attachment.get('name')}, URL: {attachment.get('url')}")
            else:
                print("No attachments found for this meeting.")
        else:
            print("Error retrieving attachments:", response.status_code, response.json())

    except Exception as e:
        print("An error occurred:", str(e))

# calendar and their lists
def list_of_meetings_calendar():
    calendar_id = get_input("Enter calendar_id of Meeting List: ")

    logic.db_calendar_list_meeting(calendar_id)

def manage_meetings():
    print("\nManage Meetings")
    print("Select an option:")
    print("1. Create Meeting")
    print("2. Query All Meetings")
    print("3. Query Meeting by ID")
    print("4. Update Meeting")
    print("5. Delete Meeting")
    print ("6. List of Calendars for a Meeting")
    print ("7. List of Participants for a Meeting")
    print ("8. List of Attachments for a Meeting")
    
    choice = input("Enter your choice: ")
    if choice == '1':
        create_meeting()  
    elif choice == '2':
        query_all_meetings() 
    elif choice == '3':
        query_meeting_by_id() 
    elif choice == '4':
        update_meeting() 
    elif choice == '5':
        delete_meeting() 
    elif choice == '6':
        list_calendar_by_meeting_ID() 
    elif choice == '7':
        list_participants_by_meeting_ID()
    elif choice == '8':
        list_attachments_by_meeting_ID()
    else:
        print("Invalid input. Please try again.")
        manage_meetings()

def manage_calendars():
    print("\nManage Calendars")
    print("Select an option:")
    print("1. Create Calendar")
    print("2. Query All Calendars")
    print("3. Query Calendar by ID")
    print("4. Update Calendar")
    print("5. Delete Calendar")
    print("6. Delete Meeting from Calendar")
    print("7. Add Meeting to Calender")
    print ("8. List of Meetings for a Calendar")
    
    choice = input("Enter your choice: ")
    if choice == '1':
        create_calendar()  
    elif choice == '2':
        query_all_calendars()  
    elif choice == '3':
        query_calendar_by_id() 
    elif choice == '4':
        update_calendar()
    elif choice == '5':
        delete_calendar()
    elif choice == '6':
        delete_meeting_calendar()
    elif choice == '7':
        add_meeting_calendar()
    elif choice == '8':
        list_of_meetings_calendar()  
    else:
        print("Invalid input. Please try again.")
        manage_calendars()

def manage_participants():
    print("\nManage Participants")
    print("Select an option:")
    print("1. Create Participant")
    print("2. Query All Participants")
    print("3. Query Participant by ID")
    print("4. Update Participant")
    print("5. Delete Participant")
    
    choice = input("Enter your choice: ")
    if choice == '1':
        create_participant() 
    elif choice == '2':
        query_all_participants() 
    elif choice == '3':
        query_participant_by_id()
    elif choice == '4':
        update_participant() 
    elif choice == '5':
        delete_participant() 
    else:
        print("Invalid input. Please try again.")
        manage_participants()

def manage_attachments():
    print("\nManage Attachments")
    print("Select an option:")
    print("1. Create Attachment")
    print("2. Query All Attachments")
    print("3. Query Attachment by ID")
    print("4. Update Attachment")
    print("5. Delete Attachment")
    
    choice = input("Enter your choice: ")
    if choice == '1':
        create_attachment() 
    elif choice == '2':
        query_all_attachments() 
    elif choice == '3':
        query_attachment_by_id()
    elif choice == '4':
        update_attachment()
    elif choice == '5':
        delete_attachment()
    else:
        print("Invalid input. Please try again.")
        manage_attachments()

if __name__ == "__main__":
    main_menu()