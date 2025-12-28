# Flask Blog

A modern, minimal blog application built with Flask. Features include user authentication, profile management, blog post CRUD operations, email-based password reset, and a clean, responsive UI inspired by Apple's design principles.

## Features

- **User Management**

  - User registration with email validation
  - Secure login/logout with Flask-Login
  - Password hashing with Bcrypt
  - Profile picture upload with automatic resizing
  - Password reset via email tokens (30-minute expiry)

- **Blog Posts**

  - Create, read, update, delete (CRUD) blog posts
  - Author-only post editing and deletion
  - Timestamp for each post (UTC timezone-aware)
  - Posts ordered by creation date (newest first)

- **UI/UX**

  - Responsive Bootstrap 5 templates
  - Apple-inspired modern design system
  - Paginated post listings (10 posts per page)
  - User profile pages with author's posts
  - Clean error pages (404, 403, 500)

- **Email**
  - Password reset notifications via SMTP
  - Gmail, Mailtrap, or custom SMTP support
  - Secure token-based reset links

## Tech Stack

- **Backend**: Flask, Flask-SQLAlchemy, Flask-Login, Flask-Bcrypt, Flask-Mail
- **Frontend**: Bootstrap 5, Jinja2 templates, custom CSS
- **Database**: SQLite (development), upgradeable to PostgreSQL/MySQL
- **Authentication**: Flask-Login + Bcrypt
- **Forms**: Flask-WTF with validation
- **Image Processing**: Pillow

## Prerequisites

- Python 3.10+
- pip (or `uv` for fast dependency resolution)
- Git
- Email account (Gmail recommended for password reset feature)

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/rex-1234/flask_blog.git
cd FLASK_BLOG
```

### 2. Create a virtual environment

```bash
uv venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
uv sync
```

### 4. Configure environment variables

```bash
export EMAIL_USER="your_email@example.com"
export EMAIL_PASS="your_app_password"
export SECRET_KEY="your_secret_key"
export SQLALCHEMY_DATABASE_URI="sqlite:///site.db"
```

### 5. Initialize the database

```bash
python - <<'PY'
from flaskblog import create_app, db
app = create_app()
with app.app_context():
  db.create_all()
print('Database created successfully')
PY
```

### 6. Run the application

#### Using Python directly

```bash
python run.py
```

#### or using uv (if available)

```bash
uv run run.py
```

#### or using Flask CLI

```bash
export FLASK_APP=run.py
flask run
```
