# Gunicorn - Falcon Simple Rest API ( Word Replace )

Building a Falcon Rest API using Gunicorn to replace word(s) based on provided dictionary. Functionality of the API is limited. API has these following endpoints:

 * /health - Checks if the application is running
 * /login - Validates username and password to provide token for 'replace' api call.
 * /replace - replace user input based on provided word map


## Running the Application

### Requirements

1. Python >= 3.8
2. Required python libraries [0]
3. Database ( Can be SQLite, Postgresql, MySQL, Oracle, MS-SQL, Firebird )
4. This API doesnt require any persistent volume. 


### Running the Application

To deploy and run the application on your laptop, you can use sqlite db as a database.
For production we highly recommend not to use sqlite.

Make sure that pip3 exists by executing
  pip3 --version

Creating a Virtual Environment
  python3 -m venv env

Activating a Virtual Environment
  source env/bin/activate

To confirm you're in the virtual environment by cheking the location of Python interpreter
  which python
  .../env/bin/python

To install requirements to your environment 
  pip(3) install -r requirements.txt

Create user in database
 User password should be hashed by running:
   hashed_password = sha256_crypt.hash("password")
   insert into users VALUES(0, 'user01', '{hashed_password}', 'example_user01@example.com', True);


We're ready to run the API service. Before running the service you may need to check configuration file [./config/config.yml]

## Testing the Application

We can start checking API by calling health endpoint
 --request GET --data '{"health-check":"True"}' 127.0.0.1:{gunicorn.bind.port}/{path_prefix}/health

 Excepted result

 {
   "error": "0",
   "message": "Everything seems fine"
 } 

To request jwt token. (To change jwt token expire limit ( Elapse_time) check configuration file)

  --header "Content-Type: application/json" --request POST --data '{"user_id":"{my_user_id}", "password": "{password}"}' http://127.0.0.1:{gunicorn.bind.port}/{path_prefix}/login

  Excepted result

  {
    "Elapse_time": "10",
    "error": "0",
    "message": "Succesful",
    "x-auth": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VReTgk4joiQXljYSIsImV4cdkfgtExNTMxNjM1N30.WcjvvB6uE-2zHIbH6FJg4yi0A43al-Vp6ydQIloJrEI"
  }

To Call replace API service we will use jwt token generated before. 

  --header "X-AUTH: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VReTgk4joiQXljYSIsImV4cdkfgtExNTMxNjM1N30.WcjvvB6uE-2zHIbH6FJg4yi0A43al-Vp6ydQIloJrEI" --request GET --data '{"value":"Hello Google"}' http://127.0.0.1:{gunicorn.bind.port}/{path_prefix}/replace

  Excepted result

  {
    "error": "0",
    "value": "Hello Google©"
  }

[0] requirements.txt
