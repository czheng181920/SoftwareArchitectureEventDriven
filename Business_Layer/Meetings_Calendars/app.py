from flask import Flask, request, jsonify
import uuid
import re
import logic as db

app = Flask(__name__)

# data layer server IP address and port
# TODO: test this with the actual IP address
DATA_LAYER_URL = 'http://172.20.96.214:5002/store'


def generate_uuid():
    return str(uuid.uuid4())

def is_valid_email(email):
    # Simple regex for validating an email
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None


# Meeting Management
@app.route('/meeting', methods=['POST'])
def create_meeting():
    data = request.json
    meeting_id = data.get('meeting_id', generate_uuid())
    title = data.get('title')
    date_time = data.get('date_time')
    location = data.get('location')
    details = data.get('details')
    
    try:
        db.db_create_meeting(meeting_id, title, date_time, location, details)
        return jsonify({"message": "Meeting created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/meetings', methods=['GET'])
def query_all_meetings():
    try:
        meetings = db.db_query_all_meetings()
        return jsonify(meetings), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/meeting/<meeting_id>', methods=['GET'])
def query_meeting_by_id(meeting_id):
    try:
        meeting = db.db_query_meeting_by_id(meeting_id)
        if meeting:
            return jsonify(meeting), 200
        else:
            return jsonify({"error": "Meeting not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/meeting/<meeting_id>', methods=['PUT'])
def update_meeting(meeting_id):
    data = request.json
    title = data.get('title')
    date_time = data.get('date_time')
    location = data.get('location')
    details = data.get('details')
    # print inputs
    print(meeting_id)
    print(title)
    print(date_time)
    print(location)
    print(details)

    try:
        db.db_update_meeting(meeting_id, title, date_time, location, details)
        return jsonify({"message": "Meeting updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/meeting/<meeting_id>', methods=['DELETE'])
def delete_meeting(meeting_id):
    try:
        db.db_delete_meeting(meeting_id)
        # TODO: call api gateway to delete orphaned attatchments and participants
        return jsonify({"message": "Meeting deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# List Calendars, Participants, and Attachments by Meeting ID
@app.route('/meeting/<meeting_id>/calendars', methods=['GET'])
def list_calendar_by_meeting_id(meeting_id):
    try:
        calendars = db.db_list_calendars_by_meeting_ID(meeting_id)
        return jsonify(calendars), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/meeting/<int:meeting_id>/participants', methods=['GET'])
def list_participants_by_meeting_id(meeting_id):
    try:
        participants = db.db_participant_list_calendar(meeting_id)
        return jsonify({"participants": participants}), 200
    except Exception as e:
        return jsonify({"error": "An error occurred: " + str(e)}), 500

@app.route('/meeting/<int:meeting_id>/attachments', methods=['GET'])
def list_attachments_by_meeting_id(meeting_id):
    try:
        attachments = db.db_attachment_list_calendar(meeting_id)
        return jsonify({"attachments": attachments}), 200
    except Exception as e:
        return jsonify({"error": "An error occurred: " + str(e)}), 500

#Calendar stuff
@app.route('/calendar', methods=['POST'])
def create_calendar():
    data = request.get_json()
    calendar_id = data.get('calendar_id')
    if not calendar_id:
        calendar_id = generate_uuid()
    title = data.get('title')
    details = data.get('details')
    
    try:
        db.db_create_calendar(calendar_id, title, details)
        return jsonify({"message": "Calendar created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/calendars', methods=['GET'])
def query_all_calendars():
    try:
        calendars = db.db_find_all_calendar()
        return jsonify(calendars), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/calendar/<calendar_id>', methods=['GET'])
def query_calendar_by_id(calendar_id):
    try:
        calendar = db.db_query_calendar_by_id(calendar_id)
        if calendar:
            return jsonify(calendar), 200
        else:
            return jsonify({"error": "Calendar not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/calendar/<calendar_id>', methods=['PUT'])
def update_calendar(calendar_id):
    data = request.json
    title = data.get('title')
    details = data.get('details')
    print(title)
    try:
        db.db_update_calendar(calendar_id, title, details)
        return jsonify({"message": "Calendar updated successfully"}), 200
    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/calendar/<calendar_id>', methods=['DELETE'])
def delete_calendar(calendar_id):
    try:
        db.db_delete_calendar(calendar_id)
        # TODO: call api gateway to delete orphaned attatchments and participants (orphaned meeetings are already deleted)
        #  might have to change the trigger to a function so we can retrieve the meeting_id before it's deleted
        return jsonify({"message": "Calendar deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/calendar/<int:calendar_id>/meetings', methods=['GET'])
def see_meetings_in_calendar(calendar_id):
    try:
        meetings = db.db_calendar_list_meeting(calendar_id)
        return jsonify({"meetings": meetings}), 200
    except Exception as e:
        return jsonify({"error": "An error occurred: " + str(e)}), 500

# Business layer route for associating a meeting with a calendar
@app.route('/calendar/addMeeting', methods=['POST'])
def add_meeting_to_calendar():
    data = request.get_json()
    meeting_id = data.get('meeting_id')
    calendar_id = data.get('calendar_id')

    if not meeting_id or not calendar_id:
        return jsonify({"error": "Meeting ID and Calendar ID are required"}), 400

    try:
        db.db_create_associated_calendar_meeting(meeting_id, calendar_id)
        return jsonify({"message": "Meeting associated with calendar successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Calendar-Meeting Management
@app.route('/calendar/<calendar_id>/meeting/<meeting_id>', methods=['DELETE'])
def delete_meeting_calendar(calendar_id, meeting_id):
    data = request.get_json()
    meeting_id = data.get('meeting_id')
    calendar_id = data.get('calendar_id')
    try:
        db.db_delete_meeting_calendar(calendar_id, meeting_id)
        return jsonify({"message": "Meeting deleted from calendar successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/calendar/<calendar_id>/meeting/<meeting_id>', methods=['POST'])
def add_meeting_calendar(calendar_id, meeting_id):
    data = request.get_json()
    meeting_id = data.get('meeting_id')
    calendar_id = data.get('calendar_id')
    try:
        db.db_create_associated_calendar_meeting(meeting_id, calendar_id)
        return jsonify({"message": "Meeting added to calendar successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)