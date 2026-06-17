# Backend - Axon FastAPI API

This is the FastAPI-based Python backend for the Axon web application.

---

## 🛠️ Main Tech Stack
- **FastAPI**: Core async API router framework.
- **SQLAlchemy**: PostgreSQL ORM mapping.
- **Alembic**: Database migrations and category seeds.
- **SlowAPI**: Rate limiting decorator on controller endpoints.
- **Cloudinary**: File storage uploads.

---

## 🚀 Installation & Running

### 1. Virtual Environment Setup
Ensure you are in the `Backend` directory:
```bash
python -m venv venv
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# macOS / Linux:
source venv/bin/activate
```

### 2. Dependencies
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Database Migrations
Configure your database string in `.env`, then run:
```bash
# Apply migrations and seeds
python -m alembic upgrade head
```

### 4. Running Locally
```bash
python src/main.py
```
The server will run locally at `http://localhost:8000`. Interact with standard Swagger documentation via `http://localhost:8000/docs`.

---

## 🧪 Running Unit Tests
Unit tests use `pytest` with async support and an in-memory SQLite runner to protect local environments. Run tests with:
```bash
python -m pytest
```
