# Gunicorn - Falcon Simple Rest API ( Word Replace )

Building a Falcon Rest API using Gunicorn to replace word(s) based on provided dictionary. Functionality of the API is limited. API has these following endpoints:

 * /health - Checks if the application is running - Supports GET requests
 * /login - Validates username and password to provide token for 'replace' api call. - Supports POST requests
 * /replace - replace user input based on provided word map - Supports POST requests


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
```
pip3 --version
```

Creating a Virtual Environment
```
python3 -m venv env
```

Activating a Virtual Environment
```
source env/bin/activate
```

To confirm you're in the virtual environment by cheking the location of Python interpreter
```
which python
.../env/bin/python
```

To install requirements to your environment
```
pip(3) install -r requirements.txt
```

We're ready to run the API service. Before running the service you may need to check configuration file [./config/config.yml]

## Testing the Application

We can start checking API by calling health endpoint

```
 --request POST --data '{"health-check":"True"}' 127.0.0.1:{gunicorn.bind.port}/{path_prefix}/health
```

Excepted result

```
 {
   "error": "0",
   "message": "Everything seems fine"
 }
```

To request jwt token. (To change jwt token expire limit ( Elapse_time) check configuration file)

```
  --header "Content-Type: application/json" --request POST --data '{"user_id":"{my_user_id}", "password": "{password}"}' http://127.0.0.1:{gunicorn.bind.port}/{path_prefix}/login
```

Excepted result

```
  {
    "Elapse_time": "10",
    "error": "0",
    "message": "Succesful",
    "x-auth": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VReTgk4joiQXljYSIsImV4cdkfgtExNTMxNjM1N30.WcjvvB6uE-2zHIbH6FJg4yi0A43al-Vp6ydQIloJrEI"
  }
```

To Call replace API service we will use jwt token generated before. 

```
  --header "X-Auth-Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VReTgk4joiQXljYSIsImV4cdkfgtExNTMxNjM1N30.WcjvvB6uE-2zHIbH6FJg4yi0A43al-Vp6ydQIloJrEI" --request POST --data '{"value":"Hello Lorem"}' http://127.0.0.1:{gunicorn.bind.port}/{path_prefix}/replace
```

  Excepted result

```
  {
    "error": "0",
    "value": "Hello Lorem©"
  }
```

## Environment Variables

# Database Specific Environment Variables
```
$DATABASE_ENGINE (Default:sqlite): Possible values; sqlite, mysql, postgresql
$DATABASE_HOST: (Default:127.0.0.1)
$DATABASE: Required (if DATABASE_ENGINE is sqlite then this should be full path of sqlite file without extension(.db))
$DATABASE_USERNAME: Required if DATABASE_ENGINE is not sqlite
$DATABASE_PASSWORD: Required if DATABASE_ENGINE is not sqlite
```

# Gunicorn Specific Environment Variables
```
$GUNICORN_WORKERS (Default:2): The number of worker processes. This number should generally be between 2-4 workers per core in the server.
$GUNICORN_BIND_PORT (Default:8080)
$GUNICORN_TIMEOUT (Default:30): Workers silent for more than this many seconds are killed and restarted.
```

# App Specific Environment Variables
```
$APP_PATH_PREFIX (Default:/): Root Path which is api will be served
$APP_ENVIRONMENT (Default:Test): Possible values; Test, Staging, Prod (For now only it affects logging level)
```

# Auth Specific Environment Variables
```
$AUTH_SECRET_KEY (Default:my-secret-key): This will be used as salt string value in app
$AUTH_JWT_EXPIRE_LIMIT (Default:30): Number of minutes before generated json expire. you'll have an access token, that's valid for {AUTH_JWT_EXPIRE_LIMIT} minutes
```

[0] requirements.txt
