# FastAPI Learning Project 🚀

A hands-on project to learn **FastAPI and Python backend development** by building a structured REST API application.

I am primarily coming from a **.NET / C# background**, so this project is also helping me understand how familiar backend concepts such as routing, validation, services, exception handling, and dependency injection are implemented in the Python ecosystem.

## GitHub Repository

https://github.com/sacgaikwad/fastapi-learning

---

# Project Structure

```text
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
```

---

# Architecture

The project currently follows a simple layered architecture:

```text
                    Client
                      │
                      │ HTTP Request
                      ▼
                ┌─────────────┐
                │   Router    │
                └──────┬──────┘
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
```

## Router

`APIRouter` is used to organize and group related API endpoints.

It is conceptually similar to a **Controller** in ASP.NET Core.

Example:

```python
@router.post("")
def create_user(user: UserRequest):
    return user_service.create_user(user)
```

Current routers:

- `user.py` - User-related APIs
- `product.py` - Product-related APIs

## Service Layer

The service layer contains business logic and keeps it separate from the API routes.

Current services:

- `user_service.py` - User-related business logic
- `product_service.py` - Product-related business logic

Example:

```text
Router
   │
   ├── User API
   │      ↓
   │  user_service.py
   │
   └── Product API
          ↓
      product_service.py
```

This is similar to the Service Layer commonly used in .NET applications.

---

# Models

The project uses **Pydantic** models for request and response data.

Example:

```python
class UserRequest(BaseModel):
    name: str
    age: int
    email: EmailStr
```

Pydantic is used for:

- Request validation
- Response models
- Type validation
- Custom field validation

Example custom validation:

```python
@field_validator("age")
@classmethod
def validate_age(cls, value):
    if value <= 18:
        raise ValueError("Age must be greater than 18")

    return value
```

---

# Exception Handling

Custom exceptions are separated from the routers and services.

```text
exceptions/
├── user.py
└── handlers.py
```

A service or router can raise a custom exception:

```python
raise UserNotFoundException(user_id)
```

The FastAPI application then uses an exception handler to convert the exception into an appropriate HTTP response.

```text
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
```

---

# API Endpoints

## Users

| Method | Endpoint | Description |
|---|---|---|
| GET | `/users/{user_id}` | Get user |
| POST | `/users` | Create user |
| DELETE | `/users/{user_id}` | Delete user |

## Products

Product-related endpoints are implemented through:

```text
Product Router
      ↓
Product Service
```

---

# Prerequisites

Before running the project, make sure the following are installed:

- Python 3.10+
- pip
- Git
- VS Code (recommended)

Verify the installations:

```powershell
python --version
pip --version
git --version
```

---

# Getting Started

## 1. Clone the repository

```powershell
git clone https://github.com/sacgaikwad/fastapi-learning.git
```

## 2. Navigate to the project

```powershell
cd fastapi-learning
```

## 3. Create a virtual environment

```powershell
python -m venv .venv
```

## 4. Activate the virtual environment

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

After activation, you should see something similar to:

```text
(.venv) PS D:\Learning\Python\fastapi-learning>
```

## 5. Install dependencies

```powershell
pip install -r requirements.txt
```

## 6. Run the application

From the project root:

```powershell
python -m app.main
```

Alternatively, run the application directly using Uvicorn:

```powershell
uvicorn app.main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

---

# Swagger Documentation

FastAPI automatically generates interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI allows you to:

- View available APIs
- View request models
- View response models
- Test APIs directly from the browser
- See HTTP status codes
- Explore validation errors

---

# ReDoc

FastAPI also provides ReDoc documentation.

Open:

```text
http://127.0.0.1:8000/redoc
```

---

# OpenAPI Specification

The generated OpenAPI specification is available at:

```text
http://127.0.0.1:8000/openapi.json
```

---

# Running the Application Flow

```text
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
Test APIs
```

---

# Stop the Application

Press:

```text
CTRL + C
```

to stop the development server.

---

# Deactivate Virtual Environment

When finished:

```powershell
deactivate
```

---

# Technologies

- Python
- FastAPI
- Uvicorn
- Pydantic
- Git
- VS Code

---

# .NET vs FastAPI

Coming from a .NET background, some of the architecture feels familiar.

| ASP.NET Core | FastAPI |
|---|---|
| Controller | APIRouter |
| Action Method | Route Function |
| DTO | Pydantic Model |
| Model Validation | Pydantic Validation |
| Service | Service |
| Repository | Repository |
| Middleware | Middleware |
| Dependency Injection | `Depends()` |
| Kestrel | Uvicorn |

The implementation is different, but the overall backend architectural concepts are quite similar.

---

# Learning Progress

This project is being developed incrementally while learning FastAPI.

## Completed

- [x] FastAPI application
- [x] Uvicorn
- [x] GET APIs
- [x] POST APIs
- [x] DELETE APIs
- [x] APIRouter
- [x] Project/package structure
- [x] `__init__.py`
- [x] Pydantic request models
- [x] Pydantic response models
- [x] Model validation
- [x] Custom email validation
- [x] HTTP status codes
- [x] Custom exceptions
- [x] Custom exception handlers
- [x] Service layer
- [x] User service
- [x] Product service
- [x] Swagger / OpenAPI

## Next Topics

- [ ] Dependency Injection
- [ ] `Depends()`
- [ ] Database integration
- [ ] Repository pattern
- [ ] Async APIs
- [ ] Authentication and Authorization
- [ ] Middleware
- [ ] Configuration management
- [ ] Testing
- [ ] Production deployment

---

# Goal

The goal of this project is to learn FastAPI from the fundamentals and gradually build a production-style Python REST API architecture.

Rather than only following tutorials, I am building the project incrementally and documenting the concepts as I learn them.

---

# Learning Approach

```text
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
```

Still learning, still experimenting, and adding to the project step by step. 🚀
