# Backend Assessment Project

## Overview

This project is a scalable backend API built using FastAPI, PostgreSQL, and Redis.  
It demonstrates CRUD operations, caching, filtering, aggregation queries, and relational data handling between Users and Posts.

The application is fully asynchronous and designed with clean architecture principles suitable for production-grade systems.

---

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy (Async)
- asyncpg
- Redis
- Docker
- Pydantic

---

## Features

### 1. User CRUD Operations

- `POST /users` – Create a new user
- `GET /users` – Fetch all users (with pagination)
- `GET /users/{id}` – Fetch a single user
- `PUT /users/{id}` – Update a user
- `DELETE /users/{id}` – Delete a user

Pagination example:

```
GET /users?skip=0&limit=10
```

---

### 2. Redis Caching

- `GET /users` responses are cached in Redis
- Cache key format: `users:{page}:{limit}`
- Cache invalidates automatically when:
  - A user is created
  - A user is updated
  - A user is deleted

This reduces database load and improves performance.

---

### 3. Filtering and Search

Search users with query parameters:

```
GET /users/search?name=John&created_after=2025-01-01
```

Supports:
- Partial name matching
- Date-based filtering

---

### 4. Aggregation Endpoints

#### User Statistics

```
GET /users/stats
```

Returns:
- Total users
- Users created in the last 7 days

#### Post Statistics

```
GET /posts/stats
```

Returns:
- Number of posts per user

---

### 5. Posts and Relationships

- One user can have multiple posts
- Foreign key validation enforced
- Posts cannot be created for non-existing users

Endpoints:

- `POST /posts`
- `GET /posts?user_id=1`
- `GET /posts/stats`

---

## Database Schema

### Users Table

| Column      | Type      | Description        |
|------------|----------|--------------------|
| id         | Integer  | Primary Key        |
| name       | String   | Required           |
| email      | String   | Unique             |
| created_at | Timestamp| Auto-generated     |

---

### Posts Table

| Column      | Type      | Description                 |
|------------|----------|-----------------------------|
| id         | Integer  | Primary Key                 |
| user_id    | Integer  | Foreign Key → users.id      |
| title      | String   | Required                    |
| content    | String   | Required                    |
| created_at | Timestamp| Auto-generated              |

---

## Project Structure

```
app/
│
├── cache.py
├── database.py
├── main.py
├── models.py
├── schemas.py
│
└── routers/
    ├── users.py
    └── posts.py
```

---

## Setup Instructions

### 1. Clone the Repository

```
git clone https://github.com/hitesh911/officesolutionsassessment.git
cd officesolutionsassessment
```

---

### 2. Create Virtual Environment

Windows:

```
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install Dependencies

```
pip install fastapi uvicorn sqlalchemy asyncpg redis python-dotenv
```

---

### 4. Setup PostgreSQL

Create a database named:

```
officesolutions
```

Create a `.env` file:

```
DATABASE_URL=postgresql+asyncpg://postgres:yourpassword@localhost:5432/fastapi_db
REDIS_URL=redis://localhost:6379/0
```

---

### 5. Run Redis Using Docker

```
docker run -d -p 6379:6379 --name fastapi-redis redis
```

Verify:

```
docker ps
```

---

### 6. Run the Application

```
uvicorn app.main:app --reload
```


Access Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## Design Decisions

- Async architecture for scalability
- Redis caching to reduce DB load
- Database-level aggregation queries
- Proper foreign key validation
- Clean modular router-based structure
- Modern FastAPI lifespan event handling

---

## Error Handling

- 404 returned for non-existing users
- 400 returned for invalid foreign key references
- Database rollbacks handled properly
- No raw database exceptions exposed to clients

---

## Performance Considerations

- Non-blocking async DB operations
- Redis caching layer
- Pagination support
- Aggregation handled at DB level

---

## Future Improvements

- JWT Authentication
- Role-based authorization
- Rate limiting
- Logging middleware
- Unit and integration testing
- Docker Compose setup
- CI/CD pipeline

---

## Author

Developed as part of a backend technical assessment using FastAPI, PostgreSQL, and Redis.
