from flask import Flask, request, jsonify
import participantsLogic as db

app = Flask(__name__)

#TODO: add endpoints for participants 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)

@app.route('/create_participant', methods=['POST'])
def create_participant():
    data = request.json
    participant_id = data.get('participant_id')
    meeting_id = data.get('meeting_id')
    name = data.get('name')
    email = data.get('email')

    print(data)

    try:
        db.db_create_participant(participant_id, meeting_id, name, email)
        return jsonify({"message": "Participant created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/all_participants', methods=['GET'])
def get_all_participants():
    try:
        participants = db.db_query_all_participants()
        return jsonify(participants), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/participant/<participant_id>', methods=['GET'])
def get_participant_by_id(participant_id):
    try:
        participant = db.db_query_participant_by_id(participant_id)
        if participant:
            return jsonify(participant), 200
        else:
            return jsonify({"error": "Participant not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/update_participant/<participant_id>', methods=['PUT'])
def update_participant(participant_id):
    data = request.json
    name = data.get('name')
    email = data.get('email')

    try:
        db.db_update_participant(participant_id, name, email)
        return jsonify({"message": "Participant updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete_participant/<participant_id>', methods=['DELETE'])
def delete_participant(participant_id):
    try:
        db.db_delete_participant(participant_id)
        return jsonify({"message": "Participant deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

