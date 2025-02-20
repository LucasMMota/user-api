# User CRUD API

This is a Flask-based API example project that uses a modular architecture 
(with similar approaches to the FastAPI) to organize code into separate layers 
(models, repositories, services, schemas, etc.). 

Below you will find an overview of each directory and file, including guidance on how 
to set up and run this project.

### Project Structure Overview

```
user-api/
├── app/
│   ├── api/                          # API endpoint definitions and versioning
│   │   └── v1/
│   │       └── routes/
│   │           └── user.py           # Defines HTTP endpoints for user operations (GET/POST/PUT/DELETE)
├── core/                            # Core code used on API
│   └── database/
│       └── database.py              # Handles the SQLAlchemy engine, manages sessions, and initializes the DB;
│                                      supports both SQLite and PostgreSQL configurations
├── models/
│   ├── base_model.py                # Defines the common SQLAlchemy declarative base for all models
│   └── user_model.py                # Defines the User model representing a "User" in the database
├── repositories/
│   ├── base_repository.py           # Generic repository foundation for handling common operations and session handling,
│   |                                  with Pydantic validation of database responses
│   └── user_repository.py           # Logic for interacting with the "User" entity in the database
├── schemas/
│   └── user_schema.py               # Defines the Pydantic schema for User data serialization/deserialization;
│                                      enables conversion of ORM objects to response models via from_orm  with pydantic 
|                                      schema enforcing                                    
├── services/
│   └── user_service.py              # Houses business logic and workflows for User operations,
│                                      coordinating between repositories and schema validation
├── main.py                          # The main entry point for launching the application
├── settings.py                      # Central configuration settings (e.g. for DB credentials, API keys)
├── logger.py                        # Sets up standardized logging for the application
├── user_api_db.db                   # SQLite database file for local development/testing
├── README.md                        # This README documentation file
└──  Makefile                         # Contains automation tasks (e.g., build enviroment, run tests, instal requirements)
````

## 1. Setup enviroment

At the bare minimum you'll need the following for your development
environment:

1. [Python 3.11.9](http://www.python.org/)


It is strongly recommended to also install and use [pyenv](https://github.com/pyenv/pyenv) with virtualenv for managing 
Python virtual environments, you can install here:

 - [pyenv-installer](https://github.com/pyenv/pyenv-installer)

This tool eases the burden of dealing with virtualenvs and having to activate and deactivate'em by hand. Once you run 
`pyenv local my-project-venv` the directory you're in will be bound to the `my-project-venv` virtual environment and 
then you will have never to bother again activating the correct venv.

### Getting Started

   a) Clone the repository:
  
      git clone https://github.com/LucasMMota/user-api.git
      cd user-api

   b) Create and activate a virtual environment:
      `make enviroment`

   c) Install dependencies:
      `make dependencies`

--------------------------------------------------------------------------------

## 3. Start the application

   - On root, run flask project by following command:
    
    flask --app app/core/main.py

You can typically run the project by executing the command above. But if find issue on running flask command, you may use: `python -m flask --app app/core/main.py` 
     
   - The API would be served at:
       http://127.0.0.1:5000/

--------------------------------------------------------------------------------

## 4. Main Components

   4.1 Models (models/)

       - Contains Python classes that represent the data structures used by the application. 
       - base_model.py: Defines the common base class (SQLAlchemy declarative base).
       - user_model.py: Defines User model representing a "User" in the database.

   4.2 Repositories (repositories/)

       - Encapsulates data access logic in database for models.
       - base_repository.py: A generic repository foundation for repositories extend. Handles session and 
         db response validation with pydantic.
       - user_repository.py: The logic for interacting with the "User" entity from database.

   4.3 Schemas (schemas/)

       - Used to enforce enetities schema and serialize/deserialize data. Helps converting database 
         objects into response models without manually serializing each field. 
       - user_schema.py: Defines "User" schema.

   4.4 Services (services/)

       - Houses business logic or application-level workflows.
       - user_service.py: Orchestrates "User" operations, calling repositories 
         and applying business rules.

   4.5 Routes (app/api/v1/routes/)

       - Defines the HTTP endpoints (FastAPI routes).
       - user.py: Handles user-related endpoints (GET/POST/PUT/DELETE).

   4.6 Database (core/database/)

       - Manages database engine creation and initialization.
       - database.py: Builds a SQLAlchemy engine, handles session management, 
         and db initialization on start up. Works with Sqlit and Postgress.

   4.7 Logger (logger.py)

       - Utility set up for standardized logging throughout the application.

--------------------------------------------------------------------------------

## 5. Database Files

   - user_api_db.db, users.db:
     These are SQLite database files likely used for local development.

--------------------------------------------------------------------------------

## 6. Testing

   - The application automated tests.
   - Run command:
       
    pytest

--------------------------------------------------------------------------------

## 7. Makefile

   - Makefile holds automatted commands that may be run via `make alias`. Example:

    make enviroment # for creating an environment in this project using pyenv and virtualenv 
