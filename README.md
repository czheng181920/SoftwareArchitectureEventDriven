# SoftwareArchitecture

Software Architecture Assignment 1(Team 3)

# Setup

run this to set up the database (have to change python3 to python if that is what you are using)

`python3 db.py`

# Running CLI

You can run the CLI by typing these commands in the terminal.

Run the cli.py file and follow commands as shown.

`python3 cli.py`

# Running Frontend(Flask)

First cd into the Presentation Layer
`cd Presentation_Layer`

run python virtual environment
`python3 -m venv .venv `
`. .venv/bin/activate`

Then, make sure you have the required packages downloaded

If you don't, then do this:
`pip install -r requirements.txt`

To run the frontend:
`flask run`
or if that doesn't work, the following will always run the server
`python app.py`

Then you should get something like this:

- Debug mode: off
  WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
- Running on http://127.0.0.1:5000
  Press CTRL+C to quit

Copy and paste the http link to your web browser to see web app

# Running either the business layer or data layer server

First cd into the correct folder
`cd`

run python virtual environment
`python3 -m venv .venv `
`. .venv/bin/activate`

Then, make sure you have the required packages downloaded

If you don't, then do this:
`pip install -r requirements.txt`

To run the frontend:
`flask run`
or if that doesn't work, the following will always run the server
`python app.py`

# Updating the requirements.txt

If you add a package to a server, you can update the dependencies by doing this:
`pip freeze > requirements.txt`

# Running Business layer and database later

In one machine (the Database Layer machine):
`cd Data_Layer`
`python3 -m venv .venv `
`. .venv/bin/activate`
`pip install -r requirements.txt`
`flask run`
Once you have the server running, flask should print the IP address and port of the server to the terminal.
Save this IP address for the Business Layer

In a second machine (the Business Layer machine):
paste the IP address in Business_Layer/app.py in the correct spot. It should look like this:

`DATA_LAYER_URL = 'http://xxx.xxx.xxx.xxx:5002/store'`
Then run the business layer server
`cd Business_Layer`
`python3 -m venv .venv `
`. .venv/bin/activate`
`pip install -r requirements.txt`
`flask run`

# Business layer integration test

You can test that the business layer and the data layer is set up by using this integration test.
Follow the steps above to set up the business layer and the data layer.
Then in a separate terminal:
`cd Business_Layer`
`. .venv/bin/activate`
`python -m unittest test_app.py`


# Hosting Each MicroService(Part 3) 
You must host each microservice before running the application

Hosting the Presentation Layer:
`cd Presentation_Layer` 
`python3 -m venv .venv`
`. .venv/bin/activate`

CLI Hosting:
`python3 cli.py`

Website Hosting:
`flask run`


Hosting the API Gateway:
`cd Business_Layer` 
`python3 -m venv .venv`
`. .venv/bin/activate`
`cd API_Gateway`
`python3 app.py`

Hosting the Meetings_Calendar Microservice:
`cd Business_Layer` 
`python3 -m venv .venv`
`. .venv/bin/activate`

`cd Meetings_Calendars`
`python3 app.py`

Hosting the Participants Microservice:
`cd Business_Layer` 
`python3 -m venv .venv`
`. .venv/bin/activate`

`cd Participants`
`python3 participantsApp.py`

Hosting the Attachments Microservice:
`cd Business_Layer` 
`python3 -m venv .venv`
`. .venv/bin/activate`

`cd Attachments`
`python3 attachmentsApp.py`


