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


b) IMPORTANT: Set your version of Python to 3.12.0


c) Run setup command:

- Make setup

OBS:

If not create a virtualenv using the correct version of Python, you can create it manually: 

- poetry env use 3.12
- poetry shell (show the complete path of virtualenv)
- source <path_to_virtualenv>/bin/activate (If name of virtualenv is not in prompt use the command)


d) Install dependencies:

- make install


e) Run ALL tests of application:

- make test

OBS: 

You can also generate the COVERAGE report of tests:

- make test-cov-rep


f) To run / up application:

- make run


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

## LINTERS

This project has a some LINTERs to mantain the quality of code.

### Coverage

To check the COVERAGE of tests of project, is possible execute the follow command:

```
make test-cov
```

To view more details about the COVERAGE, just run the command:

```
make test-cov-rep
```

This will create a folder 'htmlcov' and one file '.coverage' (they should be included in '.gitignore' file). Inside of folder 'htmlcov', just open the 'index.html' file in your browser to view details about the COVERAGE.

To delete the folder and file created, just run command:

```
make clean
```

## Black

Formats the code according to [PEP-8](https://peps.python.org/pep-0008/) standards.

```
black --check . (displays which files need adjustments in code formatting);
black --check --diff <path_to_file> (displays the necessary code formmating changes in a SPECIFIC file - manual adjust);
black . (performs code formatting "automatically" in ALL files);
black <path_to_file> (performs code formatting "automatically" in a SPECIFIC file);
```

## Isort

Performs adjustments in "imports" of project - [ISORT](https://pycqa.github.io/isort/).

```
isort --check . (displays wich files need adjustments in imports);
isort --check --diff <path_to_file> (displays the necessary adjustments in imports in a SPECIFIC file - manual adjust);
isort . (performs adjustments in imports "automatically" in ALL files);
isort <path_to_file> (performs adjustments in imports "automatically" in a SPECIFIC file);
```
