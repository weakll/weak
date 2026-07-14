# Deploy Guide: Night Market Website
# =================================

## Architecture
- Frontend: Vue 3 + Vite (deployed to Vercel)
- Backend: Django 6 + DRF (deployed to Railway)

## Option A: Deploy Backend to Railway (Recommended)

1. Create a Railway account at https://railway.app
2. Install Railway CLI: npm install -g @railway/cli
3. In the project root, run:
   railway login
   railway init
   railway up
4. Add PostgreSQL plugin in Railway dashboard
5. Set environment variables in Railway dashboard:
   - DJANGO_SECRET_KEY: (generate a secure random key)
   - DJANGO_DEBUG: False
   - DJANGO_ALLOWED_HOSTS: your-railway-url.up.railway.app
   - CORS_ALLOWED_ORIGINS: https://your-vercel-app.vercel.app
   - DJANGO_CSRF_TRUSTED_ORIGINS: https://your-railway-url.up.railway.app
   - (DATABASE_URL is auto-set by Railway PostgreSQL plugin)
6. Run migrations: railway run python manage.py migrate
7. Seed data: railway run python manage.py seed_all

## Option B: Deploy Frontend to Vercel

1. Create a Vercel account at https://vercel.com
2. Install Vercel CLI: npm install -g vercel
3. In the frontend/ directory:
   vercel login
   vercel
4. Set environment variables in Vercel dashboard:
   - (Vite automatically handles env vars prefixed with VITE_)

## Option C: Single VPS Deployment (Docker Compose)

1. Copy .env.example to .env and fill in values
2. Run: docker-compose up -d
3. Run migrations: docker-compose exec backend python manage.py migrate
4. Seed data: docker-compose exec backend python manage.py seed_all

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| DJANGO_SECRET_KEY | No | (dev key) | Django secret key (change in prod) |
| DJANGO_DEBUG | No | True | Set to False in production |
| DJANGO_ALLOWED_HOSTS | No | (empty) | Comma-separated allowed hosts |
| DATABASE_URL | No | (MySQL dev) | PostgreSQL connection string |
| CORS_ALLOWED_ORIGINS | No | (empty) | Comma-separated CORS origins |

## Post-Deployment Steps

1. Create superuser: python manage.py createsuperuser
2. Visit /admin/ to manage store data
3. Seed data if needed: python manage.py seed_all
4. Test the API: GET /api/stores/
