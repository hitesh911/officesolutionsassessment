# FastAPI Backend Assignment

## Overview

This project is a scalable backend API built using **FastAPI**, **PostgreSQL**, and **Redis**.  
It implements CRUD operations, caching, filtering, aggregation, and relational data handling between users and posts.

The project demonstrates:

- RESTful API design
- Async database integration
- Redis-based caching
- Filtering and aggregation queries
- Foreign key relationships
- Error handling and validation
- Production-ready project structure

---

## Tech Stack

- **FastAPI** – API framework
- **PostgreSQL** – Primary database
- **SQLAlchemy (Async)** – ORM
- **asyncpg** – Async PostgreSQL driver
- **Redis** – Caching layer
- **Docker** – Redis container
- **Pydantic** – Data validation

---

## Features Implemented

### 1. User CRUD APIs

- `POST /users` – Create user
- `GET /users` – List users (with pagination)
- `GET /users/{id}` – Get single user
- `PUT /users/{id}` – Update user
- `DELETE /users/{id}` – Delete user

Pagination:
