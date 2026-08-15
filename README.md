# 🚀 FastAPI Learning Project

> 🐍 A hands-on journey to learn **FastAPI + Python backend development** by building a structured REST API.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-Learning-009688?logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/PyJWT-JWT%20Authentication-000000?logo=jsonwebtokens&logoColor=white" alt="JWT">
  <img src="https://img.shields.io/badge/Architecture-Layered-6A5ACD" alt="Architecture">
  <img src="https://img.shields.io/badge/Status-Learning-F2C94C" alt="Status">
</p>

I am primarily coming from a **.NET / C# background**, so this project is also helping me understand how familiar backend concepts such as routing, validation, services, exception handling, dependency injection, authentication, and authorization are implemented in the Python ecosystem.

🔗 **GitHub:** [github.com/sacgaikwad/fastapi-learning](https://github.com/sacgaikwad/fastapi-learning)

---

## 🎯 Learning Goal

The goal is not just to learn FastAPI syntax, but to understand how to build a maintainable backend application.

```text
        🐍 Python
           │
           ▼
       ⚡ FastAPI
           │
           ▼
      📦 Pydantic
           │
           ▼
       💉 Depends()
           │
           ▼
       🔐 JWT Auth
           │
           ▼
       🔒 Authorization
           │
           ▼
       🗄️ Database
           │
           ▼
       🧪 Testing
           │
           ▼
       🚀 Production
```

---

# 🏗️ Architecture

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
                    Depends() / Auth
                           │
                           ▼
                    ┌─────────────┐
                    │   Service   │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  Repository │
                    └──────┬──────┘
                           │
                           ▼
                       Database
```

### 🛣️ Router

`APIRouter` is used to organize and group related API endpoints.

Conceptually, it is similar to a **Controller** in ASP.NET Core.

### 🧠 Service Layer

The service layer contains business logic and keeps it separate from API routes.

### 🗃️ Repository Layer

The repository layer will isolate data-access logic from the service layer as database integration is introduced.

---

# 📁 Project Structure

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
```

---

# 💉 Dependency Injection

FastAPI provides dependency injection through `Depends()`.

Example:

```python
def get_user(
    user_id: int,
    current_user_id: int = Depends(get_current_user),
    service=Depends(get_user_service)
):
    return service.get_user(user_id)
```

FastAPI resolves dependencies before executing the route function.

### Current dependencies

| Dependency | Purpose |
|---|---|
| 🔐 `get_current_user` | JWT authentication |
| 👤 `get_user_service` | User service |
| 📦 Other service dependencies | Business logic |

---

# 📦 Pydantic Models

The project uses **Pydantic** models for request and response data.

Example:

```python
class UserRequest(BaseModel):
    name: str
    age: int
    email: EmailStr
```

Pydantic provides:

- ✅ Request validation
- ✅ Response models
- ✅ Type validation
- ✅ Custom field validation

---

# ⚠️ Exception Handling

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

The FastAPI application converts custom exceptions into appropriate HTTP responses.

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

# 🔐 JWT Authentication

JWT authentication has been added to protect user APIs.

## 🔑 Authentication Flow

```text
                    👤 User
                      │
                      ▼
              POST /users/login
                      │
                      ▼
             Validate Credentials
                      │
                      ▼
                🎟️ JWT Token
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
               ┌──────┴──────┐
               │             │
             Valid         Invalid
               │             │
               ▼             ▼
      current_user_id      ❌ 401
               │
               ▼
          Protected API
```

---

## 🎟️ Creating the JWT

The access token contains the authenticated user's ID in the `sub` claim and an expiration time.

```python
payload = {
    "sub": str(user_id),
    "exp": expire
}

return jwt.encode(
    payload,
    SECRET_KEY,
    algorithm=ALGORITHM
)
```

The token is signed using the configured `SECRET_KEY` and `ALGORITHM`.

---

## 🔍 Getting the Current User

The current implementation uses FastAPI's `HTTPBearer` security dependency.

```python
bearer_scheme = HTTPBearer()

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
```

### 🔄 What happens here?

```text
Authorization Header
        │
        ▼
   HTTPBearer()
        │
        ▼
HTTPAuthorizationCredentials
        │
        ▼
credentials.credentials
        │
        ▼
       JWT
        │
        ▼
    jwt.decode()
        │
        ▼
     payload
        │
        ▼
       sub
        │
        ▼
current_user_id
```

---

# 🛡️ Protecting an Endpoint

An endpoint becomes authenticated by adding:

```python
current_user_id: int = Depends(get_current_user)
```

Example:

```python
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
```

FastAPI executes `get_current_user()` **before** executing `get_user()`.

If the JWT is missing or invalid:

```text
Request
  │
  ▼
get_current_user()
  │
  ├── ❌ Invalid → 401 Unauthorized
  │
  └── ✅ Valid
         │
         ▼
      get_user()
```

---

# 🔓 Public vs 🔐 Protected APIs

Current user API security:

| Method | Endpoint | Security |
|---|---|---|
| 🔐 GET | `/users/{user_id}` | Authentication required |
| 🔐 POST | `/users` | Authentication required |
| 🔐 DELETE | `/users/{user_id}` | Authentication required |
| 🔐 PUT | `/users/{user_id}` | Authentication required |
| 🌐 POST | `/users/login` | Public |

### Why is login public?

A user does not have a JWT before logging in.

```text
/login
  │
  ▼
Validate username/password
  │
  ▼
Generate JWT
  │
  ▼
Client receives JWT
  │
  ▼
Use JWT for protected APIs
```

---

# 🔐 Authentication vs Authorization

This is an important distinction.

### 👤 Authentication

Authentication answers:

> **Who are you?**

```text
JWT
 ↓
get_current_user()
 ↓
current_user_id
```

### 🔒 Authorization

Authorization answers:

> **What are you allowed to do?**

For example:

```text
current_user_id
       │
       ▼
   Check role
       │
   ┌───┴────┐
   │        │
 ADMIN     USER
   │        │
   ▼        ▼
 Allow    Deny
```

🚧 **Authorization is the next topic to implement.**

The current project authenticates users, but role-based and ownership-based authorization have not yet been implemented.

---

# 🧪 Example Protected Request

```http
DELETE /users/10
Authorization: Bearer <access_token>
```

Flow:

```text
HTTP Request
     │
     ▼
 HTTPBearer
     │
     ▼
get_current_user()
     │
     ▼
Extract JWT
     │
     ▼
jwt.decode()
     │
     ▼
current_user_id
     │
     ▼
delete_user()
```

---

# 📚 API Documentation

## Swagger UI

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger provides:

- 📋 API listing
- 🧩 Request models
- 📤 Response models
- 🧪 Interactive API testing
- 🔐 Authentication testing
- ⚠️ Validation errors
- 📄 OpenAPI documentation

## ReDoc

```text
http://127.0.0.1:8000/redoc
```

## OpenAPI JSON

```text
http://127.0.0.1:8000/openapi.json
```

---

# ▶️ Getting Started

## 1️⃣ Clone the repository

```powershell
git clone https://github.com/sacgaikwad/fastapi-learning.git
```

## 2️⃣ Navigate to the project

```powershell
cd fastapi-learning
```

## 3️⃣ Create a virtual environment

```powershell
python -m venv .venv
```

## 4️⃣ Activate the virtual environment

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

## 5️⃣ Install dependencies

```powershell
pip install -r requirements.txt
```

## 6️⃣ Run the application

```powershell
python -m app.main
```

Or:

```powershell
uvicorn app.main:app --reload
```

Application:

```text
http://127.0.0.1:8000
```

---

# 🔄 Application Learning Flow

```text
📥 Learn Concept
      │
      ▼
💻 Implement
      │
      ▼
🧠 Understand Architecture
      │
      ▼
🧪 Test
      │
      ▼
📝 Document
      │
      ▼
🚀 Move to Next Concept
```

---

# 📊 Learning Progress

| Topic | Status |
|---|:---:|
| 🐍 Python basics | ✅ |
| ⚡ FastAPI basics | ✅ |
| 🛣️ APIRouter | ✅ |
| 📦 Pydantic | ✅ |
| 🔎 Request validation | ✅ |
| 📤 Response models | ✅ |
| ⚠️ Custom exceptions | ✅ |
| 🧩 Exception handlers | ✅ |
| 🧠 Service layer | ✅ |
| 💉 Dependency Injection | ✅ |
| 🔗 `Depends()` | ✅ |
| 🎟️ JWT token generation | ✅ |
| 🔐 JWT authentication | ✅ |
| 🛡️ Protected endpoints | ✅ |
| 🔑 Login | ✅ |
| 🔒 Role-based authorization | 🔜 |
| 👤 Ownership authorization | 🔜 |
| 🗄️ Database integration | ⏳ |
| 🗃️ Repository pattern | ⏳ |
| ⚡ Async APIs | ⏳ |
| 🧱 Middleware | ⏳ |
| ⚙️ Configuration management | ⏳ |
| 🧪 Testing | ⏳ |
| 🚢 Production deployment | ⏳ |

### Legend

- ✅ Completed
- 🔜 Next
- ⏳ Planned

---

# 🆚 .NET vs FastAPI

Coming from a .NET background, many architectural concepts are familiar.

| ASP.NET Core | FastAPI |
|---|---|
| 🎮 Controller | 🛣️ APIRouter |
| ⚙️ Action Method | 🐍 Route Function |
| 📦 DTO | 📦 Pydantic Model |
| ✅ Model Validation | ✅ Pydantic Validation |
| 🧠 Service | 🧠 Service |
| 🗃️ Repository | 🗃️ Repository |
| 💉 Dependency Injection | 💉 `Depends()` |
| 🔐 JWT Authentication | 🔐 JWT + Security Dependency |
| ⚡ Kestrel | ⚡ Uvicorn |

The implementation differs, but the core backend architecture is surprisingly similar.

---

# 🛠️ Technologies

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Pydantic-E92063?logo=pydantic&logoColor=white" alt="Pydantic">
  <img src="https://img.shields.io/badge/Uvicorn-2C2C2C" alt="Uvicorn">
  <img src="https://img.shields.io/badge/PyJWT-000000" alt="PyJWT">
  <img src="https://img.shields.io/badge/VS%20Code-007ACC?logo=visualstudiocode&logoColor=white" alt="VS Code">
</p>

---

# 🎯 Next Step

## 🔒 Authorization

The next major topic is:

```text
JWT Authentication
        ↓
Identify Current User
        ↓
Retrieve User / Role
        ↓
Check Permission
        ↓
Allow / Deny Request
```

We will build this using FastAPI dependencies so that authorization logic stays reusable and clean.

---

# 🙌 Learning Philosophy

> **Don't just learn the framework. Understand what the framework is doing for you.**

The project is being built incrementally while learning FastAPI.

Every concept is:

```text
Learn → Implement → Test → Understand → Document
```

Still learning, still experimenting, and building one concept at a time. 🚀🐍
