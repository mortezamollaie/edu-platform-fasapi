# 🎓 Edu Platform - Educational Web App

A simple and modern educational platform built with **FastAPI**, where users can register, browse available courses, and purchase them securely.

---

## 🚀 Features

- User registration and authentication via OTP
- Browse list of available courses
- View detailed course information
- Purchase courses
- JWT-based authentication
- Modular structure using FastAPI, SQLAlchemy, and SQLite (easily upgradeable to PostgreSQL)

---

## ⚙️ Tech Stack

- **Python**
- **FastAPI**
- **SQLAlchemy**
- **SQLite**
- **Pydantic**
- **JWT (Authentication)**
- **dotenv**

---

## 🏁 Getting Started

1. **Clone the repository:**

```bash
git clone https://github.com/mortezamollaie/edu-platform-fastapi.git
cd edu-platform
```

2. **Create and activate a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Set up the .env file:**

```env
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

5. **Run the project:**

```bash
uvicorn app.main:app --reload
```

Visit: http://localhost:8000

## 📚 API Documentation
Once the server is running, API documentation is automatically generated:

- Swagger UI: `/docs`

- Redoc: `/redoc`

## 📂 Project Structure
```bash
app/
├── api/                # API routes
├── core/               # Project settings and JWT
├── crud/               # Database logic
├── models/             # SQLAlchemy models
├── schemas/            # Pydantic schemas
├── services/           # Utilities (e.g., token generation, hashing)
└── main.py             # Entry point
```