# Healthcare_management_system_simulation

How to run and test the simulation.

You can test the system in two ways:

Test the APIs using Postman.
Alternatively, run the index.html file in a browser (if you built a frontend).


Make sure your Flask server is running:
Run the command: python app.py
By default, it will run at:http://127.0.0.1:5000

We can now test the APIs by running thr following commands in our bash i.e TESTING USING POSTMAN

CREATING A PROGRAM
curl -X POST http://127.0.0.1:5000/api/programs \
-H "Content-Type: application/json" \
-d '{"name":"HIV", "description":"HIV Treatment"}'

REGISTERING CLIENTS

curl -X POST http://127.0.0.1:5000/api/clients \
-H "Content-Type: application/json" \
-d '{"name":"Precious", "dob":"2003-11-29", "gender":"Female"}'

ENROLLING CLIENTS
curl -X POST http://127.0.0.1:5000/api/enrollments \
-H "Content-Type: application/json" \
-d '{"client_id":1, "program_id":1, "date":"2025-04-26"}'

SEARCHING CLIENTS
curl http://127.0.0.1:5000/api/clients?name=Precious

VIEWING CLIENT PROFILE
curl http://127.0.0.1:5000/api/clients/1

WORKING OF AUTHENTICATION
We first login to get the token through the command

curl -X POST http://127.0.0.1:5000/api/login \
-H "Content-Type: application/json" \
-d '{"username":"doctor1", "password":"admin123"}'

# Response: {"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}

ACCESSING PROTECTED ENDPOINTS
curl -X POST http://127.0.0.1:5000/api/programs \
-H "Content-Type: application/json" \
-H "Authorization: Bearer eyJhbGci..." \
-d '{"name":"HIV", "description":"HIV Treatment Program"}'



Important Notes
Always login first to get the access token when accessing protected routes.

The server must be running locally at http://127.0.0.1:5000 for the commands to work.

Remember to use the correct Authorization Bearer token after login for protected endpoints.

🙏 Thank you for using Healthcare Management System Simulation!
