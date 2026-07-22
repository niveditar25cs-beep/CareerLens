# CareerLens Backend

A smart career opportunity platform backend built with **FastAPI**, **SQLAlchemy (async)**, and **SQLite**.

## 🚀 Quick Start

### 1. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS/Linux
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

Edit the `.env` file and set a strong `JWT_SECRET_KEY`.

### 4. Run the server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

Interactive docs: `http://127.0.0.1:8000/docs`

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Settings & environment config
│   ├── database/
│   │   ├── database.py      # Async SQLAlchemy engine & session
│   │   └── init_db.py       # Table creation on startup
│   ├── models/              # SQLAlchemy ORM models
│   ├── schemas/             # Pydantic request/response schemas
│   ├── routes/              # API route handlers
│   ├── services/            # Business logic (scraper, search, recommendations)
│   └── utils/               # Security, JWT, helpers
├── requirements.txt
├── .env
└── README.md
```

## 🔑 API Endpoints

| Prefix               | Description                  |
|-----------------------|------------------------------|
| `/api/auth`           | Register & login             |
| `/api/students`       | Student profile management   |
| `/api/opportunities`  | CRUD for career opportunities|
| `/api/recommendations`| Personalized suggestions     |
| `/api/dashboard`      | Dashboard summary metrics    |
| `/api/notifications`  | Student notifications        |
