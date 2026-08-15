FastAPI Learning Project 🚀

A hands-on project to learn FastAPI and Python backend development
by building a structured REST API application.

I am primarily coming from a .NET / C# background, so this project
is also helping me understand how familiar backend concepts such as
routing, validation, services, exception handling, dependency injection,
authentication, and authorization are implemented in the Python
ecosystem.

GitHub Repository

https://github.com/sacgaikwad/fastapi-learning

Project Structure

fastapi-learning/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── product.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── error.py
│   │
│   ├── exceptions/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── handlers.py
│   │
│   ├── dependencies/
│   │   ├── auth.py
│   │   └── user.py
│   │
│   └── services/
│       ├── __init__.py
│       ├── user_service.py
│       └── product_service.py
│
├── tests/
│   ├── __init__.py
│   └── test_user.py
│
├── .gitignore
├── requirements.txt
└── README.md

Architecture

The project follows a simple layered architecture:

                    Client
                      │
                      │ HTTP Request
                      ▼
                ┌─────────────┐
                │   Router    │
                └──────┬──────┘
                       │
                       │ Depends()
                       ▼
              Authentication
                       │
                       ▼
                ┌─────────────┐
                │   Service   │
                └──────┬──────┘
                       │
                       ▼
                 Business Logic
                       │
                       ▼
                    Database

Router

APIRouter is used to organize and group related API endpoints.

It is conceptually similar to a Controller in ASP.NET Core.

Service Layer

The service layer contains business logic and keeps it separate from the
API routes.

This is similar to the Service Layer commonly used in .NET applications.

Dependency Injection

FastAPI provides dependency injection through Depends().

Example:

def get_user(
    user_id: int,
    current_user_id: int = Depends(get_current_user),
    service=Depends(get_user_service)
):
    return service.get_user(user_id)

Dependencies are resolved by FastAPI before the route function executes.

Current dependency examples:

get_current_user - JWT authentication

get_user_service - User service dependency

Models

The project uses Pydantic models for request and response data.

Example:

class UserRequest(BaseModel):
    name: str
    age: int
    email: EmailStr

Pydantic is used for:

Request validation

Response models

Type validation

Custom field validation

Exception Handling

Custom exceptions are separated from the routers and services.

exceptions/
├── user.py
└── handlers.py

A service or router can raise a custom exception:

raise UserNotFoundException(user_id)

The FastAPI application then uses an exception handler to convert the
exception into an appropriate HTTP response.

Service
   │
   │ raise exception
   ▼
Custom Exception
   │
   ▼
Exception Handler
   │
   ▼
HTTP Response

JWT Authentication

JWT authentication has been added to the project to protect user APIs.

The authentication flow is:

              POST /users/login
                      │
                      ▼
             Validate credentials
                      │
                      ▼
             Create JWT Token
                      │
                      ▼
                Access Token
                      │
                      ▼
      Authorization: Bearer <JWT>
                      │
                      ▼
             get_current_user()
                      │
                      ▼
                 jwt.decode()
                      │
              ┌───────┴────────┐
              │                │
            Valid            Invalid
              │                │
              ▼                ▼
       current_user_id        401
              │
              ▼
        Protected API

Creating the JWT

The access token contains the authenticated user's ID in the sub claim
and an expiration time.

Example:

payload = {
    "sub": str(user_id),
    "exp": expire
}

return jwt.encode(
    payload,
    SECRET_KEY,
    algorithm=ALGORITHM
)

The token is signed using the configured SECRET_KEY and ALGORITHM.

Getting the Current User

The project uses a FastAPI dependency to extract and validate the Bearer
token:

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    )
):
    token = credentials.credentials

    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

    return int(user_id)

The dependency returns the ID of the authenticated user.

Protecting an Endpoint

An endpoint becomes authenticated by adding:

current_user_id: int = Depends(get_current_user)

Example:

@router.get(
    "/{user_id}",
    response_model=UserDetailResponse
)
def get_user(
    user_id: int,
    current_user_id: int = Depends(get_current_user),
    service=Depends(get_user_service)
):
    return service.get_user(user_id)

FastAPI executes get_current_user() before executing get_user().

If the JWT is missing or invalid, the request is rejected and the route
function is not executed.

Authentication vs Authorization

Authentication answers:

Who are you?

The JWT dependency identifies the current user:

JWT
 ↓
get_current_user()
 ↓
current_user_id

Authorization answers:

What are you allowed to do?

Authorization/role checks have not yet been implemented. The next
step is to add authorization rules such as ownership and role-based
access.

API Endpoints

Users

Method   Endpoint             Authentication

GET      /users/{user_id}   Required
POST     /users             Required
DELETE   /users/{user_id}   Required
PUT      /users/{user_id}   Required
POST     /users/login       Not required

The login endpoint is public because a user must obtain a JWT before
accessing protected endpoints.

Products

Product-related endpoints are implemented through:

Product Router
      ↓
Product Service

Authentication Request Flow

Example protected request:

DELETE /users/10
Authorization: Bearer <access_token>

The request passes through:

HTTP Request
     │
     ▼
HTTPBearer
     │
     ▼
get_current_user()
     │
     ▼
Extract Bearer Token
     │
     ▼
jwt.decode()
     │
     ▼
current_user_id
     │
     ▼
delete_user()

Swagger Documentation

FastAPI automatically generates interactive API documentation.

Open:

http://127.0.0.1:8000/docs

Swagger UI allows you to:

View available APIs

View request models

View response models

Test APIs directly from the browser

Test authenticated APIs using a Bearer token

See HTTP status codes

Explore validation errors

ReDoc

FastAPI also provides ReDoc documentation.

Open:

http://127.0.0.1:8000/redoc

OpenAPI Specification

The generated OpenAPI specification is available at:

http://127.0.0.1:8000/openapi.json

Prerequisites

Before running the project, make sure the following are installed:

Python 3.10+

pip

Git

VS Code (recommended)

Verify the installations:

python --version
pip --version
git --version

Getting Started

1. Clone the repository

git clone https://github.com/sacgaikwad/fastapi-learning.git

2. Navigate to the project

cd fastapi-learning

3. Create a virtual environment

python -m venv .venv

4. Activate the virtual environment

For Windows PowerShell:

.venv\Scripts\Activate.ps1

5. Install dependencies

pip install -r requirements.txt

6. Run the application

python -m app.main

Alternatively:

uvicorn app.main:app --reload

The application will be available at:

http://127.0.0.1:8000

Running the Application Flow

Clone Repository
       ↓
Create Virtual Environment
       ↓
Activate Virtual Environment
       ↓
Install Dependencies
       ↓
Run FastAPI Application
       ↓
Open Swagger
       ↓
Login
       ↓
Get JWT
       ↓
Authorize Protected APIs
       ↓
Test APIs

Stop the Application

Press:

CTRL + C

to stop the development server.

Deactivate Virtual Environment

When finished:

deactivate

Technologies

Python

FastAPI

Uvicorn

Pydantic

PyJWT

Git

VS Code

.NET vs FastAPI

Coming from a .NET background, some of the architecture feels familiar.

ASP.NET Core                        FastAPI

Controller                          APIRouter
Action Method                       Route Function
DTO                                 Pydantic Model
Model Validation                    Pydantic Validation
Service                             Service
Repository                          Repository
Middleware                          Middleware
Dependency Injection                Depends()
Authentication Middleware/Handler   Security Dependencies
JWT Authentication                  JWT + FastAPI Security
Kestrel                             Uvicorn

The implementation is different, but the overall backend architectural
concepts are quite similar.

Learning Progress

This project is being developed incrementally while learning FastAPI.

Completed

FastAPI application

Uvicorn

GET APIs

POST APIs

DELETE APIs

PUT APIs

APIRouter

Project/package structure

__init__.py

Pydantic request models

Pydantic response models

Model validation

Custom email validation

HTTP status codes

Custom exceptions

Custom exception handlers

Service layer

User service

Product service

Dependency Injection

Depends()

JWT access token generation

Bearer token authentication

get_current_user dependency

Protected user endpoints

Swagger / OpenAPI

Login endpoint

Next Topics

Authorization

Role-based authorization

Ownership-based authorization

Database integration

Repository pattern

Async APIs

Middleware

Configuration management

Testing

Production deployment

Goal

The goal of this project is to learn FastAPI from the fundamentals and
gradually build a production-style Python REST API architecture.

Rather than only following tutorials, I am building the project
incrementally and documenting the concepts as I learn them.

Learning Approach

Learn a Concept
      ↓
Implement It
      ↓
Understand the Architecture
      ↓
Add It to the Project
      ↓
Document It
      ↓
Move to the Next Concept

Still learning, still experimenting, and adding to the project step by
step. 🚀