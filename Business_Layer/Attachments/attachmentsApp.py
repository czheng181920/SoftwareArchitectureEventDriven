from flask import Flask, request, jsonify
import attachmentsLogic as db

app = Flask(__name__)

#TODO: add endpoints for attachments 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)

@app.route('/create_attachment', methods=['POST'])
def create_attachment():
    data = request.json
    attachment_id = data.get('attachment_id')
    meeting_id = data.get('meeting_id')
    url = data.get('url')

    try:
        db.db_create_attachment(attachment_id, meeting_id, url)
        return jsonify({"message": "Attachment created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/attachment/<attachment_id>', methods=['GET'])
def get_attachment_by_id(attachment_id):
    try:
        attachment = db.db_query_attachment_by_id(attachment_id)
        if attachment:
            return jsonify(attachment), 200
        else:
            return jsonify({"error": "Attachment not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/all_attachments', methods=['GET'])
def get_all_attachments():
    try:
        attachment = db.db_query_all_attachments()
        if attachment:
            return jsonify(attachment), 200
        else:
            return jsonify({"error": "Attachments not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500    


@app.route('/update_attachment/<attachment_id>', methods=['PUT'])
def update_participant(attachment_id):
    data = request.json
    name = data.get('name')
    email = data.get('email')

    try:
        db.db_update_attachment(attachment_id, name, email)
        return jsonify({"message": "Attachment updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/delete_attachment/<attachment_id>', methods=['DELETE'])
def delete_participant(attachment_id):
    try:
        db.db_delete_participant(attachment_id)
        return jsonify({"message": "Participant deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


