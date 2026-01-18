#!/usr/bin/env bash
set -e

DB_PATH="instance/site.db"

echo "Checking database state..."

if [ -f "$DB_PATH" ]; then
  echo "Database already exists at $DB_PATH"
  echo "Skipping database initialization."
  exit 0
fi

echo "Database not found. Initializing..."

uv run python - <<'PY'
from flaskblog import create_app, db

app = create_app()

with app.app_context():
    db.create_all()
    print("Database tables created successfully.")
PY

echo "Database initialization complete."
