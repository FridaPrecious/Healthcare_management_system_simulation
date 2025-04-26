# --- Import necessary libraries ---
# Flask helps create web applications.
# Flask-JWT-Extended helps us handle authentication securely with tokens.
# Analogy: Flask is like our restaurant, and JWTs (tokens) are like access passes for customers to enter.
from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
import datetime

# --- Set up the Flask application ---
app = Flask(__name__)

# --- Configure JWT Authentication ---
# Secret key used to sign the tokens (must be kept secret in real apps).
# Example: Like the secret recipe for your restaurant's special dish.
app.config['JWT_SECRET_KEY'] = 'your-super-secret-key-here'

# Set how long the access token should last (1 hour here)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=1)

# Initialize JWT manager
jwt = JWTManager(app)

# --- In-memory "database" ---
# These are temporary lists acting as our database.
users = [{"username": "doctor1", "password": "admin123", "role": "doctor"}]
health_programs = []
clients = []
enrollments = []

# --- AUTHENTICATION ENDPOINTS ---

# Login Endpoint
# This endpoint allows a user (e.g., doctor) to log in and get a token.
@app.route('/api/login', methods=['POST'])
def login():
    # Get username and password from the request
    username = request.json.get("username")
    password = request.json.get("password")
    
    # Check if the user exists and password matches
    user = next((u for u in users if u["username"] == username and u["password"] == password), None)
    if not user:
        # If no user found, return error
        return jsonify({"error": "Invalid credentials"}), 401
    
    # If user is found, create an access token
    access_token = create_access_token(identity={
        "username": username,
        "role": user["role"]
    })
    # Return the access token
    return jsonify(access_token=access_token)

# --- PROTECTED ENDPOINTS ---

# 1. Create Health Program
# This endpoint allows only authenticated doctors to create health programs.
@app.route('/api/programs', methods=['POST'])
@jwt_required()  # Protect this endpoint with JWT
def create_program():
    # Get details of the logged-in user
    current_user = get_jwt_identity()
    # Only allow users with 'doctor' role to create programs
    if current_user["role"] != "doctor":
        return jsonify({"error": "Doctors only!"}), 403

    # Get the program data from the request
    data = request.json
    # Create a new program
    program = {
        "id": len(health_programs) + 1,
        "name": data.get("name"),
        "description": data.get("description")
    }
    # Add the program to the "database"
    health_programs.append(program)
    return jsonify(program), 201

# 2. Register Client
# This endpoint allows logged-in users to register a new client.
@app.route('/api/clients', methods=['POST'])
@jwt_required()  # Protect this endpoint
def register_client():
    data = request.json
    client = {
        "id": len(clients) + 1,
        "name": data.get("name"),
        "dob": data.get("dob"),
        "gender": data.get("gender")
    }
    clients.append(client)
    return jsonify(client), 201

# 3. Enroll Client in Program
# This endpoint allows logged-in users to enroll a client into a program.
@app.route('/api/enrollments', methods=['POST'])
@jwt_required()  # Protect this endpoint
def enroll_client():
    data = request.json
    enrollment = {
        "client_id": data.get("client_id"),
        "program_id": data.get("program_id"),
        "date": data.get("date")
    }
    enrollments.append(enrollment)
    return jsonify(enrollment), 201

# 4. Search Clients
# This endpoint allows logged-in users to search for clients by name.
@app.route('/api/clients', methods=['GET'])
@jwt_required()  # Protect this endpoint
def search_clients():
    name_query = request.args.get("name")
    results = [c for c in clients if name_query.lower() in c["name"].lower()] if name_query else clients
    return jsonify(results)

# 5. View Client Profile (with enrollments)
# This endpoint allows logged-in users to view a specific client and all their enrollments.
@app.route('/api/clients/<int:client_id>', methods=['GET'])
@jwt_required()  # Protect this endpoint
def view_client(client_id):
    client = next((c for c in clients if c["id"] == client_id), None)
    if not client:
        return jsonify({"error": "Client not found"}), 404
    
    client_enrollments = [e for e in enrollments if e["client_id"] == client_id]
    client["enrollments"] = client_enrollments
    return jsonify(client)

# --- Run the application ---
# This starts the server so we can access all the above APIs.
if __name__ == '__main__':
    app.run(debug=True)
