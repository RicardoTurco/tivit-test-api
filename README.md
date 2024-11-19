# Tivit Test Api
This is a simple test for python developer role

## Running

To run application locally:

```
a) Clone this project in your machine


b) To run / up application:

docker compose up


c) Access documentation/swagger of application:

http://0.0.0.0:8081/docs (on your browser)


d) To stop / down application:

CTRL + C
docker compose down
```

## Running (development)

To run application in development time:

```
a) Clone this project in your machine


b) Create a virtualenv, using version 3.12 of python:

poetry env use 3.12


c) Activate virtualenv:

poetry shell
(show the complete path of virtualenv)

obs: 
If name of virtualenv is not in prompt use the command:
- source <path_to_virtualenv>/bin/activate


d) Install dependencies:
(the name of virtualenv must be in prompt)

poetry install


e) Run ALL tests of application:

pytest -v


f) To run / up application:

poetry run python main.py


g) Access documentation/swagger of application:

http://0.0.0.0:8081/docs (on your browser)


h) To stop / down application:

CTRL + C
```

## Project Structure

Project structure (considering folder start in `tivit-test-api`):

```

├── tivit-test-api
│   ├── app
│   │   ├── __init__.py
│   │   ├── constants
│   │   │    ├── __init__.py 
│   │   │    ├── constants.py
│   │   ├── decorators
│   │   │    ├── __init__.py 
│   │   │    ├── decorators.py
│   │   ├── repositories
│   │   │    ├── __init__.py 
│   │   │    ├── fake_user_repository.py
│   │   ├── routes
│   │   │    ├── __init__.py
│   │   │    ├── v1
│   │   │    │   ├── __init__.py 
│   │   │    │   ├── admin.py
│   │   │    │   ├── get_token.py
│   │   │    │   ├── health_check.py
│   │   │    │   ├── user.py
│   │   ├── schemas
│   │   │    ├── __init__.py 
│   │   │    ├── token.py
│   │   ├── services
│   │   │    ├── __init__.py 
│   │   │    ├── tivit_fake_service.py
│   ├── tests
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── routes
│   │   │    ├── __init__.py
│   │   │    ├── v1
│   │   │    │   ├── __init__.py 
│   │   │    │   ├── test_admin.py
│   │   │    │   ├── test_get_token.py
│   │   │    │   ├── test_user.py
├── .gitignore
├── docker-compose.yaml
├── Dockerfile
├── main.py
├── poetry.lock
├── pyproject.toml
├── README.md
├── urls.py

```

### Main folders

* `tivit-test-api` - "Main" folder of project.
* `app` - All the RESTfull API implementation is here.
* `app/routes/v1` - "Routes" module of project (v1 endpoints).
* `app/services` - "Services" module of project (Services).
* `tests` - All tests of application.

### Files

* `.gitignore` - Lists files and directories which should not be added to git repository.
* `docker-compose.yaml` - To UP application locally.
* `Dockerfile` - Build a image from project.
* `main.py` - The Application entrypoint.
* `poetry.lock` - Define specific versions of dependencies.
* `pyproject.toml` - Some configurations of project.
* `README.md` - Instructions and information to run this project locally.
* `urls.py` - Declare all resource routes of project.
