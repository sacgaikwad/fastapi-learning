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