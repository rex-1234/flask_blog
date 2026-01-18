# ---- Base image ----
FROM python:3.13-slim

# ---- Environment ----
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---- System dependencies ----
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       curl \
    && rm -rf /var/lib/apt/lists/*

# ---- Install uv ----
RUN pip install --no-cache-dir uv

# ---- Working directory ----
WORKDIR /app

# ---- Copy dependency files ----
COPY pyproject.toml uv.lock* ./

# ---- Install Python dependencies ----
RUN uv sync --no-dev

# ---- Copy application code ----
COPY flaskblog flaskblog
COPY run.py .
COPY init_db.sh .

# ---- Make init script executable ----
RUN chmod +x init_db.sh

# ---- Expose Flask port ----
EXPOSE 5000

# ---- Default command ----
CMD ["bash", "-c", "./init_db.sh && uv run python run.py"]
