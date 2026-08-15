# 🚀 FastAPI Learning Project

> 🐍 A hands-on journey to learn **FastAPI + Python backend
> development** by building a structured REST API.

```{=html}
<p align="center">
```
`<img src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white">`{=html}
`<img src="https://img.shields.io/badge/FastAPI-Learning-009688?logo=fastapi&logoColor=white">`{=html}
`<img src="https://img.shields.io/badge/PyJWT-JWT%20Authentication-000000">`{=html}
`<img src="https://img.shields.io/badge/RBAC-Role%20Based%20Authorization-6A5ACD">`{=html}
`<img src="https://img.shields.io/badge/Status-Learning-F2C94C">`{=html}
```{=html}
</p>
```
I am primarily coming from a **.NET / C# background**, so this project
is helping me understand how familiar backend concepts are implemented
in the Python ecosystem.

🔗 **GitHub:** https://github.com/sacgaikwad/fastapi-learning

------------------------------------------------------------------------

# 🎯 Learning Goal

The goal is not just to learn FastAPI syntax, but to understand how to
build a maintainable backend application.

``` text
Python → FastAPI → Pydantic → Depends()
                    ↓
              JWT Authentication
                    ↓
              RBAC Authorization
                    ↓
                Database
                    ↓
                 Testing
                    ↓
               Production
```

------------------------------------------------------------------------

# 🏗️ Architecture

``` text
Client
  │
  ▼
Router
  │
  │ Depends() / Authentication / Authorization
  ▼
Service
  │
  ▼
Repository
  │
  ▼
Database
```

The project follows a layered architecture similar to patterns commonly
used in ASP.NET Core.

------------------------------------------------------------------------

# 📁 Project Structure

``` text
fastapi-learning/
├── app/
│   ├── main.py
│   ├── routers/
│   │   ├── user.py
│   │   └── product.py
│   ├── models/
│   │   ├── user.py
│   │   ├── role.py
│   │   └── error.py
│   ├── database/
│   │   ├── models/
│   │   │   └── user.py
│   │   ├── dependencies.py
│   │   └── connection.py
│   ├── dependencies/
│   │   ├── auth.py
│   │   └── user.py
│   ├── services/
│   │   └── user_service.py
│   ├── repositories/
│   │   └── user_repository.py
│   ├── exceptions/
│   └── core/
├── data/
│   └── app.db
├── tests/
├── requirements.txt
└── README.md
```

------------------------------------------------------------------------

# 💉 Dependency Injection

FastAPI provides dependency injection through `Depends()`.

Current dependency examples:

  Dependency              Purpose
  ----------------------- --------------------------
  🔐 `get_current_user`   JWT authentication
  👤 `get_user_service`   User service
  🔒 `require_roles`      Role-based authorization
  🗄️ `get_db`             Database session

------------------------------------------------------------------------

# 🔐 JWT Authentication

JWT authentication protects user APIs.

## 🔑 Authentication Flow

``` text
POST /users/login
       │
       ▼
Validate Credentials
       │
       ▼
Create JWT
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
   ┌───┴───┐
   │       │
 Valid   Invalid
   │       │
   ▼       ▼
User ID   401
   │
   ▼
Protected API
```

The JWT contains the authenticated user's ID in the `sub` claim and an
expiration time.

``` python
payload = {
    "sub": str(user_id),
    "exp": expire
}
```

The role is stored in the database rather than being trusted from the
client.

------------------------------------------------------------------------

# 🔒 Role-Based Authorization (RBAC)

Authentication answers:

> **Who are you?**

Authorization answers:

> **What are you allowed to do?**

The project now implements **Role-Based Access Control (RBAC)**.

## 👤 User Roles

``` python
class UserRole(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    SUPPORT = "SUPPORT"
    USER = "USER"
```

The database stores the role:

``` python
role: Mapped[str] = mapped_column(
    String(255),
    nullable=False
)
```

New users receive the default role:

``` text
USER
```

The role is assigned server-side and is not part of `UserRequest`.

------------------------------------------------------------------------

# 🧩 Reusable `require_roles()`

Authorization is implemented as a reusable FastAPI dependency instead of
scattering role checks across endpoints.

``` python
def require_roles(*allowed_roles: UserRole):

    def roles_checker(
        current_user_id: int = Depends(get_current_user),
        service=Depends(get_user_service)
    ):
        current_user = service.get_user(current_user_id)

        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )

        return current_user

    return roles_checker
```

An endpoint can declare multiple allowed roles:

``` python
Depends(
    require_roles(
        UserRole.ADMIN,
        UserRole.SUPER_ADMIN
    )
)
```

## 🔄 Authorization Flow

``` text
HTTP Request
      │
      ▼
require_roles(...)
      │
      ▼
get_current_user()
      │
      ▼
Validate JWT
      │
      ▼
current_user_id
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
   ┌──┴──┐
   │     │
Allowed Denied
   │     │
   ▼     ▼
 API    403
```

------------------------------------------------------------------------

# 🛡️ 401 vs 403

### 🔴 401 Unauthorized

Authentication failed.

Examples:

-   Missing JWT
-   Invalid JWT
-   Expired JWT

``` text
"I don't know who you are."
```

### 🟠 403 Forbidden

Authentication succeeded, but the user does not have the required role.

``` text
"I know who you are,
but you are not allowed to do this."
```

------------------------------------------------------------------------

# 🧪 RBAC Testing

The first role-protected endpoint is:

``` http
DELETE /users/{user_id}
```

Allowed roles:

``` text
ADMIN
SUPER_ADMIN
```

Tested behavior:

  Authentication   Role            Result
  ---------------- ------------- --------
  No JWT           ---             🔴 401
  Valid JWT        USER            🟠 403
  Valid JWT        MANAGER         🟠 403
  Valid JWT        ADMIN           🟢 204
  Valid JWT        SUPER_ADMIN     🟢 204

Example endpoint:

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

------------------------------------------------------------------------

# 🔓 Public vs 🔐 Protected APIs

  Method      Endpoint             Security
  ----------- -------------------- -------------------------
  🔐 GET      `/users/{user_id}`   Authentication required
  🔐 POST     `/users`             Authentication required
  🔐 DELETE   `/users/{user_id}`   Authentication + RBAC
  🔐 PUT      `/users/{user_id}`   Authentication required
  🌐 POST     `/users/login`       Public

------------------------------------------------------------------------

# 📚 API Documentation

### Swagger UI

``` text
http://127.0.0.1:8000/docs
```

### ReDoc

``` text
http://127.0.0.1:8000/redoc
```

### OpenAPI JSON

``` text
http://127.0.0.1:8000/openapi.json
```

------------------------------------------------------------------------

# ▶️ Getting Started

``` powershell
git clone https://github.com/sacgaikwad/fastapi-learning.git
cd fastapi-learning

python -m venv .venv
.venv\Scripts\Activate.ps1

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Application:

``` text
http://127.0.0.1:8000
```

------------------------------------------------------------------------

# 📊 Learning Progress

  Topic                                Status
  ----------------------------------- --------
  🐍 Python basics                       ✅
  ⚡ FastAPI basics                      ✅
  🛣️ APIRouter                           ✅
  📦 Pydantic                            ✅
  🔎 Request validation                  ✅
  📤 Response models                     ✅
  ⚠️ Custom exceptions                   ✅
  🧩 Exception handlers                  ✅
  🧠 Service layer                       ✅
  🗃️ Repository pattern                  ✅
  🗄️ SQLAlchemy / SQLite                 ✅
  💉 Dependency Injection                ✅
  🔗 `Depends()`                         ✅
  🎟️ JWT token generation                ✅
  🔐 JWT authentication                  ✅
  🛡️ Protected endpoints                 ✅
  🔑 Login                               ✅
  👤 User roles                          ✅
  🔒 Role-based authorization            ✅
  🧩 Reusable `require_roles()`          ✅
  🧪 RBAC testing                        ✅
  👤 Ownership authorization             🔜
  🔐 Permission-based authorization      🔜
  ⚡ Async APIs                          ⏳
  🧱 Middleware                          ⏳
  ⚙️ Configuration management            ⏳
  🧪 Automated testing                   ⏳
  🚢 Production deployment               ⏳

------------------------------------------------------------------------

# 🆚 .NET vs FastAPI

  ASP.NET Core           FastAPI
  ---------------------- ---------------------------
  Controller             APIRouter
  Action Method          Route Function
  DTO                    Pydantic Model
  Model Validation       Pydantic Validation
  Service                Service
  Repository             Repository
  Dependency Injection   `Depends()`
  JWT Authentication     JWT + Security Dependency
  Authorization Policy   Dependency-based RBAC
  Kestrel                Uvicorn

------------------------------------------------------------------------

# 🛠️ Technologies

-   Python
-   FastAPI
-   Pydantic
-   SQLAlchemy
-   SQLite
-   Uvicorn
-   PyJWT
-   VS Code

------------------------------------------------------------------------

# 🎯 Next Step

``` text
Role-Based Authorization ✅
        │
        ▼
Ownership Authorization 🔜
        │
        ▼
Permission-Based Authorization 🔜
        │
        ▼
Fine-Grained Authorization
```

------------------------------------------------------------------------

# 🙌 Learning Philosophy

> **Don't just learn the framework. Understand what the framework is
> doing for you.**

``` text
Learn → Implement → Test → Understand → Document
```

Still learning, still experimenting, and building one concept at a time.
🚀🐍
