Flask Blog

A modern, minimal blog application built with Flask. Features include user authentication, profile management, blog post CRUD operations, email–based password reset, and a clean, responsive UI inspired by Apple’s design principles.

Setup Instructions
1. Clone the repository
git clone https://github.com/rex-1234/flask_blog.git
cd flask_blog

2. Create and activate environment using uv
uv venv
source .venv/bin/activate

3. Install project dependencies
uv sync

4. Set required environment variables

Create a .env file or export the values directly:

export EMAIL_USER="your_email@example.com"
export EMAIL_PASS="your_app_password"
export SECRET_KEY="your_secret_key"
export SQLALCHEMY_DATABASE_URI'='sqlite:///site.db'


These are used for:

Flask session security

Sending password reset emails

5. Run the application
flask --app flaskblog run --debug

Features
– User Management

User registration with email validation

Secure login/logout with Flask-Login

Password hashing with Bcrypt

Profile picture upload with automatic resizing

Password reset via email tokens (30-minute expiry)

– Blog Posts

Create, read, update, delete (CRUD) blog posts

Author-only post editing and deletion

Timestamp for each post (UTC timezone-aware)

Posts ordered by creation date (newest first)

– UI/UX

Responsive Bootstrap 5 templates

Apple-inspired modern design system

Clean, minimal layout for readability

Email Reset Workflow

User submits their email

A timed (30-minute) secure token is generated

User receives reset link via email

User sets a new password

Tech Stack

Flask — core backend

Flask-Login — authentication

Flask-SQLAlchemy — ORM

Flask-Bcrypt — password hashing

Jinja2 — templating

SQLite — default database

Bootstrap 5 — UI framework

Run Database Commands

Use the app context:

from flaskblog import app, db
with app.app_context():
    db.create_all()

License

This project is for learning and personal use.
