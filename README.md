# 🎓 Edu Platform - Educational Web App

A comprehensive educational platform built with **FastAPI**, featuring complete course management, user authentication, role-based permissions, and structured learning content.

---

## 🚀 Features

### 👤 User Management
- User registration and authentication via OTP
- JWT-based authentication system
- Role-based access control (Admin, Teacher, Student)
- Permission management system

### 📚 Course Management
- Create, update, delete, and retrieve courses
- Course organization with chapters and lectures
- Free and premium content support
- Multiple video sources (YouTube, Drive, Direct URL)
- Course search and filtering

### 🏗️ Content Structure
- **Courses**: Main educational content containers
- **Chapters**: Course subdivisions for better organization
- **Lectures**: Individual learning units with video content

### 🔐 Permission System
- Dynamic role and permission management
- Assign/remove permissions to roles
- Fine-grained access control

### 📱 API Features
- RESTful API design
- Comprehensive CRUD operations
- Automatic API documentation
- Input validation and error handling

---

## ⚙️ Tech Stack

- **Python 3.8+**
- **FastAPI** - Modern web framework
- **SQLAlchemy** - ORM for database operations
- **Alembic** - Database migration tool
- **SQLite** - Development database (easily upgradeable to PostgreSQL)
- **Pydantic** - Data validation and serialization
- **JWT** - Authentication tokens
- **python-dotenv** - Environment variable management

---

## 🏁 Getting Started

### 1. **Clone the repository:**

```bash
git clone https://github.com/mortezamollaie/edu-platform-fastapi.git
cd edu-platform
```

### 2. **Create and activate a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

### 4. **Set up the .env file:**

```env
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=postgresql://db_user:db_pass@localhost:5432/edu_db
```

### 5. **Initialize the database:**

```bash
# Create initial migration (if needed)
alembic revision --autogenerate -m "Initial migration"

# Apply migrations to database
alembic upgrade head
```

### 6. **Run the project:**

```bash
uvicorn app.main:app --reload
```

Visit: http://localhost:8000

---

## 🗄️ Database Management with Alembic

This project uses **Alembic** for database migrations. Here are the essential commands:

### Initialize Alembic (Already done)
```bash
alembic init alembic
```

### Create a new migration
```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Description of changes"

# Create empty migration file
alembic revision -m "Description of changes"
```

### Apply migrations
```bash
# Upgrade to latest migration
alembic upgrade head

# Upgrade to specific revision
alembic upgrade <revision_id>

# Upgrade one step forward
alembic upgrade +1
```

### Migration history and info
```bash
# Show current migration status
alembic current

# Show migration history
alembic history

# Show migration details
alembic show <revision_id>
```

### Downgrade migrations
```bash
# Downgrade one step
alembic downgrade -1

# Downgrade to specific revision
alembic downgrade <revision_id>

# Downgrade to base (empty database)
alembic downgrade base
```

### Migration workflow example
```bash
# 1. Make changes to your models in app/models/
# 2. Generate migration
alembic revision --autogenerate -m "Add new table or field"

# 3. Review the generated migration file in alembic/versions/
# 4. Apply the migration
alembic upgrade head
```

---

## 📚 API Documentation

Once the server is running, comprehensive API documentation is automatically generated:

- **Swagger UI**: http://localhost:8000/docs
- **Redoc**: http://localhost:8000/redoc

### Main API Endpoints

#### 🔐 Authentication
- `POST /api/v1/signup` - User registration
- `POST /api/v1/register` - Complete registration with OTP
- `POST /api/v1/login` - User login

#### 👥 User Management
- `GET /api/v1/users` - List users
- `GET /api/v1/users/{user_id}` - Get user details
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

#### 🎭 Roles & Permissions
- `GET /api/v1/roles` - List all roles
- `POST /api/v1/roles` - Create new role
- `GET /api/v1/roles/{role_id}` - Get role details
- `PUT /api/v1/roles/{role_id}` - Update role
- `DELETE /api/v1/roles/{role_id}` - Delete role
- `POST /api/v1/roles/{role_id}/permissions/add` - Add permissions to role
- `POST /api/v1/roles/{role_id}/permissions/remove` - Remove permissions from role
- `GET /api/v1/roles/{role_id}/permissions` - Get role permissions

#### 🔑 Permissions
- `GET /api/v1/permissions` - List all permissions
- `POST /api/v1/permissions` - Create new permission
- `GET /api/v1/permissions/{permission_id}` - Get permission details
- `PUT /api/v1/permissions/{permission_id}` - Update permission
- `DELETE /api/v1/permissions/{permission_id}` - Delete permission

#### 📚 Courses
- `GET /api/v1/courses` - List all courses
- `POST /api/v1/courses` - Create new course
- `GET /api/v1/courses/{slug}` - Get course details
- `PATCH /api/v1/courses/{slug}` - Update course
- `DELETE /api/v1/courses/{slug}` - Delete course
- `GET /api/v1/courses/{slug}/chapters` - Get course chapters

#### 📖 Chapters
- `GET /api/v1/chapters` - List all chapters
- `POST /api/v1/chapters` - Create new chapter
- `GET /api/v1/chapters/{slug}` - Get chapter details
- `PATCH /api/v1/chapters/{slug}` - Update chapter
- `DELETE /api/v1/chapters/{slug}` - Delete chapter
- `GET /api/v1/chapters/{slug}/lectures` - Get chapter lectures

#### 🎬 Lectures
- `GET /api/v1/lectures` - List all lectures
- `POST /api/v1/lectures` - Create new lecture
- `GET /api/v1/lectures/{slug}` - Get lecture details
- `PATCH /api/v1/lectures/{slug}` - Update lecture
- `DELETE /api/v1/lectures/{slug}` - Delete lecture

---

## 📂 Project Structure

```
edu_platform/
├── 📁 alembic/                 # Database migrations
│   ├── 📁 versions/            # Migration files
│   ├── 📄 env.py              # Alembic configuration
│   └── 📄 script.py.mako      # Migration template
├── 📁 app/                     # Main application
│   ├── 📁 api/                # API routes and dependencies
│   │   ├── 📁 api_v1/         # Version 1 API endpoints
│   │   │   ├── 📄 account.py  # Authentication endpoints
│   │   │   ├── 📄 user.py     # User management
│   │   │   ├── 📄 roles.py    # Role management
│   │   │   ├── 📄 permissions.py # Permission management
│   │   │   ├── 📄 courses.py  # Course endpoints
│   │   │   ├── 📄 chapters.py # Chapter endpoints
│   │   │   └── 📄 lectures.py # Lecture endpoints
│   │   └── 📄 deps.py         # API dependencies
│   ├── 📁 core/               # Core configurations
│   │   └── 📄 config.py       # App settings
│   ├── 📁 crud/               # Database operations
│   │   ├── 📄 account.py      # User, role, permission CRUD
│   │   ├── 📄 courses.py      # Course CRUD operations
│   │   ├── 📄 chapters.py     # Chapter CRUD operations
│   │   └── 📄 lectures.py     # Lecture CRUD operations
│   ├── 📁 db/                 # Database configuration
│   │   ├── 📄 base.py         # Database models import
│   │   ├── 📄 base_class.py   # Base model class
│   │   ├── 📄 init_db.py      # Database initialization
│   │   └── 📄 session.py      # Database session
│   ├── 📁 models/             # SQLAlchemy models
│   │   ├── 📄 account.py      # User, Role, Permission models
│   │   ├── 📄 learning.py     # Course, Chapter, Lecture models
│   │   └── 📄 user.py         # User model extensions
│   ├── 📁 schemas/            # Pydantic schemas
│   │   ├── 📄 account.py      # Authentication schemas
│   │   └── 📄 learning.py     # Learning content schemas
│   ├── 📁 services/           # Business logic services
│   │   ├── 📄 hash_password.py # Password hashing
│   │   └── 📄 token_management_service.py # JWT handling
│   ├── 📄 dependencies.py     # Global dependencies
│   └── 📄 main.py            # FastAPI application entry point
├── 📄 alembic.ini             # Alembic configuration file
├── 📄 requirements.txt        # Python dependencies
├── 📄 db.sqlite3             # SQLite database file
└── 📄 README.md              # Project documentation
```

---

## 🔧 Development Guidelines

### Adding New Features

1. **Models**: Add/modify models in `app/models/`
2. **Schemas**: Create Pydantic schemas in `app/schemas/`
3. **CRUD**: Implement database operations in `app/crud/`
4. **API**: Create endpoints in `app/api/api_v1/`
5. **Migration**: Generate and apply migrations with Alembic

### Database Changes Workflow

1. Modify models in `app/models/`
2. Generate migration: `alembic revision --autogenerate -m "Description"`
3. Review generated migration file
4. Apply migration: `alembic upgrade head`

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Morteza Mollaei**  
GitHub: [@mortezamollaie](https://github.com/mortezamollaie)