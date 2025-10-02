# Django web-app

Django web-app with PostgreSQL Backend, configured for production deployment with security best practices.

You should have an existing PostgreSQL database to use this app.

## Installation

```console
git clone https://github.com/dxas90/django-postgresql-gunicorn.git
cd django-postgresql-gunicorn
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

This application uses environment variables for configuration. Copy `.env.example` to `.env` and configure:

```console
cp .env.example .env
# Edit .env with your settings
```

### Required Environment Variables

#### Django Core Settings

- **DJANGO_SECRET_KEY**: Django secret key. Generate with:
  ```python
  python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
  ```
- **DJANGO_DEBUG**: Set to `False` in production (default: `False`)
- **DJANGO_ALLOWED_HOSTS**: Comma-separated list of allowed hosts (e.g., `yourdomain.com,www.yourdomain.com`)

#### Database Configuration

- **DB_NAME**: PostgreSQL database name
- **DB_USER**: Database user
- **DB_PASSWORD**: Database password
- **DB_HOST**: Database host (default: `localhost`)
- **DB_PORT**: Database port (default: `5432`)
- **DB_CONN_MAX_AGE**: Connection pool lifetime in seconds (default: `60`)
- **DB_CONNECT_TIMEOUT**: Connection timeout in seconds (default: `10`)

#### Security Settings (Production)

Enable these settings when deploying with HTTPS:

- **SECURE_HSTS_SECONDS**: HTTP Strict Transport Security age (recommended: `31536000` for 1 year)
- **SECURE_HSTS_INCLUDE_SUBDOMAINS**: Enable HSTS for subdomains (`True`/`False`)
- **SECURE_SSL_REDIRECT**: Redirect all HTTP requests to HTTPS (`True`/`False`)
- **SESSION_COOKIE_SECURE**: Use secure cookies for sessions (`True`/`False`)
- **CSRF_COOKIE_SECURE**: Use secure cookies for CSRF tokens (`True`/`False`)
- **CSRF_TRUSTED_ORIGINS**: Comma-separated list of trusted origins (e.g., `https://yourdomain.com`)

#### Logging

- **DJANGO_LOG_LEVEL**: Logging level (default: `INFO`, options: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`)

### Gunicorn Configuration

Gunicorn settings can be customized via environment variables. See `.env.example` for all available options.

## Running the Application

### Development

```console
# Run Django development server
python manage.py runserver
```

### Production

```console
# Run database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Run with Gunicorn
gunicorn xproject.wsgi:application -c gunicorn.conf.py
```

### Using Docker

```console
docker compose up -d
```

## Security Checklist for Production

Before deploying to production, ensure:

- [ ] `DJANGO_SECRET_KEY` is set to a unique, randomly generated value
- [ ] `DJANGO_DEBUG` is set to `False`
- [ ] `DJANGO_ALLOWED_HOSTS` contains only your domain(s)
- [ ] Database credentials are set via environment variables (not in code)
- [ ] HTTPS is configured and security settings are enabled:
  - [ ] `SECURE_HSTS_SECONDS=31536000`
  - [ ] `SECURE_HSTS_INCLUDE_SUBDOMAINS=True`
  - [ ] `SECURE_SSL_REDIRECT=True`
  - [ ] `SESSION_COOKIE_SECURE=True`
  - [ ] `CSRF_COOKIE_SECURE=True`
  - [ ] `CSRF_TRUSTED_ORIGINS` is configured
- [ ] Regular database backups are configured
- [ ] Log monitoring is in place

## Security Features

This application implements the following security best practices:

- **No hardcoded secrets**: All sensitive configuration via environment variables
- **Secure defaults**: DEBUG defaults to False, restrictive ALLOWED_HOSTS
- **HTTPS enforcement**: Optional SSL redirect and HSTS support
- **Secure cookies**: Session and CSRF cookies can be marked secure
- **XSS protection**: Browser XSS filter enabled
- **Clickjacking protection**: X-Frame-Options set to DENY
- **Content type sniffing protection**: X-Content-Type-Options set to nosniff
- **Database connection management**: Connection pooling with timeouts
- **HTTP method validation**: Views enforce allowed HTTP methods
- **Structured logging**: Configurable logging for observability

## Development

```console
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test
```
