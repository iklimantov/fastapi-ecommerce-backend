# FastAPI E-commerce Backend

Backend for an online store built with FastAPI.

## Tech Stack
- Python 3.10+
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL / SQLite

## Features
- User authentication
- Product catalog
- Orders and payments
- REST API

## Project structure
#### Still in process, can be modified

```text
fastapi_ecommerce/
├── app/
│   ├── __init__.py
│   │
│   ├── main.py                  # FastAPI app entrypoint
│   │
│   ├── database.py              # DB engine & session
│   ├── db_depends.py            # Depends for FastAPI (get_db)
│   │
│   ├── models/                  # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── categories.py        # Category model
│   │   └── products.py          # Product model
│   │
│   ├── schemas.py               # Pydantic schemas
│   │
│   ├── routers/                 # API routers
│   │   ├── __init__.py
│   │   ├── categories.py        # Category endpoints
│   │   └── products.py          # Product endpoints
│   │
│   └── migrations/              # Alembic migrations
│       ├── versions/
│       ├── env.py
│       ├── README
│       └── script.py.mako
│
├── .gitignore
├── alembic.ini
├── README.md
├── requirements.txt
└── ecommerce.db                 # Local SQLite DB (ignored in git)
```


