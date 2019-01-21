# Questioner

[![Build Status](https://travis-ci.com/tirgei/Questioner-API-V2.svg?branch=develop)](https://travis-ci.com/tirgei/Questioner-API-V2)
[![Coverage Status](https://coveralls.io/repos/github/tirgei/Questioner-API-V2/badge.svg?branch=develop)](https://coveralls.io/github/tirgei/Questioner-API-V2?branch=develop)
[![BCH compliance](https://bettercodehub.com/edge/badge/tirgei/Questioner-API-V2?branch=develop)](https://bettercodehub.com/)

Crowd-source questions for a meetup. Questioner helps the meetup organizer prioritize questions to be answered.

The project is managed using [Pivotal Tracker](https://www.pivotaltracker.com). You can view the board [here](https://www.pivotaltracker.com/n/projects/2235446).

The repo for the frontend is available at [Questioner](https://github.com/tirgei/Questioner)

The repo for the version 1 of the API is available at [Questioner-API](https://github.com/tirgei/Questioner-API)

## Prerequisites

- [VS Code](https://code.visualstudio.com)
- [Python 3.6](https://www.python.org)
- [Postgres](https://www.postgresql.org)
- [Insomnia](https://insomnia.rest) / [Postman](https://www.getpostman.com)

## Installation

- Clone the repo

```console
foo@bar:~$ git clone https://github.com/tirgei/Questioner-API.git
```

- Create the psql databases

```console
foo@bar:~$ createdb questioner_db
foo@bar:~$ createdb questioner_test_db
```

- CD into the folder

```console
foo@bar:~$ cd Questioner-API
```

- Create a virtual environment

```console
foo@bar:~$ python3 -m venv env
```

- Activate the virtual environment

```console
foo@bar:~$ source env/bin/activate
```

- Install dependencies

```console
foo@bar:~$ pip install -r requirements.txt
```

- Set the environment variables

```console
foo@bar:~$ mv .env.example .env
foo@bar:~$ source .env
```

- Run the tests

```console
foo@bar:~$ pytest --cov=app
```

- Run the app

```console
foo@bar:~$ flask run
```

## API Endpoints

#### User Endpoints

| **HTTP METHOD** | **URI** | **ACTION** |
| --- | --- | --- |
| **POST** | `/api/v2/auth/signup` | Register a new user |
| **POST** | `/api/v2/auth/login` | Login a user |
| **POST** | `/api/v2/refresh-token` | Refresh access token |
| **GET** | `/api/v2/profile/<int:user_id>` | Fetch a users profile |
| **POST** | `/api/v2/auth/logout` | Logout a user |

#### Meetup Endpoints

| **HTTP METHOD** | **URI** | **ACTION** |
| --- | --- | --- |
| **POST** | `/api/v2/meetups` | Create a new meetup |
| **GET** | `/api/v2/meetups` | Fetch all meetups |
| **GET** | `/api/v2/meetups/upcoming` | Fetch upcoming meetups in the next 1 week|
| **GET** | `/api/v2/meetups/<int:meetup_id>` | Fetch specific meetup |
| **POST** | `/api/v2/meetups/<int:meetup_id>/<string:rsvp>` | RSVP to a meetup |
| **GET** | `/api/v2/meetups/<int:meetup_id>/attendees` | Fetch list of attendees for a meetup|
| **PATCH** | `/api/v2/meetups/<int:meetup_id>/tags` | Add tags to a meetup|
| **DELETE** | `/api/v2/meetups/<int:meetup_id>` | Delete specific meetup |

#### Question Endpoints

| **HTTP METHOD** | **URI** | **ACTION** |
| --- | --- | --- |
| **POST** | `/api/v2/questions` | Post a question to a specific meetup |
| **GET** | `/api/v2/meetups/<int:meetup_id>/questions` | Fetch all questions for a meetup |
| **PATCH** | `/api/v2/questions/<int:question_id>/upvote` | Upvote a question |
| **PATCH** | `/api/v2/questions/<int:question_id>/downvote` | Downvote a question |

#### Comment Endpoints

| **HTTP METHOD** | **URI** | **ACTION** |
| --- | --- | --- |
| **POST** | `/api/v2/questions/<int:question_id>/comments` | Post a comment to a question |
| **GET** | `/api/v2/questions/<int:question_id>/comments` | Fetch all comments for a question |

## Libraries Used

- [Flask](http://flask.pocoo.org) - Python Microframework for backend solutions

- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/latest/) - Flask library for JWT 
implementation

- [Flask-RESTful](https://flask-restful.readthedocs.io) - Flask extension that adds support for building REST APIs

- [Marshmallow](https://marshmallow.readthedocs.io) - Framework for converting complex datatypes, such as objects, to and from native Python datatypes.

- [PEP-8](https://www.python.org/dev/peps/pep-0008/) - Style Guide for Python Code

- [Pytest](https://docs.pytest.org/en/latest/) - Framework for running Python tests

- [Pytest-cov](https://pytest-cov.readthedocs.io) - Plugin to produces coverage reports for Pytest

- [Psycopg2](http://initd.org/psycopg/) - Postgresql adapter for Python

- [Gunicorn](https://gunicorn.org) - Python HTTP server 

## Author

Vincent Kiptirgei - [Tirgei](https://tirgei.github.io)
