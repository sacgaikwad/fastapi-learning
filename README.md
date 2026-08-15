# 🚀 FastAPI Learning Project

> 🐍 A hands-on journey to learn **FastAPI + Python backend
> development** by building a structured REST API.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Learning-009688?logo=fastapi&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-Validation-E92063?logo=pydantic&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?logo=sqlalchemy&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Authentication-000000)
![RBAC](https://img.shields.io/badge/RBAC-Authorization-6A5ACD)
![Status](https://img.shields.io/badge/Status-Learning-F2C94C)

I am primarily coming from a **.NET / C# background**, so this project
is helping me understand how familiar backend concepts are implemented
in the Python ecosystem.

The objective is not only to learn FastAPI syntax, but to understand
**how a production-style backend is structured**, how the different
layers communicate, and what FastAPI provides under the hood.

🔗 **GitHub:** https://github.com/sacgaikwad/fastapi-learning

------------------------------------------------------------------------

# 🎯 Project Goal

This project is being developed incrementally.

The learning approach is:

``` text
Learn a concept
      ↓
Implement it
      ↓
Test it
      ↓
Understand the architecture
      ↓
Document it
      ↓
Move to the next concept
```

The project currently covers:

``` text
🐍 Python
   ↓
⚡ FastAPI
   ↓
📦 Pydantic
   ↓
💉 Dependency Injection
   ↓
🧠 Service Layer
   ↓
🗃️ Repository Layer
   ↓
🗄️ SQLAlchemy + SQLite
   ↓
🔐 Password Hashing
   ↓
🎟️ JWT Authentication
   ↓
🔒 Role-Based Authorization
```

------------------------------------------------------------------------

# 🏗️ Application Architecture

The application follows a layered architecture.

``` text
                         HTTP Request
                              │
                              ▼
                     ┌─────────────────┐
                     │     Router      │
                     │   APIRouter     │
                     └────────┬────────┘
                              │
                     Depends / Security
                              │
                              ▼
                     ┌─────────────────┐
                     │     Service     │
                     │  Business Logic │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │   Repository    │
                     │ Database Access │
                     └────────┬────────┘
                              │
                              ▼
                         SQLite DB
```

The responsibilities are intentionally separated:

  Layer            Responsibility
  ---------------- --------------------------------------------------------
  Router           HTTP endpoints and request/response handling
  Dependency       Dependency injection, authentication and authorization
  Service          Business logic
  Repository       Database access
  Model            Request/response/domain structures
  Database Model   SQLAlchemy ORM mapping
  Core             Security and logging
  Exceptions       Application-specific exceptions

------------------------------------------------------------------------

# 📁 Project Structure

``` text
fastapi-learning/
│
├── app/
│   │
│   ├── main.py
│   │
│   ├── routers/
│   │   └── user.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   └── role.py
│   │
│   ├── database/
│   │   ├── models/
│   │   │   └── user.py
│   │   ├── connection.py
│   │   └── dependencies.py
│   │
│   ├── dependencies/
│   │   ├── auth.py
│   │   └── user.py
│   │
│   ├── services/
│   │   └── user_service.py
│   │
│   ├── repositories/
│   │   └── user_repository.py
│   │
│   ├── exceptions/
│   │   ├── auth.py
│   │   └── user.py
│   │
│   └── core/
│       ├── security.py
│       └── logging.py
│
├── data/
│   └── app.db
│
├── tests/
│
├── scripts/
│   └── update_user_role.py
│
├── requirements.txt
└── README.md
```

------------------------------------------------------------------------

# ⚡ FastAPI Fundamentals

## APIRouter

User APIs are grouped using `APIRouter`:

``` python
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
```

This gives the application a clean way to organize endpoints.

------------------------------------------------------------------------

# 🛣️ User APIs

The current user router contains:

``` text
POST   /users/login
GET    /users/{user_id}
POST   /users
PUT    /users/{user_id}
DELETE /users/{user_id}
```

Example:

``` python
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

The route function stays small because authentication, dependency
resolution, business logic and database access are handled elsewhere.

------------------------------------------------------------------------

# 📦 Pydantic Models

Pydantic is used for request validation and response serialization.

## UserRequest

``` python
class UserRequest(BaseModel):
    name: str
    age: int
    email: EmailStr
    password: str
```

## Custom Email Validation

Only Gmail addresses are currently accepted:

``` python
@field_validator("email")
@classmethod
def validate_email(cls, value):
    domain = value.split("@")[1]

    if domain != "gmail.com":
        raise ValueError(
            "Email must be a gmail.com address"
        )

    return value
```

## Custom Age Validation

The current rule requires the user to be older than 18:

``` python
@field_validator("age")
@classmethod
def validate_age(cls, value):
    if value <= 18:
        raise ValueError(
            "Age must be greater than 18"
        )

    return value
```

------------------------------------------------------------------------

# 📤 Response Models

The API uses separate response models instead of returning database
entities directly.

``` python
class UserResponse(BaseModel):
    user_id: int
```

Detailed user response:

``` python
class UserDetailResponse(BaseModel):
    user_id: int
    name: str
    age: int
    email: str
    role: UserRole
```

This separation helps prevent implementation details such as
`password_hash` from being returned to API consumers.

------------------------------------------------------------------------

# 💉 Dependency Injection

FastAPI provides dependency injection through `Depends()`.

Current dependencies include:

``` text
get_db()
    ↓
Database Session

get_user_logger()
    ↓
Application Logger

get_user_repository()
    ↓
UserRepository

get_user_service()
    ↓
UserService

get_current_user()
    ↓
JWT Authentication

require_roles()
    ↓
Role Authorization
```

------------------------------------------------------------------------

# 🗄️ Database

The project currently uses:

-   SQLAlchemy ORM
-   SQLite
-   `app.db`

The database is stored under:

``` text
data/app.db
```

The database path is created using `pathlib`:

``` python
BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(exist_ok=True)

DATABASE_URL = f"sqlite:///{DATA_DIR / 'app.db'}"
```

This avoids relying on the current working directory.

------------------------------------------------------------------------

# 🔌 Database Session

The application uses a SQLAlchemy session factory:

``` python
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)
```

The FastAPI database dependency provides a session to requests and
closes it after use.

Conceptually:

``` text
HTTP Request
     ↓
get_db()
     ↓
Create Session
     ↓
Repository uses Session
     ↓
Request completes
     ↓
Session closed
```

------------------------------------------------------------------------

# 🗃️ SQLAlchemy User Model

The database user model contains:

``` python
class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    age: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
```

Important:

``` text
password_hash
```

is stored instead of the original password.

The role is stored in the database so authorization can be evaluated
server-side.

------------------------------------------------------------------------

# 🧠 Service Layer

The `UserService` contains business logic.

Example:

``` python
def create_user(
    self,
    user: UserRequest
) -> UserResponse:

    password_hashed = hash_password(
        user.password
    )

    user_created = self.repository.create_user(
        user,
        password_hashed,
        UserRole.USER
    )

    return UserResponse(
        user_id=user_created.id
    )
```

Notice that the password is hashed before being passed to the
repository.

Also notice that a newly created user is assigned:

``` text
USER
```

The client does not choose the initial role.

------------------------------------------------------------------------

# 🗃️ Repository Pattern

The repository is responsible for database operations.

Example:

``` python
def get_user(self, user_id: int):

    user = self.db.query(User).filter(
        User.id == user_id
    ).first()

    if user is None:
        raise UserNotFoundException(user_id)

    return {
        "user_id": user.id,
        "name": user.name,
        "age": user.age,
        "email": user.email,
        "role": user.role
    }
```

The service consumes this data and converts it into the appropriate
response model.

Architecture:

``` text
Router
  ↓
UserService
  ↓
UserRepository
  ↓
SQLAlchemy
  ↓
SQLite
```

------------------------------------------------------------------------

# 🔐 Password Security

Passwords should never be stored as plain text.

The application uses password hashing:

``` text
User Password
      ↓
hash_password()
      ↓
Password Hash
      ↓
Database
```

During login:

``` text
Entered Password
      ↓
verify_password()
      ↓
Stored Password Hash
      ↓
Match?
   ┌──┴──┐
  Yes    No
   │      │
   ▼      ▼
Login   Invalid
```

The database stores:

``` text
password_hash
```

and never the original password.

------------------------------------------------------------------------

# 🔑 Login

The login request contains:

``` python
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
```

The login flow is:

``` text
POST /users/login
       │
       ▼
Find user by email
       │
       ▼
Verify password
       │
   ┌───┴────┐
   │        │
 Valid    Invalid
   │        │
   ▼        ▼
Create JWT  401
   │
   ▼
Return Access Token
```

The response contains:

``` python
class LoginResponse(BaseModel):
    access_token: str | None = None
    token_type: str | None = None
```

Example:

``` json
{
    "access_token": "<JWT>",
    "token_type": "bearer"
}
```

------------------------------------------------------------------------

# 🎟️ JWT Authentication

JWT is used to authenticate protected endpoints.

The access token is created with:

``` python
def create_access_token(
    user_id: int,
    expires_delta: timedelta | None = None
):
    expire = datetime.now(timezone.utc)

    if expires_delta:
        expire += expires_delta
    else:
        expire += timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

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

The JWT contains:

``` text
sub → user ID
exp → expiration time
```

------------------------------------------------------------------------

# 🔍 `get_current_user()`

The application uses FastAPI's `HTTPBearer`.

``` python
bearer_scheme = HTTPBearer()
```

The dependency extracts the bearer token:

``` python
def get_current_user(
    credentials: HTTPAuthorizationCredentials =
        Depends(bearer_scheme)
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

The request therefore needs:

``` http
Authorization: Bearer <access_token>
```

------------------------------------------------------------------------

# 🔐 Authentication vs Authorization

This distinction is important.

## Authentication

Authentication answers:

> **Who are you?**

Our implementation:

``` text
JWT
 ↓
get_current_user()
 ↓
Validate token
 ↓
Get user ID
```

## Authorization

Authorization answers:

> **Are you allowed to perform this operation?**

Our implementation:

``` text
Current User
 ↓
Get role from database
 ↓
Compare with allowed roles
 ↓
Allow or reject request
```

------------------------------------------------------------------------

# 🔒 Role-Based Access Control (RBAC)

RBAC is now implemented and tested.

The basic idea:

``` text
User
 ↓
Role
 ↓
Permissions / Access
```

The role is stored in the database.

Example roles used by the authorization design:

``` text
SUPER_ADMIN
ADMIN
MANAGER
SUPPORT
USER
```

The exact access policy can evolve as the application becomes more
complex.

------------------------------------------------------------------------

# 🧩 Reusable `require_roles()`

The most important part of the RBAC implementation is the reusable
dependency:

``` python
def require_roles(*allowed_roles: UserRole):

    def roles_checker(
        current_user_id: int = Depends(get_current_user),
        service=Depends(get_user_service)
    ):
        current_user = service.get_user(
            current_user_id
        )

        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )

        return current_user

    return roles_checker
```

This gives us a reusable authorization mechanism.

For example:

``` python
Depends(
    require_roles(
        UserRole.ADMIN,
        UserRole.SUPER_ADMIN
    )
)
```

means:

``` text
ADMIN       → allowed
SUPER_ADMIN → allowed
USER        → denied
MANAGER     → denied
SUPPORT     → denied
```

------------------------------------------------------------------------

# 🔄 Complete Authentication + Authorization Flow

``` text
                    HTTP Request
                         │
                         ▼
                  Router Endpoint
                         │
                         ▼
                require_roles(...)
                         │
                         ▼
                get_current_user()
                         │
                         ▼
                    JWT Decode
                         │
                 ┌───────┴────────┐
                 │                │
              Invalid            Valid
                 │                │
                 ▼                ▼
                401         current_user_id
                                  │
                                  ▼
                         get_user_service()
                                  │
                                  ▼
                         UserService.get_user()
                                  │
                                  ▼
                        UserRepository.get_user()
                                  │
                                  ▼
                              Database
                                  │
                                  ▼
                           current_user.role
                                  │
                            ┌─────┴─────┐
                            │           │
                         Allowed      Denied
                            │           │
                            ▼           ▼
                       Execute API     403
```

------------------------------------------------------------------------

# 🛡️ 401 vs 403

This project explicitly distinguishes authentication failures from
authorization failures.

## 401 Unauthorized

The identity cannot be established.

Examples:

``` text
No token
Invalid token
Expired token
Malformed token
```

Meaning:

> "I don't know who you are."

## 403 Forbidden

The identity is valid, but access is denied.

Example:

``` text
JWT valid
User role = USER
Required role = ADMIN
```

Meaning:

> "I know who you are, but you are not allowed to do this."

------------------------------------------------------------------------

# 🧪 RBAC Test Results

The first role-protected endpoint is:

``` http
DELETE /users/{user_id}
```

Current authorization:

``` python
require_roles(
    UserRole.ADMIN,
    UserRole.SUPER_ADMIN
)
```

Test results:

  Request                                Result
  ----------------------- ---------------------
  No JWT                    🔴 401 Unauthorized
  Valid USER JWT               🟠 403 Forbidden
  Valid ADMIN JWT             🟢 204 No Content
  Valid SUPER_ADMIN JWT       🟢 204 No Content

This confirms that both authentication and role-based authorization are
working.

------------------------------------------------------------------------

# 🗑️ Protected DELETE Endpoint

The endpoint is implemented as:

``` python
@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user(
    user_id: int,
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN
        )
    ),
    service=Depends(get_user_service)
):
    return service.delete_user(user_id)
```

The endpoint itself does not contain:

``` python
if role == "ADMIN":
```

Instead, authorization is handled by the reusable dependency.

This keeps route handlers clean and makes authorization rules easier to
reuse.

------------------------------------------------------------------------

# 🔓 Public vs Protected APIs

  Method   Endpoint             Current Security
  -------- -------------------- --------------------------
  POST     `/users/login`       🌐 Public
  GET      `/users/{user_id}`   🔐 Authentication
  POST     `/users`             🔐 Authentication
  PUT      `/users/{user_id}`   🔐 Authentication
  DELETE   `/users/{user_id}`   🔒 Authentication + RBAC

The login endpoint must remain public because a user needs to
authenticate before obtaining a JWT.

------------------------------------------------------------------------

# ⚠️ Exception Handling

The project uses custom exceptions instead of putting all error handling
directly into route functions.

Examples include:

``` text
UserNotFoundException
InvalidCredentialsException
```

Conceptually:

``` text
Repository / Service
        │
        ▼
Raise Application Exception
        │
        ▼
Global Exception Handler
        │
        ▼
HTTP Response
```

This keeps business code cleaner.

------------------------------------------------------------------------

# 📝 Logging

Logging is centralized through the application's logging utilities.

Services and repositories receive a logger through dependency injection.

Example:

``` python
def __init__(
    self,
    repository: UserRepository,
    logger: logging.Logger
):
    self.repository = repository
    self.logger = logger
```

This allows important operations to be logged, such as:

``` text
User login
User creation
User retrieval
User update
User deletion
Database operations
Authentication failures
```

------------------------------------------------------------------------

# 📚 API Documentation

FastAPI automatically generates OpenAPI documentation.

## Swagger UI

``` text
http://127.0.0.1:8000/docs
```

Swagger provides:

-   API listing
-   Request models
-   Response models
-   Interactive API testing
-   Authentication support
-   Validation errors
-   OpenAPI documentation

## ReDoc

``` text
http://127.0.0.1:8000/redoc
```

## OpenAPI JSON

``` text
http://127.0.0.1:8000/openapi.json
```

------------------------------------------------------------------------

# ▶️ Getting Started

## 1. Clone the repository

``` powershell
git clone https://github.com/sacgaikwad/fastapi-learning.git
```

## 2. Navigate to the project

``` powershell
cd fastapi-learning
```

## 3. Create a virtual environment

``` powershell
python -m venv .venv
```

## 4. Activate the environment

``` powershell
.venv\Scripts\Activate.ps1
```

## 5. Install dependencies

``` powershell
pip install -r requirements.txt
```

## 6. Start FastAPI

``` powershell
uvicorn app.main:app --reload
```

Application:

``` text
http://127.0.0.1:8000
```

Swagger:

``` text
http://127.0.0.1:8000/docs
```

------------------------------------------------------------------------

# 🧪 Testing the Authentication Flow

## Step 1 --- Login

``` http
POST /users/login
```

Example request:

``` json
{
    "email": "1@gmail.com",
    "password": "your-password"
}
```

Response:

``` json
{
    "access_token": "<JWT>",
    "token_type": "bearer"
}
```

## Step 2 --- Authorize Swagger

Click:

``` text
Authorize
```

and provide:

``` text
Bearer <JWT>
```

## Step 3 --- Call a protected API

For example:

``` http
GET /users/1
```

## Step 4 --- Test RBAC

Use a USER token:

``` http
DELETE /users/1
```

Expected:

``` text
403 Forbidden
```

Then use an ADMIN token:

``` http
DELETE /users/1
```

Expected:

``` text
204 No Content
```

------------------------------------------------------------------------

# 🗄️ Working with the SQLite Database

The database is located at:

``` text
D:\Learning\Python\fastapi-learning\data\app.db
```

The exact path depends on the local project location.

The database can be inspected with SQLite tools such as DB Browser for
SQLite.

Example query:

``` sql
SELECT id, name, email, role
FROM users;
```

For RBAC testing, a user's role can be changed in the development
database:

``` sql
UPDATE users
SET role = 'ADMIN'
WHERE id = 1;
```

For learning/testing only, this can also be done using a temporary
Python script.

------------------------------------------------------------------------

# ⚠️ SQLite Development Note

SQLite is excellent for learning and small applications, but concurrent
writes can result in:

``` text
sqlite3.OperationalError:
database is locked
```

For example, if FastAPI and another process both hold the database open
during a write.

A practical development approach is:

``` text
Stop FastAPI
   ↓
Close DB Browser
   ↓
Perform database update
   ↓
Restart FastAPI
```

The application can later be moved to a production database such as
PostgreSQL or SQL Server.

------------------------------------------------------------------------

# 🆚 .NET vs FastAPI

Coming from a .NET background, many architectural concepts map
naturally:

  ASP.NET Core           FastAPI
  ---------------------- ---------------------------
  Controller             `APIRouter`
  Action Method          Route Function
  DTO                    Pydantic Model
  Model Validation       Pydantic Validation
  Service                Service
  Repository             Repository
  Dependency Injection   `Depends()`
  JWT Authentication     JWT + Security Dependency
  Authorization Policy   Dependency-based RBAC
  Middleware             FastAPI Middleware
  Kestrel                Uvicorn
  Entity Framework       SQLAlchemy

The syntax is different, but the architectural ideas are very similar.

------------------------------------------------------------------------

# 📊 Learning Progress

  Topic                            Status
  ------------------------------- --------
  🐍 Python fundamentals             ✅
  ⚡ FastAPI fundamentals            ✅
  🛣️ APIRouter                       ✅
  📦 Pydantic models                 ✅
  🔎 Request validation              ✅
  📤 Response models                 ✅
  ⚠️ Custom exceptions               ✅
  🧩 Exception handling              ✅
  🧠 Service layer                   ✅
  🗃️ Repository pattern              ✅
  🗄️ SQLAlchemy                      ✅
  💾 SQLite                          ✅
  💉 Dependency Injection            ✅
  🔗 `Depends()`                     ✅
  📝 Application logging             ✅
  🔐 Password hashing                ✅
  🔑 Login                           ✅
  🎟️ JWT generation                  ✅
  🔐 JWT authentication              ✅
  🛡️ Protected endpoints             ✅
  👤 User roles                      ✅
  🔒 Role-Based Authorization        ✅
  🧩 Reusable `require_roles()`      ✅
  🧪 RBAC testing                    ✅
  ⚙️ Middleware                      🔜
  🌐 CORS                            ⏳
  ⚡ Async / Await                   ⏳
  🧪 Pytest                          ⏳
  🧰 Configuration management        ⏳
  🚀 Background tasks                ⏳
  📊 API monitoring / metrics        ⏳
  🚢 Production deployment           ⏳

### Legend

-   ✅ Completed
-   🔜 Next
-   ⏳ Planned

------------------------------------------------------------------------

# 🧭 Learning Roadmap

The current roadmap is:

``` text
FastAPI Fundamentals
        │
        ▼
Pydantic + Validation
        │
        ▼
Exception Handling
        │
        ▼
Service / Repository Architecture
        │
        ▼
SQLAlchemy + SQLite
        │
        ▼
Dependency Injection
        │
        ▼
Password Hashing
        │
        ▼
JWT Authentication
        │
        ▼
RBAC Authorization
        │
        ▼
⚙️ Middleware             ← NEXT
        │
        ▼
🌐 CORS
        │
        ▼
⚡ Async / Await
        │
        ▼
🧪 Pytest
        │
        ▼
🧰 Configuration
        │
        ▼
🚀 Production
```

------------------------------------------------------------------------

# 🎯 Why Middleware Is Next

RBAC is now complete at the fundamentals level.

The next concept is **FastAPI Middleware**.

Middleware sits around the request/response pipeline:

``` text
Client
  │
  ▼
┌─────────────────┐
│   Middleware    │
└────────┬────────┘
         │
         ▼
      Router
         │
         ▼
   Dependencies
         │
         ▼
      Service
         │
         ▼
    Repository
         │
         ▼
      Database
         │
         ▼
      Response
         │
         ▼
┌─────────────────┐
│   Middleware    │
└────────┬────────┘
         │
         ▼
       Client
```

Middleware can be used for:

-   Request/response logging
-   Execution-time measurement
-   Request IDs / correlation IDs
-   CORS
-   Headers
-   Global request processing
-   Metrics
-   Cross-cutting concerns

This is the next concept we will explore.

------------------------------------------------------------------------

# 🙌 Learning Philosophy

> **Don't just learn the framework. Understand what the framework is
> doing for you.**

The goal is to understand the concepts rather than simply copy code.

``` text
Learn
  ↓
Implement
  ↓
Test
  ↓
Debug
  ↓
Understand
  ↓
Document
  ↓
Move Forward
```

Still learning, still experimenting, and building one concept at a time.
🚀🐍
