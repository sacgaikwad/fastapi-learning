# FastAPI Learning Project 🚀

A hands-on project to learn **FastAPI and Python backend development** by building a structured REST API application.

I am primarily coming from a **.NET / C# background**, so this project is also helping me understand how familiar backend concepts such as routing, validation, services, exception handling, dependency injection, repositories, and logging are implemented in the Python ecosystem.

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
│   │   └── logging.py
│   │
│   ├── dependencies/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── product.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── product.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── product.py
│   │   └── error.py
│   │
│   ├── exceptions/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── handlers.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── product_service.py
│   │
│   └── repositories/
│       ├── __init__.py
│       ├── user_repository.py
│       └── product_repository.py
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

The project follows a simple layered architecture:

```text
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
                    ┌─────────────┐
                    │   Service   │
                    └──────┬──────┘
                           │
                 ┌─────────┴─────────┐
                 │                   │
                 ▼                   ▼
          ┌─────────────┐      ┌─────────────┐
          │ Repository  │      │    Logger   │
          └──────┬──────┘      └─────────────┘
                 │
                 ▼
              Database
```

Responsibilities:

```text
Router       → HTTP/API concerns
Service      → Business logic
Repository   → Data access
Logger       → Application diagnostics
Database     → Data persistence
```

The goal is to keep each layer focused on its own responsibility.

---

# Router

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
    service: UserService = Depends(get_user_service)
):
    return service.get_user(user_id)
```

Current routers:

- `user.py` - User-related APIs
- `product.py` - Product-related APIs

---

# Service Layer

The service layer contains business logic and keeps it separate from API routes.

The services are implemented as classes so that dependencies such as repositories and loggers can be injected.

Example:

```python
class UserService:

    def __init__(
        self,
        repository: UserRepository,
        logger: logging.Logger
    ):
        self._repository = repository
        self._logger = logger
```

The service can then use the injected repository:

```python
user = self._repository.get_user(user_id)
```

And the injected logger:

```python
self._logger.info(
    "Getting user with ID: %d",
    user_id
)
```

Current services:

- `UserService`
- `ProductService`

---

# Repository Layer

The repository layer is responsible for data-access operations.

For example:

```python
class UserRepository:

    def __init__(self, logger: logging.Logger):
        self._logger = logger

    def get_user(self, user_id: int):

        self._logger.info(
            "Fetching user with ID from database: %d",
            user_id
        )

        # Database access
        ...
```

The service does not directly access the database.

Instead:

```text
Service
   │
   ▼
Repository
   │
   ▼
Database
```

This keeps business logic and data-access logic separated.

---

# Dependency Injection

FastAPI provides dependency injection through `Depends()`.

Example:

```python
@router.get(
    "/{user_id}",
    response_model=UserDetailResponse
)
def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    return service.get_user(user_id)
```

The router doesn't create `UserService` itself.

FastAPI resolves the dependency:

```text
Router
   │
   │ Depends(get_user_service)
   ▼
UserService
```

---

# Nested Dependencies

Dependencies can themselves have dependencies.

For example:

```python
def get_user_logger() -> logging.Logger:
    return get_logger(
        "app.services.user_service"
    )


def get_user_repository(
    logger: logging.Logger = Depends(get_user_logger)
) -> UserRepository:

    return UserRepository(
        logger=logger
    )


def get_user_service(
    repository: UserRepository = Depends(get_user_repository),
    logger: logging.Logger = Depends(get_user_logger)
) -> UserService:

    return UserService(
        repository=repository,
        logger=logger
    )
```

FastAPI resolves the dependency chain automatically:

```text
Router
   │
   ▼
get_user_service()
   │
   ├───────────────┐
   │               │
   ▼               ▼
Repository       Logger
   │
   │ Depends()
   ▼
Logger
```

Conceptually:

```text
Router
   ↓
Service
   ↓
Repository
   ↓
Database
```

while the logger is also injected where required.

This is similar to dependency injection in ASP.NET Core, although the implementation is different.

---

# Logging

The project uses Python's built-in `logging` module.

A logger can be provided through a dependency:

```python
def get_user_logger() -> logging.Logger:
    return get_logger(
        "app.services.user_service"
    )
```

The service receives the logger through its constructor:

```python
def __init__(
    self,
    repository: UserRepository,
    logger: logging.Logger
):
    self._repository = repository
    self._logger = logger
```

Logging examples:

```python
self._logger.info(
    "Getting user with ID: %d",
    user_id
)
```

```python
self._logger.info(
    "Creating user with name: %s",
    user.name
)
```

```python
self._logger.error(
    "User with ID %d not found",
    user_id
)
```

The leading underscore follows the Python convention for internal class attributes:

```python
self._repository
self._logger
```

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
        raise ValueError(
            "Age must be greater than 18"
        )

    return value
```

The project also includes custom email validation.

---

# Exception Handling

Custom exceptions are separated from routers and services.

```text
exceptions/
├── user.py
└── handlers.py
```

A service can raise a custom exception:

```python
raise UserNotFoundException(user_id)
```

The FastAPI application registers an exception handler to convert the exception into an appropriate HTTP response.

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

Product-related APIs follow the same architecture:

```text
Product Router
      ↓
Product Service
      ↓
Product Repository
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

Alternatively, if `app/main.py` contains the Uvicorn startup block:

```powershell
python -m app.main
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

# VS Code Debugging

The project can be debugged using VS Code and `debugpy`.

A typical `launch.json` configuration is:

```json
{
    "name": "FastAPI Debug",
    "type": "debugpy",
    "request": "launch",
    "module": "uvicorn",
    "args": [
        "app.main:app",
        "--port",
        "8001"
    ],
    "console": "integratedTerminal",
    "justMyCode": true
}
```

Then:

1. Open **Run and Debug** in VS Code.
2. Select **FastAPI Debug**.
3. Press **F5**.
4. Open Swagger on the configured port.
5. Set breakpoints in Router, Dependency, Service or Repository code.

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
       ↓
Debug / Experiment
       ↓
Add Next Concept
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
- Python Logging
- Git
- GitHub
- VS Code
- debugpy

---

# .NET vs FastAPI

Coming from a .NET background, some architectural concepts feel very familiar.

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
| `ILogger<T>` | Python `logging` |
| Kestrel | Uvicorn |

A typical architecture:

```text
ASP.NET Core

Controller → Service → Repository → Database


FastAPI

Router → Service → Repository → Database
```

The implementation is different, but the overall architectural thinking is quite similar.

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
- [x] Repository layer
- [x] User repository
- [x] Product repository
- [x] Dependency Injection
- [x] `Depends()`
- [x] Nested dependencies
- [x] Logger injection
- [x] Application logging
- [x] Swagger / OpenAPI
- [x] VS Code debugging

## Next Topics

- [ ] Database integration
- [ ] Async APIs
- [ ] Authentication and Authorization
- [ ] Middleware
- [ ] Configuration management
- [ ] Testing
- [ ] Production deployment
- [ ] Advanced dependency management

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
Debug It
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