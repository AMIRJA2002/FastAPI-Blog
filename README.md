# FastAPI Blog API

## Overview
This project is a **FastAPI-based Blog API** designed for managing blog posts, users, and comments. It supports RESTful operations, uses a database for persistence, and provides Docker support for deployment.

---

## Features
- User authentication and authorization by using PyJWT
- Blog post creation, retrieval, update, and deletion
- postgresql as database and SQLAlchemy as orm
- Database migrations using Alembic
- Easy deployment with Docker and Docker Compose
- Environment variable configuration for secure setup
- Comprehensive testing suite

---

## Prerequisites
Ensure you have the following installed:
- Python 3.10 or later
- Docker and Docker Compose (optional for containerized setup)
- A compatible OS (Ubuntu is recommended)

---

## Installation and Setup

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd data-co-lab_blog_api
```

### Step 2: Create your .env file 
```bash
mv env.example .env
```

### Step 3: Generate a secret key
```bash
echo "SECRET_KEY=$(openssl rand -hex 32)" >> .env
```

### Step 4: Spin up your Docker
```bash
docker compose up --build # docker-compose up --build for older version 
```

### Step 5: OpenAPI documentation
```bash
127.0.0.1:7070/docs 
```

---

## How to deploy
Move project file to server:
- make sure how setup .env file 
- spin up project's docker
- requests are served on port 7070.

---

## project structure

```bash
data-co-lab_blog_api/
│
├── app.py                 # Main application file
├── core/                  # Core application logic
    ├── init.py
    ├── users              # users code base and logic
    ├── post               # posts code base and logic 
├── config.py              # Application configuration
├── datebase.py            # Database initialization
├── dependencies.py        # Dependency management
├── alembic/               # Database migrations
├── tests/                 # Test suite
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables (excluded in version control)
```



