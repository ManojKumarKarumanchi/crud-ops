# FastAPI CRUD Application with JWT Authentication

**Production-ready RESTful API with authentication, async PostgreSQL, and comprehensive CRUD operations.**

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://www.postgresql.org/)

---

## 📋 Table of Contents

- [About](#about)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Authentication Flow](#authentication-flow)
- [Testing](#testing)
- [Production Deployment](#production-deployment)
- [Project Structure](#project-structure)

---

**Exercise Requirements:**
- ✅ Authenticated CRUD APIs with JWT
- ✅ Relational database with proper schema (6 tables/6 columns)
- ✅ Clean, scalable architecture
- ✅ Production-ready code quality
- ✅ Cloud deployment ready
- ✅ Comprehensive documentation

**Completed By:** April 22, 2026

---

## ✨ Features

### Core Features
- 🔐 **JWT Authentication** - Secure token-based auth with OAuth2
- 📝 **Full CRUD Operations** - Create, Read, Update, Delete for all entities
- 🗄️ **Async PostgreSQL** - High-performance async database operations
- 🆔 **UUID Primary Keys** - Globally unique identifiers
- ⏰ **Auto Timestamps** - Automatic `created_at` and `updated_at` tracking
- ✅ **Data Validation** - Pydantic schemas for request/response validation
- 📊 **API Versioning** - `/v1/` prefix for future compatibility

### Security Features
- 🔒 **Password Hashing** - Bcrypt with 12 rounds
- 🎫 **Token Expiration** - Configurable JWT expiry (30 min default)
- 🛡️ **Protected Routes** - Middleware-based authentication
- 👑 **Role-Based Access Control (RBAC)** - Admin-only endpoints with `is_admin` flag
- 🚫 **Input Validation** - Prevent injection attacks (8-72 char passwords)
- 📝 **Audit Logging** - Track all authentication events
- 🔄 **Exception Handling** - Production-grade error handling with rollback
- 🔐 **Admin Dashboard** - Complete system overview for administrators

### Developer Experience
- 📖 **Interactive API Docs** - Swagger UI and ReDoc
- 🔍 **Comprehensive Logging** - Console + rotating file logs (10MB, 5 backups)
- ⚡ **Hot Reload** - Development mode with auto-reload
- 🧪 **Database Testing** - Connection test utilities
- 🐳 **Docker Ready** - Containerization support

---

## 🏗️ Architecture

### System Flow

```mermaid
graph TB
    Client[Client/Browser] -->|HTTP Request| API[FastAPI Application]
    API -->|Authentication| JWT[JWT Middleware]
    JWT -->|Valid Token| Router[API Routes v1]
    JWT -->|Invalid| Error[401 Unauthorized]
    Router -->|Business Logic| Service[Service Layer]
    Service -->|Database Ops| DB[(PostgreSQL)]
    Service -->|Response| Router
    Router -->|JSON| Client
    
    style API fill:#green
    style JWT fill:#orange
    style Service fill:#blue
    style DB fill:#purple
```

### Authentication Flow

```mermaid
sequenceDiagram
    participant User
    participant API
    participant Auth
    participant DB
    
    User->>API: POST /v1/auth/register
    API->>Auth: Hash Password (bcrypt)
    Auth->>DB: Store User (UUID, is_admin=False)
    DB-->>API: User Created
    API-->>User: 201 Created + User Data
    
    User->>API: POST /v1/auth/login (email+password)
    API->>DB: Get User by Email
    DB-->>API: User Data (with is_admin flag)
    API->>Auth: Verify Password
    Auth->>Auth: Generate JWT Token (includes email)
    Auth-->>User: Access Token (30min)
    
    User->>API: GET /v1/users/me (+ Bearer Token)
    API->>Auth: Validate JWT Token
    Auth->>DB: Get User by Email from Token
    DB-->>API: User Data
    API-->>User: User Profile
```

### CRUD Operations Flow

```mermaid
graph LR
    A[Client Request] --> B[FastAPI Router]
    B --> C{Auth Required?}
    C -->|Yes| D[JWT Validation]
    C -->|No| E[Service Layer]
    D -->|Valid| E
    D -->|Invalid| F[401 Error]
    E --> G{Operation}
    G -->|Create| H[INSERT to DB]
    G -->|Read| I[SELECT from DB]
    G -->|Update| J[UPDATE in DB]
    G -->|Delete| K[DELETE from DB]
    H --> L[Update Timestamp]
    J --> L
    L --> M[Response Schema]
    I --> M
    K --> M
    M --> N[JSON Response]
    N --> A
```

### Admin Authorization Flow

```mermaid
graph TD
    A[Client Request to /v1/admin/*] --> B[JWT Middleware]
    B -->|No Token| C[401 Unauthorized]
    B -->|Valid Token| D[Extract User from Token]
    D --> E[Get User from Database]
    E --> F{Check is_admin Flag}
    F -->|is_admin = False| G[403 Forbidden]
    F -->|is_admin = True| H[Admin Route Handler]
    H --> I{Admin Operation}
    I -->|Dashboard| J[Get System Statistics]
    I -->|List Users| K[Get All Users + Pagination]
    I -->|List Items| L[Get All Items + Filters]
    I -->|User Count| M[Count Active/Inactive Users]
    I -->|Item Count| N[Count Available Items by Category]
    J --> O[Return JSON Response]
    K --> O
    L --> O
    M --> O
    N --> O
    O --> A
    
    style F fill:#orange
    style G fill:#red
    style H fill:#green
```

### Complete Authentication & Authorization Flow

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant JWT_Middleware
    participant Admin_Check
    participant Service
    participant DB
    
    rect rgb(200, 220, 250)
    Note over Client,DB: Regular User Flow
    Client->>API: POST /v1/auth/login (user credentials)
    API->>DB: Verify credentials
    DB-->>API: User data (is_admin=False)
    API->>JWT_Middleware: Generate JWT token
    JWT_Middleware-->>Client: Access token
    
    Client->>API: GET /v1/items/ (+ Bearer token)
    API->>JWT_Middleware: Validate token
    JWT_Middleware->>DB: Get user from token
    DB-->>JWT_Middleware: User data
    JWT_Middleware-->>API: User authenticated
    API->>Service: Get items
    Service->>DB: SELECT items
    DB-->>Service: Items data
    Service-->>API: Items list
    API-->>Client: 200 OK + Items
    end
    
    rect rgb(255, 230, 230)
    Note over Client,DB: Regular User Tries Admin Endpoint (DENIED)
    Client->>API: GET /v1/admin/users (+ user token)
    API->>JWT_Middleware: Validate token
    JWT_Middleware->>DB: Get user from token
    DB-->>JWT_Middleware: User data (is_admin=False)
    JWT_Middleware-->>API: User authenticated
    API->>Admin_Check: Check is_admin flag
    Admin_Check-->>API: DENIED (is_admin=False)
    API-->>Client: 403 Forbidden
    end
    
    rect rgb(230, 255, 230)
    Note over Client,DB: Admin User Flow (ALLOWED)
    Client->>API: POST /v1/auth/login (admin credentials)
    API->>DB: Verify credentials
    DB-->>API: User data (is_admin=True)
    API->>JWT_Middleware: Generate JWT token
    JWT_Middleware-->>Client: Access token
    
    Client->>API: GET /v1/admin/dashboard (+ admin token)
    API->>JWT_Middleware: Validate token
    JWT_Middleware->>DB: Get user from token
    DB-->>JWT_Middleware: User data (is_admin=True)
    JWT_Middleware-->>API: User authenticated
    API->>Admin_Check: Check is_admin flag
    Admin_Check-->>API: ALLOWED (is_admin=True)
    API->>Service: Get dashboard data
    Service->>DB: Get user stats, item stats, recent activity
    DB-->>Service: Aggregated data
    Service-->>API: Dashboard summary
    API-->>Client: 200 OK + Dashboard data
    end
```

---

## 📦 Prerequisites

### Required Software

| Software | Version | Purpose | Installation |
|----------|---------|---------|--------------|
| Python | 3.12+ | Runtime environment | [python.org](https://www.python.org/downloads/) |
| PostgreSQL | 15+ | Database | [postgresql.org](https://www.postgresql.org/download/) |
| uv or pip | Latest | Package manager | `pip install uv` |
| Git | Latest | Version control | [git-scm.com](https://git-scm.com/) |

### Optional Tools
- **Docker & Docker Compose** - For containerized DB
- **Postman or HTTPie** - API testing
- **DBeaver or pgAdmin** - Database GUI
- **VS Code** - Recommended IDE

---

## 🚀 Installation

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd crud
```

### Step 2: Set Up Python Environment

#### Option A: Using uv (Recommended - 10x Faster)

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows: irm https://astral.sh/uv/install.ps1 | iex

# Create virtual environment with Python 3.12
uv venv --python 3.12

# Activate virtual environment
# Windows (PowerShell)
.venv\Scripts\activate
# Windows (CMD)
.venv\Scripts\activate.bat
# Linux/Mac
source .venv/bin/activate

# Install all dependencies
uv pip install -r requirements.txt
```

#### Option B: Using Standard pip

```bash
# Ensure Python 3.12 is installed
python3.12 --version

# Create virtual environment
python3.12 -m venv .venv

# Activate virtual environment
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Set Up PostgreSQL Database

#### Option A: Docker (Recommended - Easiest Setup)

```bash
# Start PostgreSQL container
docker run --name postgres-crud \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_DB=crud_db \
  -p 5432:5432 \
  -d postgres:15

# Verify container is running
docker ps

# Check logs
docker logs postgres-crud
```

#### Option B: Local PostgreSQL Installation

**Windows:**
```powershell
# Download installer from postgresql.org
# After installation, open SQL Shell (psql)
CREATE DATABASE crud_db;
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo -u postgres psql
CREATE DATABASE crud_db;
\q
```

**macOS:**
```bash
brew install postgresql@15
brew services start postgresql@15
createdb crud_db
```

### Step 4: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Generate secure secret key
python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))" >> .env

# Edit .env with your settings
# Windows: notepad .env
# Linux/Mac: nano .env
```

### Step 5: Test Database Connection

```bash
# Run comprehensive connection test
python test_db_connection.py

# Expected output:
# ============================================================
# Testing asyncpg Connection
# ============================================================
# [OK] Connected to PostgreSQL
# [OK] Database: crud_db
# [OK] User: postgres
# [OK] Version: PostgreSQL 15.x...
# 
# Tables in database:
#   (no tables yet - will be created on app startup)
# 
# [OK] Connection test passed
# 
# ============================================================
# Testing SQLAlchemy Engine
# ============================================================
# [OK] SQLAlchemy engine works
# [OK] Test query result: 1
# 
# ============================================================
# Test Summary
# ============================================================
# asyncpg connection: PASS
# SQLAlchemy engine: PASS
# 
# [SUCCESS] Database ready for application
```

---

## ⚙️ Configuration

### Environment Variables

Create `.env` file in project root:

```bash
# Database Configuration
DATABASE_URL=postgresql+asyncpg://username:password@host:port/database

# JWT Authentication Configuration
# Generate with: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=your-secret-key-change-in-production-64-chars-recommended
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Settings
APP_NAME=CRUD API
APP_VERSION=1.0.0
DEBUG=False
```

### Security Configuration

```bash
# Generate cryptographically secure secret key
python -c "import secrets; print(secrets.token_hex(32))"
# Output: eccfa8aab8387b8c249acfbac68bdfd18b8f6ea1c6d7839b5ecaec15761c385c

# Update .env
SECRET_KEY=eccfa8aab8387b8c249acfbac68bdfd18b8f6ea1c6d7839b5ecaec15761c385c
```

**⚠️ SECURITY WARNING:**
- Never commit `.env` to version control
- Use different keys for dev/staging/production
- Rotate keys periodically
- Store production keys in secure vaults (AWS Secrets Manager, HashiCorp Vault)

---

## 🏃 Running the Application

### Development Mode (Auto-reload)

```bash
# Method 1: Using main.py
python main.py

# Method 2: Using uvicorn CLI (with hot reload)
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Method 3: Custom host/port
uvicorn app:app --reload --host 127.0.0.1 --port 8080
```

### Production Mode

```bash
# Single worker (basic)
uvicorn app:app --host 0.0.0.0 --port 8000 --no-reload

# Multiple workers (recommended for production)
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4

# With specific log level
uvicorn app:app --host 0.0.0.0 --port 8000 --log-level info
```

### Application Startup

On startup, you'll see:

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

Tables are automatically created on first startup:
- `users` table (UUID id, email, hashed_password, full_name, is_active, is_admin, created_at, updated_at)
- `items` table (UUID id, title, description, price, category, is_available, created_at, updated_at)

### Seeding Test Data

To populate the database with realistic test data including the admin user:

```bash
# Reset and seed database
python reset_db.py    # Drops and recreates all tables
python seed_database.py  # Creates admin + 6 users + 6 items
```

**Seeded Data:**
- **1 Admin User:**
  - Email: `admin`
  - Password: `adminpass123`
  - Role: Administrator (full access)

- **6 Regular Users:**
  - Random realistic names and emails
  - Password: `Test@123` (same for all test users)
  - Example: `gillsylvia@example.org`

- **6 Items (One per category):**
  - Electronics (e.g., Samsung Galaxy S24 Ultra, Rs.1,299.99)
  - Books (e.g., Atomic Habits, Rs.5.99)
  - Clothing (e.g., Levi's 501 Jeans, Rs.39.99)
  - Home & Kitchen (e.g., Philips Air Fryer, Rs.159.99)
  - Sports & Fitness (e.g., Yonex Badminton Racket, Rs.169.99)
  - Toys & Games (e.g., LEGO Creator Set, Rs.129.99)

### Access Points

| Service | URL | Description |
|---------|-----|-------------|
| **API Root** | http://localhost:8000 | Welcome message + version |
| **Health Check** | http://localhost:8000/health | Service health status |
| **Swagger UI** | http://localhost:8000/docs | Interactive API documentation |
| **ReDoc** | http://localhost:8000/redoc | Alternative API documentation |
| **OpenAPI Schema** | http://localhost:8000/openapi.json | Raw OpenAPI specification |

---

## 📚 API Documentation

### Quick Reference

#### Public Endpoints
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/v1/auth/register` | ❌ | Register new user |
| POST | `/v1/auth/login` | ❌ | Login and get JWT token |

#### User Endpoints (Authentication Required)
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/v1/users/me` | ✅ | Get current user profile |
| GET | `/v1/items/` | ✅ | List all items (paginated) |
| GET | `/v1/items/{id}` | ✅ | Get single item by UUID |
| POST | `/v1/items/` | ✅ | Create new item |
| PUT | `/v1/items/{id}` | ✅ | Update existing item |
| DELETE | `/v1/items/{id}` | ✅ | Delete item |

#### Admin Endpoints (Admin Role Required)
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/v1/admin/dashboard` | 🔐 Admin | Complete system overview with statistics |
| GET | `/v1/admin/users` | 🔐 Admin | List all users (paginated) |
| GET | `/v1/admin/users/count` | 🔐 Admin | User statistics (total, active, admins) |
| GET | `/v1/admin/items` | 🔐 Admin | List all items (paginated, filterable) |
| GET | `/v1/admin/items/count` | 🔐 Admin | Item statistics by category |

### Authentication Endpoints

#### 1. Register New User

```http
POST /v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "John Doe"
}
```

**Response (201 Created):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2026-04-20T10:00:00",
  "updated_at": "2026-04-20T10:00:00"
}
```

**Validation Rules:**
- Email: Valid email format (EmailStr)
- Password: 8-72 characters (bcrypt limit)
- Full name: Optional

#### 2. Login (Get JWT Token)

```http
POST /v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=password123
```

**Note:** `username` field should contain your **email address**.

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNjE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
  "token_type": "bearer"
}
```

**Token Details:**
- Algorithm: HS256
- Expiration: 30 minutes (configurable)
- Payload: `{"sub": "email", "exp": timestamp}`

### Protected Endpoints

**Authentication Required:** All endpoints below require `Authorization: Bearer <token>` header.

#### 3. Get Current User Profile

```http
GET /v1/users/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response (200 OK):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2026-04-20T10:00:00",
  "updated_at": "2026-04-20T10:00:00"
}
```

#### 4. List Items (with Pagination)

```http
GET /v1/items/?skip=0&limit=100
Authorization: Bearer <token>
```

**Query Parameters:**
- `skip`: Number of items to skip (default: 0)
- `limit`: Max items to return (default: 100, max: 100)

**Response (200 OK):**
```json
[
  {
    "id": "789e0123-e89b-12d3-a456-426614174001",
    "title": "Product Name",
    "description": "Product description",
    "price": 1000,
    "category": "Electronics",
    "is_available": true,
    "created_at": "2026-04-20T10:00:00",
    "updated_at": "2026-04-20T10:00:00"
  }
]
```

#### 5. Create Item

```http
POST /v1/items/
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Wireless Mouse",
  "description": "Ergonomic wireless mouse with USB receiver",
  "price": 2999,
  "category": "Electronics",
  "is_available": true
}
```

**Field Validation:**
- `title`: 1-255 characters, required
- `description`: Optional text
- `price`: Integer >= 0 (in cents), required
- `category`: Optional, max 100 chars
- `is_available`: Boolean, default true

**Response (201 Created):**
```json
{
  "id": "789e0123-e89b-12d3-a456-426614174001",
  "title": "Wireless Mouse",
  "description": "Ergonomic wireless mouse with USB receiver",
  "price": 2999,
  "category": "Electronics",
  "is_available": true,
  "created_at": "2026-04-20T10:00:00",
  "updated_at": "2026-04-20T10:00:00"
}
```

#### 6. Update Item

```http
PUT /v1/items/789e0123-e89b-12d3-a456-426614174001
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Wireless Mouse Pro",
  "price": 3499
}
```

**Note:** Only provided fields are updated. `updated_at` is automatically set.

**Response (200 OK):**
```json
{
  "id": "789e0123-e89b-12d3-a456-426614174001",
  "title": "Wireless Mouse Pro",
  "description": "Ergonomic wireless mouse with USB receiver",
  "price": 3499,
  "category": "Electronics",
  "is_available": true,
  "created_at": "2026-04-20T10:00:00",
  "updated_at": "2026-04-20T11:30:00"
}
```

#### 7. Delete Item

```http
DELETE /v1/items/789e0123-e89b-12d3-a456-426614174001
Authorization: Bearer <token>
```

**Response (204 No Content)**

---

### Admin-Only Endpoints

**⚠️ Admin Authorization Required:** All endpoints below require a valid JWT token with `is_admin=True`. Regular users receive `403 Forbidden`.

**Admin Credentials:**
- Email: `admin`
- Password: `adminpass123`

#### 8. Admin Dashboard (Complete Overview)

```http
GET /v1/admin/dashboard
Authorization: Bearer <admin-token>
```

**Response (200 OK):**
```json
{
  "statistics": {
    "users": {
      "total": 8,
      "active": 7,
      "inactive": 1,
      "admins": 1
    },
    "items": {
      "total": 6,
      "available": 5,
      "unavailable": 1,
      "by_category": {
        "Electronics": 1,
        "Books": 1,
        "Clothing": 1,
        "Home & Kitchen": 1,
        "Sports & Fitness": 1,
        "Toys & Games": 1
      }
    }
  },
  "recent_users": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "email": "recent@example.com",
      "full_name": "Recent User",
      "is_active": true,
      "is_admin": false,
      "created_at": "2026-04-20T15:30:00"
    }
  ],
  "recent_items": [
    {
      "id": "789e0123-e89b-12d3-a456-426614174001",
      "title": "Sony WH-1000XM5 Wireless Headphones",
      "category": "Electronics",
      "price": 29999,
      "is_available": true,
      "created_at": "2026-04-20T15:00:00"
    }
  ]
}
```

#### 9. List All Users (Admin)

```http
GET /v1/admin/users?skip=0&limit=100
Authorization: Bearer <admin-token>
```

**Query Parameters:**
- `skip`: Number of users to skip (default: 0)
- `limit`: Max users to return (default: 100, max: 500)

**Response (200 OK):**
```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "user@example.com",
    "full_name": "John Doe",
    "is_active": true,
    "is_admin": false,
    "created_at": "2026-04-20T10:00:00",
    "updated_at": "2026-04-20T10:00:00"
  }
]
```

#### 10. User Statistics (Admin)

```http
GET /v1/admin/users/count
Authorization: Bearer <admin-token>
```

**Response (200 OK):**
```json
{
  "total_users": 8,
  "active_users": 7,
  "inactive_users": 1,
  "admin_users": 1
}
```

#### 11. List All Items (Admin)

```http
GET /v1/admin/items?skip=0&limit=100&category=Electronics&available_only=true
Authorization: Bearer <admin-token>
```

**Query Parameters:**
- `skip`: Number of items to skip (default: 0)
- `limit`: Max items to return (default: 100, max: 500)
- `category`: Filter by category (optional)
- `available_only`: Only return available items (optional, default: false)

**Response (200 OK):**
```json
[
  {
    "id": "789e0123-e89b-12d3-a456-426614174001",
    "title": "Samsung Galaxy S24 Ultra 5G",
    "description": "Flagship smartphone with 200MP camera...",
    "price": 129999,
    "category": "Electronics",
    "is_available": true,
    "created_at": "2026-04-20T10:00:00",
    "updated_at": "2026-04-20T10:00:00"
  }
]
```

#### 12. Item Statistics (Admin)

```http
GET /v1/admin/items/count
Authorization: Bearer <admin-token>
```

**Response (200 OK):**
```json
{
  "total_items": 6,
  "available_items": 5,
  "unavailable_items": 1,
  "items_by_category": {
    "Electronics": 1,
    "Books": 1,
    "Clothing": 1,
    "Home & Kitchen": 1,
    "Sports & Fitness": 1,
    "Toys & Games": 1
  }
}
```

#### Admin Authorization Error (Regular User)

When a regular user tries to access admin endpoints:

```http
GET /v1/admin/dashboard
Authorization: Bearer <regular-user-token>
```

**Response (403 Forbidden):**
```json
{
  "detail": "Admin access required. Only administrators can access this resource."
}
```

---

## 🔐 Authentication Flow

### Method 1: Using Swagger UI (Easiest)

1. **Navigate to Swagger UI**
   ```
   http://localhost:8000/docs
   ```

2. **Register a New User**
   - Scroll to `POST /v1/auth/register`
   - Click "Try it out"
   - Fill in request body:
     ```json
     {
       "email": "demo@test.com",
       "password": "password123",
       "full_name": "Demo User"
     }
     ```
   - Click "Execute"
   - Verify 201 response

3. **Authorize (Get Token)**
   - Click 🔒 **"Authorize"** button (top right)
   - Enter credentials:
     - **username**: demo@test.com (⚠️ use your email)
     - **password**: password123
     - **client_id**: (leave empty)
   - Click "Authorize"
   - Click "Close"

4. **Test Protected Endpoints**
   - All endpoints with 🔒 icon are now accessible
   - Try `GET /v1/users/me`
   - Should return your profile data

### Method 2: Using cURL

```bash
# Step 1: Register
curl -X POST http://localhost:8000/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email":"test@example.com",
    "password":"password123",
    "full_name":"Test User"
  }'

# Step 2: Login and save token
TOKEN=$(curl -X POST http://localhost:8000/v1/auth/login \
  -d "username=test@example.com&password=password123" \
  | jq -r '.access_token')

# Step 3: Use token to access protected endpoint
curl http://localhost:8000/v1/users/me \
  -H "Authorization: Bearer $TOKEN"

# Step 4: Create an item
curl -X POST http://localhost:8000/v1/items/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title":"Test Product",
    "price":1000,
    "category":"Test"
  }'

# Step 5: List all items
curl http://localhost:8000/v1/items/ \
  -H "Authorization: Bearer $TOKEN"

# Step 6: Login as admin
ADMIN_TOKEN=$(curl -X POST http://localhost:8000/v1/auth/login \
  -d "username=admin&password=adminpass123" \
  | jq -r '.access_token')

# Step 7: Access admin dashboard
curl http://localhost:8000/v1/admin/dashboard \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Step 8: Try admin endpoint with regular user token (will fail with 403)
curl http://localhost:8000/v1/admin/users/count \
  -H "Authorization: Bearer $TOKEN"
```

### Method 3: Using HTTPie

```bash
# Install HTTPie
pip install httpie

# Register
http POST :8000/v1/auth/register \
  email=test@test.com \
  password=password123 \
  full_name="Test User"

# Login (save token)
http -f POST :8000/v1/auth/login \
  username=test@test.com \
  password=password123

# Use token (replace TOKEN)
http :8000/v1/users/me \
  "Authorization: Bearer TOKEN"

# Create item
http POST :8000/v1/items/ \
  "Authorization: Bearer TOKEN" \
  title="Product" \
  price:=1000
```

### Method 4: Using Python Requests

```python
import requests

BASE_URL = "http://localhost:8000"

# Register
response = requests.post(
    f"{BASE_URL}/v1/auth/register",
    json={
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User"
    }
)
print("Register:", response.status_code)

# Login
response = requests.post(
    f"{BASE_URL}/v1/auth/login",
    data={
        "username": "test@example.com",
        "password": "password123"
    }
)
token = response.json()["access_token"]
print("Token:", token[:50] + "...")

# Get current user
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(f"{BASE_URL}/v1/users/me", headers=headers)
print("User:", response.json())

# Create item
response = requests.post(
    f"{BASE_URL}/v1/items/",
    headers=headers,
    json={
        "title": "Test Product",
        "price": 1000,
        "category": "Test"
    }
)
print("Item created:", response.json())

# Admin login
response = requests.post(
    f"{BASE_URL}/v1/auth/login",
    data={
        "username": "admin",
        "password": "adminpass123"
    }
)
admin_token = response.json()["access_token"]
print("Admin token:", admin_token[:50] + "...")

# Get admin dashboard
admin_headers = {"Authorization": f"Bearer {admin_token}"}
response = requests.get(f"{BASE_URL}/v1/admin/dashboard", headers=admin_headers)
print("Dashboard:", response.json())

# Regular user tries admin endpoint (will fail)
response = requests.get(f"{BASE_URL}/v1/admin/users/count", headers=headers)
print("Regular user accessing admin endpoint:", response.status_code, response.json())
```


### Production Environment Variables

```bash
# .env.production
DATABASE_URL=postgresql+asyncpg://user:password@prod-db.example.com:5432/prod_db
SECRET_KEY=<64-character-random-string>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=False
APP_NAME=Production API
APP_VERSION=1.0.0
```

### Docker Configuration

**Dockerfile Features:**
- ✅ Multi-stage build (smaller final image ~150MB vs 1GB+)
- ✅ Non-root user for security (appuser)
- ✅ Health check endpoint integration
- ✅ Production-ready with 4 workers
- ✅ Includes utility scripts (reset_db.py, seed_database.py)
- ✅ Optimized layer caching

**docker-compose.yml Features:**
- ✅ PostgreSQL 15 with persistent volumes
- ✅ Health checks for both services
- ✅ Automatic restart policies
- ✅ Isolated network for service communication
- ✅ Environment variable configuration
- ✅ Optional pgAdmin integration (commented out)

### Deployment Options

#### Option 1: Docker Deployment (Single Container)

```bash
# Build image
docker build -t crud-api:latest .

# Run container (requires external PostgreSQL)
docker run -d \
  --name crud-api \
  -p 8000:8000 \
  -e DATABASE_URL="postgresql+asyncpg://user:pass@host:5432/crud_db" \
  -e SECRET_KEY="your-secret-key-here" \
  -e ALGORITHM="HS256" \
  -e ACCESS_TOKEN_EXPIRE_MINUTES="30" \
  --restart unless-stopped \
  crud-api:latest

# Check logs
docker logs -f crud-api

# Stop and remove
docker stop crud-api
docker rm crud-api
```

#### Option 2: Docker Compose (Recommended - Complete Stack)

The `docker-compose.yml` includes:
- PostgreSQL 15 database with health checks
- FastAPI API with 4 workers
- Automatic database connection on startup
- Persistent data volumes
- Health checks for both services
- Optimized networking

**Quick Start:**

```bash
# Generate secure secret key (optional - has default)
export SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# Start all services (database + API)
docker-compose up -d

# View logs
docker-compose logs -f api

# Check service status
docker-compose ps

# Expected output:
# NAME           IMAGE           STATUS         PORTS
# crud-api       crud-api        Up (healthy)   0.0.0.0:8000->8000/tcp
# crud-postgres  postgres:15     Up (healthy)   0.0.0.0:5432->5432/tcp
```

**Database Operations:**

```bash
# Seed database (create admin + test data)
docker-compose exec api python seed_database.py

# Reset database (drop and recreate tables)
docker-compose exec api python reset_db.py

# Access PostgreSQL CLI
docker-compose exec db psql -U postgres -d crud_db

# Backup database
docker-compose exec db pg_dump -U postgres crud_db > backup.sql

# Restore database
docker-compose exec -T db psql -U postgres crud_db < backup.sql
```

**Service Management:**

```bash
# Stop services (keeps containers)
docker-compose stop

# Start stopped services
docker-compose start

# Restart services
docker-compose restart

# Stop and remove containers (keeps volumes)
docker-compose down

# Stop and remove everything including volumes (⚠️ deletes data)
docker-compose down -v

# Rebuild images and restart
docker-compose up -d --build

# View resource usage
docker-compose stats
```

**Troubleshooting:**

```bash
# Check API logs
docker-compose logs api

# Check database logs
docker-compose logs db

# Follow logs in real-time
docker-compose logs -f

# Execute commands inside API container
docker-compose exec api bash

# Check database connection from API
docker-compose exec api python test_db_connection.py

# Test API health
curl http://localhost:8000/health
```

**Production Configuration:**

Create `.env` file for production:

```bash
# .env
SECRET_KEY=your-production-secret-key-64-characters-long
DATABASE_URL=postgresql+asyncpg://postgres:your-strong-password@db:5432/crud_db
```

Update `docker-compose.yml`:

```yaml
services:
  db:
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
  
  api:
    environment:
      DATABASE_URL: ${DATABASE_URL}
      SECRET_KEY: ${SECRET_KEY}
```

Start with environment file:

```bash
docker-compose --env-file .env up -d
```

#### Option 3: Cloud Platform Deployment

**Railway:**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and init
railway login
railway init

# Deploy
railway up

# Add PostgreSQL
railway add postgresql

# Configure environment variables in Railway dashboard
```

**Render:**
1. Connect GitHub repository
2. Create Web Service
3. Add PostgreSQL database
4. Set environment variables
5. Deploy

**Heroku:**
```bash
# Login
heroku login

# Create app
heroku create your-app-name

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:mini

# Deploy
git push heroku main

# Configure environment
heroku config:set SECRET_KEY=your-secret-key
```

#### Option 4: VPS/Server Deployment

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install dependencies
sudo apt install python3.12 python3.12-venv postgresql nginx supervisor

# 3. Clone repository
git clone <repo-url> /var/www/crud-api
cd /var/www/crud-api

# 4. Set up virtual environment
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Configure systemd service
sudo nano /etc/systemd/system/crud-api.service
```

**systemd service file:**
```ini
[Unit]
Description=FastAPI CRUD API
After=network.target postgresql.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/crud-api
Environment="PATH=/var/www/crud-api/venv/bin"
ExecStart=/var/www/crud-api/venv/bin/uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable crud-api
sudo systemctl start crud-api
sudo systemctl status crud-api
```

**Nginx reverse proxy:**
```nginx
# /etc/nginx/sites-available/crud-api
server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site and reload nginx
sudo ln -s /etc/nginx/sites-available/crud-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Configure SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d api.example.com
```

### Production Monitoring

```bash
# Check application logs
tail -f /var/www/crud-api/app.log

# Check system logs
sudo journalctl -u crud-api -f

# Monitor processes
htop

# Database connections
sudo -u postgres psql -c "SELECT count(*) FROM pg_stat_activity;"

# API health check
curl http://localhost:8000/health
```

### Backup Strategy

```bash
# Database backup script
#!/bin/bash
BACKUP_DIR=/var/backups/postgresql
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -U postgres crud_db | gzip > $BACKUP_DIR/crud_db_$DATE.sql.gz

# Keep only last 7 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete
```

---

## 📁 Project Structure

```
crud/
├── app/
│   ├── __init__.py              # FastAPI app initialization & CORS
│   ├── config.py                # Configuration management (Pydantic Settings)
│   ├── logger.py                # Logging setup (console + file)
│   │
│   ├── auth/                    # Authentication module
│   │   ├── __init__.py
│   │   └── security.py          # JWT & password handling (bcrypt)
│   │
│   ├── db/                      # Database module
│   │   ├── __init__.py
│   │   ├── database.py          # Async engine, session, Base
│   │   └── models.py            # SQLAlchemy ORM models (User, Item)
│   │
│   ├── schemas/                 # Pydantic validation schemas
│   │   ├── __init__.py
│   │   ├── user.py              # UserCreate, UserResponse, Token
│   │   └── item.py              # ItemCreate, ItemUpdate, ItemResponse
│   │
│   ├── services/                # Business logic layer
│   │   ├── __init__.py
│   │   ├── user_service.py      # User CRUD & authentication
│   │   └── item_service.py      # Item CRUD operations
│   │
│   └── routes/                  # API endpoints
│       ├── __init__.py
│       └── v1/                  # Version 1 routes
│           ├── __init__.py      # Router aggregation
│           ├── auth.py          # POST register, login
│           ├── users.py         # GET /me
│           ├── items.py         # Full CRUD endpoints
│           └── admin.py         # Admin dashboard & management
│
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (not in git)
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
├── Dockerfile                   # Docker configuration
├── docker-compose.yml           # Multi-container setup
├── reset_db.py                  # Drop and recreate all tables
├── seed_database.py             # Populate DB with realistic test data
├── test_db_connection.py        # Async DB test utility
├── test_db_simple.py            # Simple sync DB test
├── test_admin.py                # Admin dashboard functionality tests
├── INTERVIEW_REQUIREMENTS.md    # Interview exercise documentation
├── CLAUDE.md                    # Project instructions for Claude Code
├── START_GUIDE.md               # Quick start guide
└── README.md                    # This file
```

### Module Responsibilities

```mermaid
graph TD
    Main[main.py] --> App[app/__init__.py]
    App --> Routes[routes/v1/]
    Routes --> Auth[auth.py]
    Routes --> Users[users.py]
    Routes --> Items[items.py]
    Routes --> Admin[admin.py]
    
    Auth --> AuthService[services/user_service.py]
    Users --> AuthMiddleware[auth/security.py]
    Items --> AuthMiddleware
    Admin --> AdminMiddleware[auth/security.py - Admin Check]
    Items --> ItemService[services/item_service.py]
    Admin --> UserService[services/user_service.py]
    Admin --> ItemService
    
    AuthService --> DB[db/models.py]
    ItemService --> DB
    UserService --> DB
    AuthMiddleware --> DB
    AdminMiddleware --> DB
    
    DB --> Postgres[(PostgreSQL)]
    
    Config[config.py] -.->|Settings| App
    Config -.->|Settings| DB
    Logger[logger.py] -.->|Logging| App
    
    style App fill:#green
    style Routes fill:#blue
    style AuthMiddleware fill:#orange
    style AdminMiddleware fill:#red
    style DB fill:#purple
```

---

## 🛠️ Technology Stack

### Core Framework
- **FastAPI 0.100+** - Modern async web framework
- **Uvicorn** - ASGI server with WebSocket support
- **Pydantic 2.x** - Data validation using Python type hints

### Database
- **PostgreSQL 15+** - Advanced open-source relational database
- **SQLAlchemy 2.x** - Python SQL toolkit and ORM
- **asyncpg** - Fast PostgreSQL client library for Python asyncio

### Authentication & Security
- **python-jose 3.x** - JOSE implementation (JWT tokens)
- **passlib 1.7.x** - Password hashing library
- **bcrypt 4.x** - Provably secure password hashing
- **python-multipart** - Streaming multipart parser

### Development Tools
- **uv** - Ultra-fast Python package installer (10x faster than pip)
- **python-dotenv** - Environment variable management

### Dependencies Version Lock

```txt
fastapi==0.100+
uvicorn==0.24+
sqlalchemy==2.0+
asyncpg==0.29+
passlib[bcrypt]==1.7+
bcrypt>=4.0,<5.0
python-jose[cryptography]==3.3+
python-multipart==0.0.6+
pydantic==2.5+
pydantic-settings==2.1+
email-validator==2.1+
python-dotenv==1.0+
```

---

## 📊 Database Schema

```mermaid
erDiagram
    USERS {
        uuid id PK "Primary Key"
        varchar email UK "Unique, Indexed"
        varchar hashed_password "Bcrypt hash"
        varchar full_name "Optional"
        boolean is_active "Default true"
        boolean is_admin "Default false"
        timestamp created_at "Auto-set"
        timestamp updated_at "Auto-updated"
    }
    
    ITEMS {
        uuid id PK "Primary Key"
        varchar title "1-255 chars, Indexed"
        text description "Optional"
        integer price "In cents, >= 0"
        varchar category "Optional, max 100"
        boolean is_available "Default true"
        timestamp created_at "Auto-set"
        timestamp updated_at "Auto-updated"
    }
```

### Table Details

**Users Table:**
- `id`: UUID v4, primary key, indexed
- `email`: Unique constraint, indexed for fast lookups
- `hashed_password`: Bcrypt with 12 rounds
- `full_name`: Optional display name
- `is_active`: Soft delete / account status
- `is_admin`: Admin role flag (default: false) - controls access to admin endpoints
- `created_at`: Set on insert, immutable
- `updated_at`: Auto-updates on any modification

**Items Table:**
- `id`: UUID v4, primary key, indexed
- `title`: Required, indexed for search
- `description`: Optional long text
- `price`: Integer (cents), validation >= 0
- `category`: Optional classification
- `is_available`: Stock/visibility flag
- `created_at`: Set on insert
- `updated_at`: Auto-updates on modification

### Indexes

```sql
-- Automatically created indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_id ON users(id);
CREATE INDEX idx_items_title ON items(title);
CREATE INDEX idx_items_id ON items(id);
```

---

### Reference Materials
- [FastAPI Official Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Async Guide](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [JWT.io - JWT Debugger](https://jwt.io/)
- [PostgreSQL Best Practices](https://wiki.postgresql.org/wiki/Don%27t_Do_This)
- [GeeksforGeeks - FastAPI JWT Guide](https://www.geeksforgeeks.org/python/login-registration-system-with-jwt-in-fastapi/)

---

## 🤝 Contributing

This is an interview exercise project. Contributions are not currently accepted.

### Code Quality Standards
- PEP 8 compliant
- Type hints on all functions
- Docstrings (Google style)
- Exception handling with rollback
- Production-grade logging
- Secure by default

---

## 👤 Author
**Manoj Kumar Karumanchi**

---

### Common Issues

**1. Database Connection Failed**
```bash
# Check PostgreSQL is running
docker ps  # or
sudo systemctl status postgresql

# Test connection
python test_db_connection.py

# Check .env DATABASE_URL format
# Must be: postgresql+asyncpg://user:pass@host:port/db
```

**2. Import Errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Check Python version
python --version  # Must be 3.12+
```

**3. Token Expired / 401 Errors**
```bash
# Check token expiry (default 30 min)
# Re-login to get new token
curl -X POST http://localhost:8000/v1/auth/login \
  -d "username=your@email.com&password=yourpassword"
```

**4. bcrypt Warning**
```
# (trapped) error reading bcrypt version
```
This is a harmless warning from passlib checking bcrypt version. Functionality is not affected.

### Debug Mode

```bash
# Enable debug logging
DEBUG=True python main.py

# Check application logs
tail -f app.log

# Check database logs
docker logs postgres-crud  # or
sudo tail -f /var/log/postgresql/postgresql-15-main.log
```

### Getting Help

1. Check [API Documentation](http://localhost:8000/docs)
2. Review `app.log` for errors
3. Run `python test_db_connection.py`
4. Verify `.env` configuration
5. Check PostgreSQL is accessible

---

## 🔄 Version History

### v1.0.0 (April 20, 2026)
**Initial Release - Interview Exercise**

**Features:**
- ✅ JWT authentication with OAuth2
- ✅ User registration and login
- ✅ Full CRUD operations for Items
- ✅ **Role-Based Access Control (RBAC)** - Admin-only endpoints
- ✅ **Admin Dashboard** - Complete system overview with statistics
- ✅ **Admin User Management** - List users, get user counts, filter by status
- ✅ **Admin Item Management** - List all items, get statistics by category
- ✅ UUID primary keys
- ✅ Auto timestamps (created_at, updated_at)
- ✅ Async PostgreSQL with connection pooling
- ✅ Password hashing (bcrypt, 12 rounds)
- ✅ API versioning (/v1/)
- ✅ Comprehensive logging (console + file)
- ✅ Exception handling with database rollback
- ✅ Pydantic validation
- ✅ Interactive API documentation (Swagger/ReDoc)
- ✅ Production-ready architecture
- ✅ Docker support
- ✅ Environment-based configuration
- ✅ Database connection testing utilities
- ✅ Realistic test data seeder with admin user

**Security:**
- ✅ Password length validation (8-72 chars)
- ✅ Email format validation
- ✅ JWT token expiration
- ✅ Protected routes with authentication
- ✅ **Admin authorization** - Role-based access with 403 Forbidden for non-admins
- ✅ Input validation on all endpoints
- ✅ SQL injection prevention (ORM)
- ✅ CORS configuration

**Performance:**
- ✅ Async database operations
- ✅ Connection pooling (10 size, 20 overflow)
- ✅ Connection recycling (30 min)
- ✅ Pre-ping for stale connections
- ✅ Rotating log files (10MB, 5 backups)
