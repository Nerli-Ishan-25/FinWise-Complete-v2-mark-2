# FinWise Backend — Complete Project Explanation
### *Interview-Ready Deep Dive: Architecture, Logic & Data Flow*

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Technology Stack](#2-technology-stack)
3. [Folder & File Structure](#3-folder--file-structure)
4. [The Request Lifecycle (How It All Connects)](#4-the-request-lifecycle-how-it-all-connects)
5. [Core Layer — `app/core/`](#5-core-layer--appcore)
6. [Database Layer — `app/database/`](#6-database-layer--appdatabase)
7. [Models Layer — `app/models/`](#7-models-layer--appmodels)
8. [Schemas Layer — `app/schemas/`](#8-schemas-layer--appschemas)
9. [Services Layer — `app/services/`](#9-services-layer--appservices)
10. [API Routes Layer — `app/api/`](#10-api-routes-layer--appapi)
11. [AI Engine — `app/ai_engine.py`](#11-ai-engine--appai_enginepy)
12. [ML Models — `app/ml_models/`](#12-ml-models--appml_models)
13. [Entry Point — `app/main.py`](#13-entry-point--appmainpy)
14. [Configuration & Environment — `.env` / `requirements.txt`](#14-configuration--environment)
15. [Database Schema Files — `app/database/schema/`](#15-database-schema-files)
16. [Authentication & Security Flow](#16-authentication--security-flow)
17. [Key Design Patterns & Interview Talking Points](#17-key-design-patterns--interview-talking-points)
18. [Dependency Graph (Visual Summary)](#18-dependency-graph-visual-summary)

---

## 1. Project Overview

**FinWise** is an AI-powered personal finance management backend built with **FastAPI** (Python). It allows users to:

- Track income, expenses, loans, assets, liabilities, subscriptions, and budgets
- Get AI-generated financial health scores and actionable recommendations
- Chat with an AI financial assistant (backed by multiple LLM providers)
- Receive loan eligibility predictions using a trained **XGBoost** ML model

Think of it as a smart personal finance API — somewhere between a bank's transaction API and a personal finance advisor.

---

## 2. Technology Stack

| Component | Technology | Why |
|---|---|---|
| Web Framework | **FastAPI** | Fast, async-ready, auto-generates OpenAPI docs |
| ORM (Database Bridge) | **SQLAlchemy** | Maps Python classes to database tables |
| Database | **SQLite** (via `finance_app.db`) | Lightweight, file-based, zero setup for dev |
| Data Validation | **Pydantic v2** | Schema enforcement, request/response serialization |
| Authentication | **JWT (python-jose)** | Stateless token-based auth |
| Password Hashing | **Passlib (pbkdf2_sha256)** | Secure password storage |
| ML Model | **XGBoost + joblib** | Loan default prediction |
| LLM Providers | **Groq, Gemini, Ollama, HF, OpenAI, Anthropic** | Multi-provider AI chat with failover |
| HTTP Client (async) | **httpx** | For calling external LLM APIs |
| Server | **Uvicorn** | ASGI server to run FastAPI |

---

## 3. Folder & File Structure

```
Backend-Finwise/
│
├── app/                        ← All application source code lives here
│   ├── main.py                 ← App entry point: creates FastAPI app, registers all routes
│   ├── ai_engine.py            ← Custom heuristic financial scoring & forecasting models
│   │
│   ├── core/                   ← Global configuration & security utilities
│   │   ├── config.py           ← All settings (DB URL, JWT secret, API keys)
│   │   └── security.py         ← Password hashing & JWT token creation
│   │
│   ├── database/               ← Database connection setup & raw SQL schema files
│   │   ├── connection.py       ← SQLAlchemy engine, session factory, get_db dependency
│   │   ├── initDB.js           ← Legacy/alternative JS init script (not used by Python)
│   │   └── schema/             ← Raw SQL CREATE TABLE definitions (documentation/reference)
│   │       ├── users.sql
│   │       ├── transactions.sql
│   │       ├── assets.sql
│   │       ├── liabilities.sql
│   │       ├── budgets.sql
│   │       ├── categories.sql
│   │       ├── loans.sql
│   │       └── subscriptions.sql
│   │
│   ├── models/                 ← SQLAlchemy ORM models (Python ↔ DB table mapping)
│   │   └── user_finance.py     ← ALL database table classes defined here
│   │
│   ├── schemas/                ← Pydantic schemas (API request/response shapes)
│   │   ├── auth_schema.py      ← User registration, login, token, onboarding schemas
│   │   └── finance_schema.py   ← All financial data shapes (income, expense, budget, etc.)
│   │
│   ├── services/               ← Business logic layer (the "brain" of the app)
│   │   ├── auth_service.py     ← User CRUD, authentication, onboarding logic
│   │   ├── finance_service.py  ← Core financial CRUD + dashboard calculations
│   │   ├── analytics_service.py← Bridges finance data → AI engine → health scores
│   │   └── ai_assistant_service.py ← Multi-provider LLM chatbot with failover
│   │
│   ├── api/                    ← HTTP route handlers (thin controllers)
│   │   ├── dependencies.py     ← FastAPI dependency: JWT validation → current user
│   │   ├── auth_routes.py      ← /auth/* endpoints (register, login, onboarding)
│   │   ├── finance_routes.py   ← /finance/* (income, expenses, loans, transactions, dashboard)
│   │   ├── asset_routes.py     ← /assets/* CRUD
│   │   ├── liability_routes.py ← /liabilities/* CRUD
│   │   ├── budget_routes.py    ← /budgets/* CRUD
│   │   ├── category_routes.py  ← /categories/* CRUD
│   │   ├── subscription_routes.py ← /subscriptions/* CRUD
│   │   ├── insights_routes.py  ← /insights/* AI financial insights
│   │   ├── loan_assessment_routes.py ← /loan-assessment/* XGBoost ML prediction
│   │   ├── assistant_routes.py ← /assistant/chat LLM chat endpoint
│   │   ├── admin_routes.py     ← /admin/* (admin-only user management)
│   │   └── __init__.py         ← Exports all router objects for main.py
│   │
│   └── ml_models/              ← Trained ML artifacts & inference code
│       ├── loan_inference.py   ← Feature engineering + XGBoost prediction logic
│       ├── optimised_xgb_pipeline.pkl  ← Serialized trained XGBoost pipeline
│       └── optimised_xgb_threshold.pkl ← Custom decision threshold (~0.6387)
│
├── finance_app.db              ← SQLite database file (auto-created on first run)
├── finance_app_backup.db       ← Backup of the database
├── .env.example                ← Template showing what environment variables are needed
├── requirements.txt            ← Python package dependencies
└── venv/                       ← Python virtual environment (excluded from explanation)
```

---

## 4. The Request Lifecycle (How It All Connects)

Every API call flows through the same pipeline. Here is the complete path for a request like `GET /api/v1/finance/dashboard`:

```
CLIENT (Flutter App / Postman)
    │
    │  HTTP Request with Bearer Token
    ▼
app/main.py
    │  FastAPI receives the request
    │  CORS middleware allows the origin
    │  Routes the request to finance_routes.router
    ▼
app/api/finance_routes.py  →  get_dashboard()
    │
    │  FastAPI Dependency Injection kicks in:
    │  → get_db()          (from database/connection.py) opens a DB session
    │  → get_current_active_user() (from api/dependencies.py)
    │       ↳ Reads Bearer token from Authorization header
    │       ↳ Decodes JWT using SECRET_KEY (core/security.py)
    │       ↳ Queries DB for User by id from token payload
    │       ↳ Returns current_user object
    │
    ▼
app/services/finance_service.py  →  get_dashboard_metrics()
    │  Does all DB queries (income, expenses, assets, liabilities)
    │  Calculates net worth, savings rate
    │  Calls analytics_service.get_ai_insights()
    │       ↳ Calls ai_engine.financial_score_model.calculate_financial_health()
    │       ↳ Calls ai_engine.forecasting_model.forecast_expenses()
    │
    ▼
Response Dictionary
    │
    ▼
FastAPI serializes it using DashboardMetrics Pydantic Schema
    │
    ▼
JSON Response → CLIENT
```

This pattern — **Route → Dependency Injection → Service → DB/AI → Schema → Response** — repeats for every single endpoint in the app.

---

## 5. Core Layer — `app/core/`

### `config.py` — The Settings Hub

This file uses **Pydantic's `BaseSettings`** to manage all configuration. Every setting is read from the `.env` file at startup.

```python
class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Finance Platform"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = ...
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./finance_app.db"
    GROQ_API_KEY: str | None = None
    GEMINI_API_KEY: str | None = None
    # ... more LLM keys
```

**Why a `settings` object?** Any file in the codebase can do `from app.core.config import settings` and get typed, validated access to configuration. No raw `os.getenv()` calls scattered across files.

**LLM Provider Config:** The config supports 7 different LLM providers. Only the ones with API keys present in `.env` are activated at runtime.

### `security.py` — Passwords & Tokens

Two responsibilities:

1. **Password hashing:** Uses `pbkdf2_sha256` (a one-way hashing algorithm). When a user registers, their plaintext password is *never* stored — only its hash. On login, the plaintext is hashed again and compared.

2. **JWT token creation:** Creates a JSON Web Token embedding `user_id`, `role`, and an expiry timestamp. The token is signed with `SECRET_KEY` so it cannot be tampered with. The token is passed in every subsequent request to prove identity.

```python
def create_access_token(subject, role, expires_delta):
    to_encode = {"exp": expire, "sub": str(subject), "role": role}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
```

**Connection to rest of app:** `security.py` is used by `auth_service.py` (to hash/verify passwords) and `auth_routes.py` (to create the token on successful login).

---

## 6. Database Layer — `app/database/`

### `connection.py` — The Database Engine

This file sets up **SQLAlchemy** and provides the database session to the rest of the app.

Three key exports:

| Export | Type | What it does |
|---|---|---|
| `Base` | SQLAlchemy `DeclarativeBase` | All model classes inherit from this |
| `engine` | SQLAlchemy `Engine` | The actual connection to SQLite |
| `get_db()` | Generator function | FastAPI dependency — opens and closes a session per request |

The `get_db()` function is a **FastAPI dependency**. FastAPI automatically calls it before every route handler that lists `db: Session = Depends(get_db)`, injects the session, and guarantees `db.close()` runs even if an exception occurs (the `try/finally` block).

### `schema/` — SQL Reference Files

These are raw `.sql` files containing `CREATE TABLE` statements. **They are not used by the Python runtime** — SQLAlchemy creates the tables automatically via `Base.metadata.create_all(bind=engine)` in `main.py`. The SQL files serve as human-readable documentation of the table structure and are useful for understanding the database design or setting up an alternative database manually.

### `initDB.js` — Legacy File

A Node.js script from an earlier version of the project. Not used in the current Python/FastAPI flow.

---

## 7. Models Layer — `app/models/user_finance.py`

This is **the single most important file** for understanding the data structure. Every database table in the app is defined here as a Python class.

### All Models (Tables)

| Class | Table Name | What it Represents |
|---|---|---|
| `User` | `users` | A registered user account |
| `Income` | `income` | A single income entry (salary, freelance, etc.) |
| `Expense` | `expenses` | A single expense entry |
| `Loan` | `loans` | A loan the user has taken |
| `Transaction` | `transactions` | A unified ledger of all financial events |
| `Asset` | `assets` | Things the user owns (car, stock, property) |
| `Liability` | `liabilities` | Things the user owes (credit card debt, EMI) |
| `Category` | `categories` | Labels for budgeting (Food, Travel, etc.) |
| `Budget` | `budgets` | A monthly spending limit per category |
| `Subscription` | `subscriptions` | Recurring payments (Netflix, gym, etc.) |

### The Central `User` Model and Relationships

The `User` model is the **parent** of everything. Every other model has a `user_id` foreign key pointing back to `users.id`. This is one-to-many: one user → many incomes, many expenses, many assets, etc.

SQLAlchemy `relationship()` lets you do `user.assets` in Python and get a list of that user's assets without writing a JOIN query manually.

```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    ...
    assets = relationship("Asset", back_populates="user")
    expenses = relationship("Expense", back_populates="user")
    # ...
```

### The `Transaction` Table — The Unified Ledger

When a user logs income or an expense, **two** database rows are created:
1. One in `income` or `expenses` (the detailed record)
2. One in `transactions` (a unified ledger entry with `type="income"` or `type="expense"`)

This gives the frontend a single `/finance/transactions` endpoint to display a complete activity feed without having to merge two separate lists.

---

## 8. Schemas Layer — `app/schemas/`

Pydantic schemas serve as the **contract between the API and the outside world**. They define exactly what JSON shape is accepted in requests and returned in responses.

### Why Schemas Are Separate From Models

SQLAlchemy models describe database columns. Pydantic schemas describe API shapes. They are deliberately kept separate because:
- The DB might have a `password_hash` column you never want to expose in an API response
- An API might accept a flat JSON object that maps to multiple DB tables
- You might need different shapes for "create" vs "update" vs "response"

### `auth_schema.py`

| Schema | Used For |
|---|---|
| `UserCreate` | POST /auth/register — incoming registration data |
| `UserInDB` | Response for user info (no password) |
| `Token` | Response for successful login (access_token + token_type) |
| `TokenData` | Internal: the decoded payload of a JWT |
| `OnboardingData` | POST /auth/onboarding — assets, liabilities, income provided at signup |

### `finance_schema.py`

Contains `Create`, `Update`, and `Response` variants for every financial entity. For example, `AssetCreate` requires `name` and `value`, while `AssetResponse` includes `id`, `user_id`, and `created_at` that the server fills in.

The `DashboardMetrics` schema is what the dashboard endpoint returns — a rich object with `netWorth`, `savingsRate`, `financialHealthScore`, `insights`, and `forecastedNextMonth`.

---

## 9. Services Layer — `app/services/`

This is the **business logic layer**. Routes call services; services call models and external APIs. The services contain all the real work.

### `auth_service.py` — User Management

| Function | What It Does |
|---|---|
| `create_user()` | Hashes password, inserts User row |
| `authenticate_user()` | Looks up user by email, verifies password hash |
| `complete_onboarding()` | Atomically saves assets, liabilities, and incomes from onboarding, marks `user.onboarded = True` |
| `update_user()` | Partial update using `exclude_unset=True` so only provided fields are changed |

### `finance_service.py` — The Core Logic

The largest service file. It handles everything financial. Key highlights:

**Dual-write on Income/Expense creation:** Every `create_user_income()` call also creates a `Transaction` row. This keeps the transactions table in sync automatically.

**Dashboard Calculation (`get_dashboard_metrics`):**
1. Gets this month's income (prefers `user.monthly_income` if set, otherwise sums income table)
2. Gets this month's expenses
3. Calculates net worth = total assets − total liabilities
4. Calculates savings rate = (income − expenses) / income × 100
5. Calls `analytics_service.get_ai_insights()` for the health score, recommendations, and forecast
6. Returns a single consolidated dictionary

**Cascade Delete on Transactions:** When a transaction is deleted, the service also finds and deletes the matching `Income` or `Expense` row to keep both tables consistent.

**`get_financial_profile_snapshot()`:** Builds a human-readable text string of the user's financial state (net worth, income, expenses). This is passed as *context* to the LLM chatbot so it can give personalized advice.

### `analytics_service.py` — AI Insights Bridge

This is a **thin bridge** between `finance_service` and `ai_engine`. It:
1. Gets raw financial metrics
2. Derives two calculated ratios: `emergency_fund_ratio` and `debt_to_income`
3. Passes them to `ai_engine.financial_score_model` for scoring
4. Calls `forecasting_model.forecast_expenses()` for next-month prediction
5. Returns everything packaged together

### `ai_assistant_service.py` — Multi-Provider LLM Chatbot

This service powers the `/assistant/chat` endpoint. It is designed with **failover** in mind.

**How the failover chain works:**
- On startup, it builds `self.providers` — a list of async functions, one per configured LLM.
- The order is: Ollama Cloud → Ollama Local → Groq → Gemini → HuggingFace → OpenAI → Anthropic
- `generate_response()` loops through providers and returns the first successful response
- If a provider throws an exception, it logs a warning and tries the next

**System Prompt Injection:** Before every chat call, the user's financial snapshot (from `get_financial_profile_snapshot`) is injected into the system prompt so the LLM has context about the user's real finances.

```python
system_prompt = (
    "You are FinWise AI, a personal finance assistant..."
    f"USER CONTEXT:\n{context_str}"  # ← Real financial data injected here
)
```

---

## 10. API Routes Layer — `app/api/`

Routes are **thin controllers**. They should do minimal logic — validate the request, call a service, return the result.

### `dependencies.py` — The Auth Gate

This file defines three reusable FastAPI dependencies:

| Dependency | What It Does | Used By |
|---|---|---|
| `get_current_user()` | Decodes JWT → fetches user from DB | All protected routes |
| `get_current_active_user()` | Wraps above (could add `is_active` check here) | Most routes |
| `get_current_admin_user()` | Ensures `user.role == "admin"`, else 403 | Admin routes |

When a route declares `current_user: User = Depends(get_current_active_user)`, FastAPI automatically validates the token and injects the user object. If the token is missing or invalid, FastAPI returns 401 before the route function ever runs.

### Route Files & Their URLs

| File | URL Prefix | Key Endpoints |
|---|---|---|
| `auth_routes.py` | `/api/v1/auth` | POST /register, POST /login, POST /onboarding |
| `finance_routes.py` | `/api/v1/finance` | GET /dashboard, GET/POST /income, /expenses, /loans, /transactions |
| `asset_routes.py` | `/api/v1/assets` | CRUD for assets |
| `liability_routes.py` | `/api/v1/liabilities` | CRUD for liabilities |
| `budget_routes.py` | `/api/v1/budgets` | CRUD for budgets with live `spent` calculation |
| `category_routes.py` | `/api/v1/categories` | CRUD for expense categories |
| `subscription_routes.py` | `/api/v1/subscriptions` | CRUD for recurring subscriptions |
| `insights_routes.py` | `/api/v1/insights` | GET AI insights/score |
| `loan_assessment_routes.py` | `/api/v1/loan-assessment` | POST /predict (XGBoost ML inference) |
| `assistant_routes.py` | `/api/v1/assistant` | POST /chat (LLM chat) |
| `admin_routes.py` | `/api/v1/admin` | Admin-only: list/update/delete users |

### `auth_routes.py` — Rate Limiting

The login endpoint has a **simple in-memory rate limiter** to prevent brute-force attacks:
- Tracks login attempts per IP address using a Python `defaultdict`
- Maximum 5 attempts per 5-minute window
- Returns HTTP 429 if exceeded
- Clears the counter on successful login

**Limitation:** Because it's in-memory, rate limiting resets if the server restarts and does not work across multiple server instances. A production system would use Redis.

### `loan_assessment_routes.py` — ML Prediction

The most technically complex route file. It:
1. Accepts a detailed `LoanAssessmentRequest` with personal and loan details
2. Uses Pydantic `@field_validator` to validate categorical fields (e.g., education must be one of `["Bachelor's", "High School", "Master's", "PhD"]`)
3. Passes data to `loan_inference.predict_loan_eligibility()` which runs the XGBoost pipeline
4. Returns a prediction: **APPROVED** or **REJECTED**, with a default probability and confidence score

---

## 11. AI Engine — `app/ai_engine.py`

This is a **custom, lightweight, rule-based "AI"** — not an external API call, not a trained ML model. It runs entirely on the server with no network requests.

### `FinancialScoreModel`

Computes a **0–10 financial health score** from three inputs:
- `savings_rate` — percentage of income saved
- `debt_to_income` — estimated monthly debt / monthly income
- `emergency_fund_ratio` — total assets / monthly expenses (months of runway)

Scoring rules (additive from a base of 5.0):
- Savings rate ≥ 20% → +3; ≥ 10% → +2; ≥ 5% → +1; negative → -2
- Emergency fund ≥ 6 months → +2; ≥ 3 months → +1
- DTI ≥ 60% → -3; ≥ 40% → -2; ≥ 30% → -1

It also generates `generate_recommendations()` — rule-based text advice based on the same metrics (e.g., "Your savings rate is low. Aim to save at least 5–10%...").

### `ForecastingModel`

A deliberately simple forecaster: it averages all historical expense amounts and returns that as the predicted next-month expense. The `lookback_months` attribute exists for future improvement but is not yet applied as a filter.

**Interview Tip:** Be ready to explain *why* these are rule-based rather than ML models. The answer: for small user bases with limited historical data, a rule-based system is more reliable, interpretable, and doesn't require training data. The XGBoost model (loan assessment) uses a large public dataset instead.

---

## 12. ML Models — `app/ml_models/`

### `loan_inference.py` — XGBoost Inference Engine

This module wraps a pre-trained XGBoost model for **loan default prediction**.

**The ML Pipeline** (stored in `optimised_xgb_pipeline.pkl`):
1. `preprocessor` — ColumnTransformer: One-Hot Encodes categorical features, passes through numerics
2. `smote` — SMOTE oversampler (training only, skipped at inference automatically by sklearn pipeline)
3. `classifier` — XGBClassifier (the actual prediction model)

**Feature Engineering** (done in Python before sending to the pipeline):
```
Loan_to_Income  = LoanAmount / Income
EMI_to_Income   = (LoanAmount / LoanTerm) / Income
Credit_per_Line = CreditScore / NumCreditLines
```

These three engineered features are computed from raw inputs and appended before inference.

**Custom Decision Threshold:** The model outputs a probability of default (0–1). Instead of the default 0.5 threshold, this model uses **0.6387** (stored in `optimised_xgb_threshold.pkl`). This means the model is more conservative — it only rejects a loan if it's highly confident the borrower will default. This threshold was optimized during training (likely on precision/recall tradeoff).

**Lazy Loading:** The model is loaded from disk only once, on the first prediction request, and cached in a module-level variable. This avoids loading a 6MB file on every API call.

**Input Validation:** The `LoanInputValidationError` custom exception is raised if invalid categorical values are provided (before even touching the model).

### Model Files

| File | Size | What It Is |
|---|---|---|
| `optimised_xgb_pipeline.pkl` | ~6.3 MB | Full sklearn pipeline (preprocessor + XGBoost) serialized with joblib |
| `optimised_xgb_threshold.pkl` | 21 bytes | Single float: the optimal decision threshold |

---

## 13. Entry Point — `app/main.py`

This is where the FastAPI application is **assembled**. It runs once at startup.

```python
# 1. Create the FastAPI app instance
app = FastAPI(title=settings.PROJECT_NAME, ...)

# 2. Apply CORS middleware (allow all origins — appropriate for tunneled dev)
app.add_middleware(CORSMiddleware, allow_origins=["*"], ...)

# 3. Create all database tables (if they don't exist)
Base.metadata.create_all(bind=engine)

# 4. Register all routers with their URL prefixes
app.include_router(auth_routes.router, prefix="/api/v1/auth")
app.include_router(finance_routes.router, prefix="/api/v1/finance")
# ... all 11 routers
```

**`Base.metadata.create_all(bind=engine)`** is the key startup step — it reads all SQLAlchemy model classes (imported via `from app.models import user_finance`) and creates the corresponding tables in SQLite if they don't exist yet. This means the database schema is always in sync with the Python models.

---

## 14. Configuration & Environment

### `.env.example`

A template that documents what environment variables the app needs. Developers copy this to `.env` and fill in real values. The `.env` file itself is never committed to git (it contains secrets).

Key variables:
- `SECRET_KEY` — Used to sign JWTs. If this leaks, anyone can forge auth tokens.
- `SQLALCHEMY_DATABASE_URI` — Points to `finance_app.db` for SQLite.
- LLM API keys — At least one must be set for AI features to work.

### `requirements.txt`

Lists all Python packages the project depends on. Key ones:

| Package | Purpose |
|---|---|
| `fastapi` | Web framework |
| `uvicorn[standard]` | ASGI server |
| `sqlalchemy` | ORM |
| `pydantic-settings` | Settings management |
| `python-jose[cryptography]` | JWT |
| `passlib[bcrypt]` | Password hashing |
| `xgboost` | ML loan prediction |
| `imbalanced-learn` | SMOTE in training pipeline |
| `joblib` | Model serialization |
| `pandas` | Data handling for ML |
| `httpx` | Async HTTP client for LLM API calls |

---

## 15. Database Schema Files

The SQL files in `app/database/schema/` define the actual table structures. These are for reference only — SQLAlchemy handles creation. Understanding them helps you answer schema questions in interviews:

- **`users.sql`** — `id`, `name`, `email` (unique), `password_hash`, `role` (enum), `created_at`, `onboarded` (boolean), `monthly_income`
- **`transactions.sql`** — `id`, `user_id` (FK), `type` (income/expense/loan), `category`, `amount`, `date`, `description`
- **`assets.sql`** — `id`, `user_id` (FK), `name`, `type`, `value`, `created_at`
- **`liabilities.sql`** — `id`, `user_id` (FK), `name`, `type`, `amount`, `interest_rate`, `created_at`
- **`loans.sql`** — `id`, `user_id` (FK), `loan_amount`, `interest_rate`, `remaining_amount`, `created_at`
- **`budgets.sql`** — `id`, `user_id` (FK), `category_id` (FK → categories), `budget_amount`, `month`, `year`
- **`categories.sql`** — `id`, `user_id` (nullable FK — `NULL` means it's a global/default category), `name`, `type`
- **`subscriptions.sql`** — `id`, `user_id` (FK), `name`, `amount`, `billing_cycle`, `next_payment_date`, `active`, `last_used`

---

## 16. Authentication & Security Flow

### Registration Flow
```
POST /api/v1/auth/register
  Body: { name, email, password, role? }
  
  → auth_routes.py checks if email already exists
  → auth_service.create_user() hashes the password (pbkdf2_sha256)
  → Saves User row to DB
  → Returns UserInDB (no password hash exposed)
```

### Login Flow
```
POST /api/v1/auth/login
  Body: form-data { username (email), password }
  
  → Rate limit check (max 5/5min per IP)
  → auth_service.authenticate_user() verifies password hash
  → security.create_access_token() creates JWT with user_id + role
  → Returns { access_token, token_type: "bearer" }
```

### Protected Request Flow
```
GET /api/v1/finance/dashboard
  Header: Authorization: Bearer <JWT>
  
  → dependencies.get_current_user() decodes JWT
  → Extracts user_id and role from payload
  → Queries DB for user
  → Route function gets current_user injected
```

### Onboarding Flow
```
POST /api/v1/auth/onboarding (requires auth token)
  Body: { goal, assets: [...], liabilities: [...], income: [...] }
  
  → Checks user.onboarded == False (can't onboard twice)
  → auth_service.complete_onboarding() saves all data in one transaction
  → Sets user.onboarded = True
```

---

## 17. Key Design Patterns & Interview Talking Points

### 1. Layered Architecture
The project follows a clean **4-layer architecture**: Routes → Services → Models → Database. Each layer has one responsibility. Routes don't touch the DB directly; services don't know about HTTP.

### 2. FastAPI Dependency Injection
FastAPI's `Depends()` system is used heavily. `get_db` provides the session; `get_current_user` provides authentication. These can be composed — `get_current_admin_user` wraps `get_current_user` and adds a role check.

### 3. Dual-Write Pattern
Every income/expense creation writes to two tables simultaneously (the specific table + transactions). This is a conscious denormalization for read performance on the activity feed.

### 4. Multi-Provider AI with Failover
The `AIAssistantService` tries providers in priority order. This makes the app resilient — if Groq is down, it automatically tries Gemini, then HuggingFace, etc. This pattern is sometimes called a **chain of responsibility**.

### 5. Rule-Based vs. ML AI
The financial scoring is *intentionally* rule-based (transparent, debuggable, no training data needed). The loan prediction is *intentionally* ML-based (complex, non-linear patterns, large training dataset exists). Choosing the right tool for each problem is a good interview talking point.

### 6. Lazy Model Loading
The 6MB XGBoost model is loaded from disk exactly once on the first prediction, then cached. This avoids startup latency and memory waste if the endpoint is never called.

### 7. User-Scoped Data
Every DB query in the services layer always filters by `user_id`. For example: `db.query(Asset).filter(Asset.user_id == user_id)`. This prevents any user from accessing another user's data. It's a simple but critical security pattern.

### 8. Pydantic for Validation
All input data goes through Pydantic schemas before reaching the service layer. Invalid types, missing required fields, or values out of range return a clean 422 Unprocessable Entity response — no manual validation code needed.

---

## 18. Dependency Graph (Visual Summary)

```
                          main.py
                             │
             ┌───────────────┼────────────────────┐
             ▼               ▼                    ▼
          core/           database/          app/api/routes
        config.py        connection.py    (all route files)
        security.py         │                    │
             │              ▼                    ▼
             │           models/          api/dependencies.py
             │         user_finance.py          │
             │              │                   │
             └──────────────┴──────────────────►│
                                                 │
                                                 ▼
                                          services/
                              ┌───────────────────────────────┐
                              │  auth_service.py              │
                              │  finance_service.py           │
                              │  analytics_service.py ───────►│
                              │  ai_assistant_service.py      │
                              └───────────────────────────────┘
                                          │           │
                                          ▼           ▼
                                    ai_engine.py   ml_models/
                                  (rule-based AI)  loan_inference.py
                                                  (XGBoost ML model)
                                                         │
                                                         ▼
                                           optimised_xgb_pipeline.pkl
                                           optimised_xgb_threshold.pkl
```

---

*This document covers every file in the FinWise backend and explains its role, its internal logic, and how it connects to the rest of the system. Use this as your reference going into the interview.*
