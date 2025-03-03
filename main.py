from flask import Flask, request, jsonify, send_from_directory
import tiw_secrets
import fabman
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static')
# Update CORS configuration to be more specific
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5000", "http://127.0.0.1:5000"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})

# Initialize Fabman client
secrets = tiw_secrets.Secrets()
fab = fabman.Fabman(secrets.fabman_api_key)

@app.route('/api/search-members', methods=['GET'])
def search_members():
    search_term = request.args.get('q', '')
    if not search_term:
        return jsonify({'error': 'Search term is required'}), 400
    
    try:
        members = fab.get_members(q=search_term)
        # Convert members to JSON-serializable format
        members_list = [{
            'id': member.__getattribute__("id"),
            'name': member.__getattribute__("firstName") + " " + member.__getattribute__("lastName"),
            'email': member.__getattribute__("emailAddress")
        } for member in members]
        
        return jsonify({
            'success': True,
            'members': members_list
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/send-invitation/<int:member_id>', methods=['POST'])
def send_invitation(member_id):
    try:
        # Get the member object
        member = fab.get_member(member_id)
        
        # Send invitation
        response = member._requester.request(
            "POST",
            f"/members/{member_id}/invitation",
            _kwargs={},
        )
        
        return jsonify({
            'success': True,
            'message': f'Invitation sent successfully to member {member_id}'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico')

if __name__ == '__main__':
    app.run(debug=True)


    






