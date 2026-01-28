# 📘 README.md

```markdown
# FastAPI Backend Assessment Project

## 📌 Project Overview

This project is a scalable backend API built using **FastAPI**, **PostgreSQL**, and **Redis**.

The application implements:

- Full CRUD operations for Users
- Caching using Redis
- Filtering and search endpoints
- Aggregation queries
- Relational data handling between Users and Posts
- Async architecture for performance and scalability

The goal of this project is to demonstrate backend API design, database integration, caching strategies, and clean architecture principles.

---

# 🏗️ Architecture Overview

This application follows a modular, layered structure:

- **Router Layer** → API endpoints
- **Schema Layer** → Data validation (Pydantic)
- **ORM Layer** → SQLAlchemy models
- **Database Layer** → Async PostgreSQL engine
- **Caching Layer** → Redis integration
- **Application Lifecycle Management** → FastAPI lifespan handler

All database interactions are asynchronous using `asyncpg`.

---

# 🛠️ Tech Stack

| Component | Technology |
|------------|------------|
| API Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy (Async) |
| DB Driver | asyncpg |
| Cache | Redis |
| Containerization | Docker |
| Validation | Pydantic |

---

# 📂 Project Structure

```

app/
│
├── main.py              # App entry point
├── database.py          # DB configuration
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── cache.py             # Redis caching layer
│
└── routers/
├── users.py         # User endpoints
└── posts.py         # Post endpoints

.env
README.md
DEVELOPER_DOCUMENTATION.md

```

---

# 🚀 Features Implemented

---

## ✅ Task 1 – CRUD API Endpoints

### Users

| Method | Endpoint | Description |
|--------|----------|------------|
| POST | `/users` | Create new user |
| GET | `/users` | Get all users (with pagination) |
| GET | `/users/{id}` | Get single user |
| PUT | `/users/{id}` | Update user |
| DELETE | `/users/{id}` | Delete user |

### Pagination

```

GET /users?skip=0&limit=10

```

---

## ✅ Task 2 – Redis Caching

- `GET /users` is cached
- Cache key format:
```

users:{skip}:{limit}

```
- Cache invalidation triggered on:
- User creation
- User update
- User deletion

This reduces database load for frequently accessed endpoints.

---

## ✅ Task 3 – Filtering & Aggregation

### Search Users

```

GET /users/search?name=John&created_after=2025-01-01

```

Supports:
- Name filtering (case insensitive)
- Created after date filtering

---

### User Statistics

```

GET /users/stats

```

Returns:
- Total users
- Users created in last 7 days

---

## ✅ Task 4 – Dynamic Data & Relationships

### Posts Table

- Linked to users via foreign key
- One user → many posts
- Foreign key validation enforced

### Post Endpoints

| Method | Endpoint | Description |
|--------|----------|------------|
| POST | `/posts` | Create post for user |
| GET | `/posts?user_id=1` | Fetch posts by user |
| GET | `/posts/stats` | Posts per user |

---

# 🗄️ Database Schema

## Users Table

| Column | Type | Description |
|--------|------|------------|
| id | Integer | Primary Key |
| name | String | Required |
| email | String | Unique |
| created_at | Timestamp | Auto-generated |

---

## Posts Table

| Column | Type | Description |
|--------|------|------------|
| id | Integer | Primary Key |
| user_id | Integer | Foreign Key → users.id |
| title | String | Required |
| content | String | Required |
| created_at | Timestamp | Auto-generated |

---

# ⚙️ Setup Instructions

---

## 1️⃣ Clone Repository

```

git clone <your_repo_url>
cd fastapi-backend

```

---

## 2️⃣ Create Virtual Environment

Windows:

```

python -m venv venv
venv\Scripts\activate

```

Mac/Linux:

```

python3 -m venv venv
source venv/bin/activate

```

---

## 3️⃣ Install Dependencies

```

pip install fastapi uvicorn sqlalchemy asyncpg redis python-dotenv

```

---

## 4️⃣ Setup PostgreSQL

Create a database:

```

fastapi_db

```

Update `.env`:

```

DATABASE_URL=postgresql+asyncpg://postgres:yourpassword@localhost:5432/fastapi_db
REDIS_URL=redis://localhost:6379/0

```

---

## 5️⃣ Run Redis (Docker)

```

docker run -d -p 6379:6379 --name fastapi-redis redis

```

Verify:

```

docker ps

```

---

## 6️⃣ Run Application

```

uvicorn app.main:app --reload

```

Open:

```

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

```

Swagger UI available for testing.

---

# 🧪 Example API Flow

1. Create user
2. Create post with valid `user_id`
3. Fetch users (cached)
4. Fetch posts by user
5. Check stats endpoints

---

# ⚡ Performance Considerations

- Fully async architecture
- Database-level aggregations
- Redis caching layer
- Pagination to reduce large payloads
- Explicit error handling
- Controlled foreign key validation

---

# 🧠 Design Decisions

- Used `asyncpg` for non-blocking DB operations
- Used Redis instead of in-memory cache to simulate production caching
- Implemented lifespan event handler (modern FastAPI pattern)
- Used modular routers for maintainability
- Enforced relational integrity at DB level

---

# 🛡️ Error Handling

- 404 for non-existing users
- 400 for invalid foreign key reference
- No raw database errors exposed
- Proper rollback on integrity errors

---

# 🔮 Future Improvements

- Authentication (JWT)
- Role-based authorization
- Unit & integration tests
- Logging middleware
- Rate limiting
- Docker Compose for full stack setup
- CI/CD integration
- API versioning

---

# 📖 Developer Documentation

See:
```

DEVELOPER_DOCUMENTATION.md

```

---

# 👨‍💻 Author

Developed as part of a backend technical assessment using FastAPI, PostgreSQL, and Redis.
```



