# Rami Khaled — Personal Portfolio & Academic Engineering Platform

> **"Engineer in progress. Developer by curiosity. Builder by ambition."**

A complete, modern, production-grade personal portfolio and academic showcase designed for **Rami Khaled** — First-year engineering student at **École Nationale Polytechnique d'Alger (ENP)**. 

Built with **Python**, **Flask**, **PostgreSQL / SQLAlchemy**, **Flask-Migrate**, and a modern, high-performance frontend styled with **Tailwind CSS**, **Lucide Icons**, and vanilla JavaScript.

---

## 🌟 Overview & Purpose

This platform serves two primary missions:
1. **Professional Developer Portfolio**: Highlighting hands-on software development across Python, desktop GUIs, browser automation, web applications, data visualization, and Flutter mobile prototypes.
2. **Academic & Scholarship Admissions Platform**: Communicating academic discipline (Baccalaureate 17.80/20, BEM 17.43/20, ENP entrance), intellectual initiative, algorithmic curiosity, and future engineering ambitions (Python + AI + Flutter).

---

## 🏗️ Architecture & Tech Stack

### Backend
* **Python 3.12+ / 3.14+**
* **Flask 3.x**: Modular application factory with Blueprints (`main`, `projects`, `auth`, `admin`, `api`).
* **SQLAlchemy & PostgreSQL**: Robust relational ORM persistence with flexible fallback to SQLite for zero-friction local testing.
* **Flask-Migrate (Alembic)**: Database schema migration and version control.
* **Flask-Login**: Secure session authentication for the admin control panel.
* **Flask-WTF & WTForms**: Form rendering, validation, and CSRF protection.
* **Werkzeug**: Secure password hashing with PBKDF2/SHA-256.

### Frontend
* **HTML5 & Jinja2**: Semantic markup with component template inheritance.
* **Tailwind CSS**: Modern utility styling, custom typography tokens, and glassmorphic panels.
* **Vanilla JavaScript**: Lightweight theme switching (Dark/Light mode with `localStorage`), dynamic project filtering, and mobile drawer navigation.
* **Lucide Icons**: Crisp, modern technical iconography.

### Directory Structure
```text
rami-portfolio/
│
├── app/
│   ├── __init__.py           # Application factory (create_app), context processors & error handlers
│   ├── extensions.py         # SQLAlchemy, Migrate, LoginManager, CSRFProtect
│   ├── models/               # SQLAlchemy Models
│   │   ├── __init__.py
│   │   ├── user.py           # Admin User authentication
│   │   ├── project.py        # Projects & ProjectImages
│   │   ├── education.py      # Academic milestones & scores
│   │   ├── skill.py          # Categorized skills & proficiency levels
│   │   ├── certification.py  # Verified credentials & bootcamps
│   │   ├── contact.py        # Contact messages
│   │   └── site_setting.py   # Dynamic CMS text settings
│   ├── routes/               # Modular Flask Blueprints
│   │   ├── __init__.py
│   │   ├── main.py           # Homepage, contact form, robots.txt, sitemap.xml
│   │   ├── projects.py       # Projects gallery & deep case studies (/projects/<slug>)
│   │   ├── auth.py           # Admin login & logout
│   │   ├── admin.py          # Full CRUD admin dashboard
│   │   └── api.py            # JSON API endpoints
│   ├── forms/                # Flask-WTF validation forms
│   │   ├── __init__.py
│   │   ├── auth_forms.py
│   │   ├── project_forms.py
│   │   ├── skill_forms.py
│   │   ├── education_forms.py
│   │   ├── cert_forms.py
│   │   └── setting_forms.py
│   ├── static/
│   │   ├── css/style.css     # Glassmorphism, animations, grid background, dark mode
│   │   ├── js/main.js        # Dark/light toggle, live filtering, mobile drawer
│   │   ├── js/admin.js       # Admin slug auto-generator, delete confirmations
│   │   └── uploads/          # User-uploaded screenshots & assets
│   └── templates/
│       ├── base.html         # Global layout with SEO meta & Schema.org JSON-LD
│       ├── index.html        # Comprehensive narrative homepage
│       ├── contact.html      # Dedicated contact form
│       ├── projects/         # Projects gallery & case study detail
│       ├── admin/            # Admin control panel templates
│       ├── auth/             # Login view
│       └── errors/           # 404, 500, 403 error pages
│
├── migrations/               # Alembic database migration scripts
├── tests/                    # Complete pytest test suite
│   ├── conftest.py           # Test fixtures & in-memory database
│   ├── test_routes.py        # Public routes & sitemap tests
│   ├── test_auth.py          # Login, logout & security tests
│   └── test_admin.py         # CRUD dashboard tests
├── seed.py                   # Realistic seed script for Rami's academic & project history
├── config.py                 # Dev, testing, and production configuration profiles
├── run.py                    # Application runner
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
└── README.md
```

---

## ⚡ Quick Start & Local Setup

### 1. Prerequisites
* Python 3.10+ (tested on Python 3.14)
* PostgreSQL (optional for local dev; SQLite fallback is supported automatically)

### 2. Clone and Enter Project Directory
```bash
git clone <repository-url>
cd rami-portfolio
```

### 3. Create and Activate Virtual Environment
On Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Copy `.env.example` to `.env`:
```powershell
Copy-Item .env.example .env
```
Edit `.env` to suit your environment:
```ini
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=generate-a-strong-random-key-here

# PostgreSQL connection string:
# DATABASE_URL=postgresql://postgres:password@localhost:5432/rami_portfolio
# Or leave as default for local SQLite:
DATABASE_URL=sqlite:///rami_portfolio.db

# Admin User credentials
ADMIN_USERNAME=rami
ADMIN_EMAIL=rami.khaled@example.dz
ADMIN_PASSWORD=AdminRami2026!
```

---

## 🐘 PostgreSQL Setup (Production or Local)

To use PostgreSQL locally:
1. Start your PostgreSQL service.
2. Create the database:
   ```sql
   CREATE DATABASE rami_portfolio;
   ```
3. Set `DATABASE_URL` in `.env`:
   ```ini
   DATABASE_URL=postgresql://username:password@localhost:5432/rami_portfolio
   ```
4. Run migrations:
   ```bash
   flask db upgrade
   ```
5. Seed initial data:
   ```bash
   python seed.py
   ```

---

## 🚀 Running the Application

Start the Flask development server:
```bash
python run.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000/
```

### Admin Access
Navigate to:
```
http://127.0.0.1:5000/auth/login
```
* **Username**: `rami`
* **Password**: `AdminRami2026!` (configured in `.env` / `seed.py`)

---

## 🧪 Running Automated Tests

Run the complete test suite with `pytest`:
```bash
python -m pytest -v
```

All 15 tests cover:
* Homepage rendering and academic milestone badges.
* Project showcase filtering and search.
* Deep-dive project case study rendering (`/projects/<slug>`).
* 404 and 500 error handlers.
* Contact form submission and database persistence.
* `robots.txt` and `sitemap.xml` SEO generation.
* Admin authentication, session cookies, and login protections.
* Admin project creation, editing, and deletion.

---

## 🚢 Deployment Guide

### Deploying to Modern PaaS (Render / Railway / Fly.io / Heroku)

1. **Procfile**:
   Create a `Procfile`:
   ```text
   web: gunicorn run:app
   ```
   Add `gunicorn` to `requirements.txt`:
   ```bash
   pip install gunicorn
   ```

2. **Environment Variables on Host**:
   * `FLASK_ENV=production`
   * `SECRET_KEY=<generate-a-64-character-random-hex>`
   * `DATABASE_URL=<provided-by-your-managed-postgresql-instance>`
   * `ADMIN_USERNAME=rami`
   * `ADMIN_EMAIL=rami.khaled@example.dz`
   * `ADMIN_PASSWORD=<secure-production-password>`

3. **Release Command**:
   Set your deployment build/release command:
   ```bash
   flask db upgrade && python seed.py
   ```

---

## 🔒 Security & Best Practices

* **Password Security**: Passwords hashed with PBKDF2/SHA-256 via Werkzeug.
* **CSRF Protection**: All POST forms include strict CSRF token validation via Flask-WTF.
* **SQL Injection Prevention**: Safe parameter binding handled by SQLAlchemy ORM.
* **Open Redirect Protection**: Next-url validation during authentication.
* **Environment Isolation**: Secrets stored in `.env`, excluded from git via `.gitignore`.
* **Honest Representation**: No synthetic awards or exaggerated metrics.

---

## 📄 License & Credits
Designed and engineered for **Rami Khaled**.
© 2026 Rami Khaled. All rights reserved.
