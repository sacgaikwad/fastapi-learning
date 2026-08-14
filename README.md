# FastAPI Learning Project 🚀

A hands-on project to learn **FastAPI and Python backend development** by building a structured REST API application.

I am primarily coming from a **.NET / C# background**, so this project is also helping me understand how familiar backend concepts such as routing, validation, services, dependency injection, repositories, database access, exception handling, and authentication are implemented in the Python ecosystem.

The goal is not just to build APIs, but to understand **how the different backend components work together**.

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
│   ├── core/
│   │   ├── __init__.py
│   │   ├── logging.py
│   │   └── security.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   ├── init_db.py
│   │   │
│   │   └── models/
│   │       ├── __init__.py
│   │       └── user.py
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
│   │   ├── __init__.py
│   │   └── user.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── user_repository.py
│   │
│   └── services/
│       ├── __init__.py
│       ├── user_service.py
│       └── product_service.py
│
├── data/
│   └── app.db
│
├── tests/
│   ├── __init__.py
│   └── test_user.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

> The project structure will continue to evolve as new concepts are introduced.

---

# Architecture

The project currently follows a layered architecture:

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
                ┌─────────────┐
                │ Repository  │
                └──────┬──────┘
                       │
                       ▼
                 SQLAlchemy
                       │
                       ▼
                Database Session
                       │
                       ▼
                     SQLite
```

This architecture is intentionally similar to patterns commonly used in .NET applications.

---

# Router Layer

`APIRouter` is used to organize and group related API endpoints.

It is conceptually similar to a **Controller** in ASP.NET Core.

Example:

```python
@router.get(
    "/{user_id}",
    response_model=UserDetailResponse
)
def get_user(
    user_id: int,
    service=Depends(get_user_service)
):
    return service.get_user(user_id)
```

Current routers:

- `user.py` - User-related APIs
- `product.py` - Product-related APIs

---

# Service Layer

The service layer contains business logic and keeps it separate from the API routes.

Current services:

- `user_service.py`
- `product_service.py`

Example:

```text
Router
   │
   ▼
UserService
   │
   ▼
UserRepository
```

The service layer does not directly deal with SQLAlchemy queries.

---

# Repository Layer

The repository layer is responsible for database operations.

The User Repository currently handles:

- Create
- Read
- Update
- Delete
- Database queries
- Transactions
- Rollback
- Database-related logging

Example:

```python
user = (
    self.db
    .query(User)
    .filter(User.id == user_id)
    .first()
)
```

This keeps database-specific logic separate from business logic.

---

# Dependency Injection

FastAPI's `Depends()` is used for dependency injection.

Example:

```python
def get_user_service(
    repository: UserRepository = Depends(get_user_repository)
):
    return UserService(repository)
```

Database sessions are also injected:

```python
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
```

Current dependency flow:

```text
Router
   │
   ▼
get_user_service()
   │
   ▼
get_user_repository()
   │
   ▼
get_db()
   │
   ▼
SQLAlchemy Session
```

This is conceptually similar to Dependency Injection in ASP.NET Core.

---

# Database

The project currently uses:

- **SQLite**
- **SQLAlchemy ORM**

SQLite was intentionally selected because it does not require a separate database server.

The database is stored locally:

```text
data/app.db
```

---

# SQLAlchemy

SQLAlchemy is used as the ORM/database toolkit.

The project currently uses:

- SQLAlchemy Engine
- Declarative Base
- ORM Models
- Database Sessions
- Session Factory
- Queries
- Transactions
- Commit
- Rollback

Basic flow:

```text
FastAPI
   ↓
Service
   ↓
Repository
   ↓
SQLAlchemy Session
   ↓
SQLAlchemy ORM
   ↓
SQLite
```

---

# Database Models

Database models are kept separately from Pydantic request/response models.

Conceptually:

```text
Pydantic Model
      │
      ├── Request validation
      └── Response validation


SQLAlchemy Model
      │
      └── Database table mapping
```

The current SQLAlchemy User model maps to:

```text
users
├── id
├── name
├── age
└── email
```

---

# CRUD Operations

The User API currently supports complete CRUD operations.

| Operation | HTTP Method | Endpoint | Status |
|---|---|---|---|
| Create | POST | `/users` | ✅ |
| Read | GET | `/users/{user_id}` | ✅ |
| Update | PUT | `/users/{user_id}` | ✅ |
| Delete | DELETE | `/users/{user_id}` | ✅ |

---

## Create User

```http
POST /users
```

Flow:

```text
UserRequest
    ↓
UserService
    ↓
UserRepository
    ↓
db.add()
    ↓
db.commit()
    ↓
db.refresh()
    ↓
SQLite
```

Example SQLAlchemy operations:

```python
db.add(user)
db.commit()
db.refresh(user)
```

---

## Get User

```http
GET /users/{user_id}
```

The repository queries the database:

```python
user = (
    self.db
    .query(User)
    .filter(User.id == user_id)
    .first()
)
```

If the user does not exist:

```python
raise UserNotFoundException(user_id)
```

---

## Update User

```http
PUT /users/{user_id}
```

SQLAlchemy tracks the existing ORM object.

Example:

```python
user.name = new_name
user.age = new_age
user.email = new_email

self.db.commit()
```

---

## Delete User

```http
DELETE /users/{user_id}
```

The repository removes the ORM object:

```python
self.db.delete(user)
self.db.commit()
```

If the user does not exist:

```python
raise UserNotFoundException(user_id)
```

---

# Transactions and Rollback

Database operations are performed inside transactions.

Example:

```python
try:
    self.db.delete(user)
    self.db.commit()

except Exception:
    self.db.rollback()
    raise
```

If a database operation fails:

```text
Database Operation
       ↓
     Error
       ↓
   rollback()
       ↓
Session returned to usable state
```

This helps maintain database consistency.

---

# Logging

The project contains centralized logging functionality.

Example:

```python
self.logger.info(
    "Getting user with ID: %d",
    user_id
)
```

Logging is currently used for:

- Service initialization
- User creation
- User retrieval
- User update
- User deletion
- Database operations
- Errors

Example:

```text
2026-08-14 15:18:49
app.services.user_service
INFO
User created with ID: 1
```

For errors, `logger.exception()` can be used when a traceback is useful:

```python
self.logger.exception(
    "Error deleting user with ID %d",
    user_id
)
```

---

# Exception Handling

Custom exceptions are separated from routers and services.

```text
exceptions/
├── user.py
└── handlers.py
```

Example:

```python
raise UserNotFoundException(user_id)
```

Application flow:

```text
Service / Repository
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

# Pydantic

Pydantic is used for API request and response validation.

Example:

```python
class UserRequest(BaseModel):
    name: str
    age: int
    email: EmailStr
```

Pydantic provides:

- Request validation
- Response validation
- Type validation
- Field validation
- Custom validation

---

# API Endpoints

## Users

| Method | Endpoint | Description |
|---|---|---|
| GET | `/users/{user_id}` | Get user |
| POST | `/users` | Create user |
| PUT | `/users/{user_id}` | Update user |
| DELETE | `/users/{user_id}` | Delete user |

## Products

Product-related APIs are currently implemented through:

```text
Product Router
      ↓
Product Service
```

Additional database models will be introduced incrementally.

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
- Test APIs directly
- View HTTP status codes
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
uvicorn app.main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

---

# Database

The project currently uses SQLite.

Database file:

```text
data/app.db
```

The database schema is currently created using SQLAlchemy.

> **Alembic migrations are intentionally postponed** for a later stage of the learning journey.

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
- SQLAlchemy
- SQLite
- Git
- VS Code

---

# .NET vs FastAPI

Coming from a .NET background, several architectural concepts feel familiar.

| ASP.NET Core | FastAPI |
|---|---|
| Controller | APIRouter |
| Action Method | Route Function |
| DTO | Pydantic Model |
| Model Validation | Pydantic Validation |
| Service | Service |
| Repository | Repository |
| DbContext | SQLAlchemy Session |
| Entity Framework | SQLAlchemy ORM |
| Middleware | Middleware |
| Dependency Injection | `Depends()` |
| Kestrel | Uvicorn |

The implementation is different, but many backend architectural concepts are similar.

---

# Learning Progress

This project is being developed incrementally while learning FastAPI.

## Completed

- [x] FastAPI application
- [x] Uvicorn
- [x] GET APIs
- [x] POST APIs
- [x] PUT APIs
- [x] DELETE APIs
- [x] APIRouter
- [x] Project/package structure
- [x] `__init__.py`
- [x] Pydantic request models
- [x] Pydantic response models
- [x] Model validation
- [x] Custom field validation
- [x] Custom email validation
- [x] HTTP status codes
- [x] Custom exceptions
- [x] Custom exception handlers
- [x] Service layer
- [x] Repository pattern
- [x] Dependency Injection
- [x] FastAPI `Depends()`
- [x] Logging
- [x] SQLite
- [x] SQLAlchemy Engine
- [x] SQLAlchemy ORM models
- [x] SQLAlchemy Session
- [x] Database dependency
- [x] User database integration
- [x] Create user
- [x] Get user
- [x] Update user
- [x] Delete user
- [x] Database transactions
- [x] Transaction rollback
- [x] Swagger / OpenAPI

---

# Intentionally Postponed

## Alembic Migrations

Alembic is an important database migration tool, but it has been intentionally postponed until the SQLAlchemy and database concepts are more familiar.

It will be introduced later when the project starts dealing with schema evolution.

---

# Next Topics

The next major module is **Authentication and Authorization**.

Planned learning path:

```text
Authentication
      ↓
Password Hashing
      ↓
User Registration
      ↓
Login
      ↓
JWT Access Token
      ↓
Authentication Dependency
      ↓
Protect APIs
      ↓
Authorization
      ↓
Roles & Permissions
```

After authentication and authorization, planned topics include:

- [ ] Middleware
- [ ] Configuration management
- [ ] Testing
- [ ] Async APIs
- [ ] Alembic migrations
- [ ] Production deployment

---

# Authentication & Authorization Roadmap

Authentication will be introduced step by step rather than implementing everything at once.

## 1. Password Hashing

Never store plain-text passwords.

```text
Password
   ↓
Hashing Algorithm
   ↓
Password Hash
   ↓
Database
```

## 2. User Registration

A user will register with credentials.

```text
Registration Request
       ↓
Validate Input
       ↓
Hash Password
       ↓
Save User
```

## 3. Login

```text
Login Request
       ↓
Find User
       ↓
Verify Password
       ↓
Generate Token
```

## 4. JWT Authentication

```text
Login
  ↓
Validate Credentials
  ↓
Generate JWT
  ↓
Return Access Token
```

## 5. Protect APIs

Existing APIs will eventually require authentication:

```text
GET /users/1
      ↓
Validate JWT
      ↓
Authenticated?
   /       \
 Yes        No
  ↓          ↓
Service    HTTP 401
```

## 6. Authorization

After authentication, we will learn authorization:

```text
Authentication
      ↓
Who are you?
      ↓
Authorization
      ↓
What are you allowed to do?
```

---

# Learning Approach

```text
Learn a Concept
      ↓
Understand Why
      ↓
Implement It
      ↓
Test It
      ↓
Understand the Architecture
      ↓
Add It to the Project
      ↓
Document It
      ↓
Move to the Next Concept
```

The project is intentionally being developed step by step rather than building everything at once.

---

# Goal

The goal of this project is to learn FastAPI and Python backend development from the fundamentals and gradually build a production-style REST API architecture.

Rather than only following tutorials, I am building the project incrementally and documenting the concepts as I learn them.

Coming from a .NET / C# background, the project also serves as a way to compare familiar backend concepts with their Python/FastAPI equivalents.

Still learning, still experimenting, and adding to the project step by step. 🚀