# Use Python 3.13 (stable, close to 3.14 used in dev)
FROM python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=night_market.settings

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libmariadb-dev-compat \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
# The project uses MySQL/PyMySQL, but for Railway we switch to PostgreSQL
# or keep SQLite for simplicity. We'll install both DB drivers.
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn psycopg[binary] dj-database-url

# Copy project
COPY . .

# Build frontend (optional - comment out if deploying frontend separately)
# RUN cd frontend && npm install && npm run build

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Expose port
EXPOSE $PORT

# Run gunicorn
CMD gunicorn night_market.wsgi:application --bind 0.0.0.0:$PORT --workers 4 --timeout 120
