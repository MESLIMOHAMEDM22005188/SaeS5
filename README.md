# CyberMouse Academy

CyberMouse Academy is a Django application that teaches practical cybersecurity habits through guided learning levels, quizzes, and interactive simulations.

## Stack

- Python 3.12 and Django 5.2
- Django templates, CSS, and vanilla JavaScript
- Django authentication and session management
- SQLite locally; configurable external database support
- Gunicorn and WhiteNoise for deployment
- Optional Twilio SMS verification

## Architecture

```text
config/                     Project settings, root URLs, ASGI/WSGI
academy/
  models.py                 Persistence models (legacy schema kept stable)
  forms.py                  Input validation
  admin.py                  Django admin
  urls.py                   Route declarations
  views/
    accounts.py             Registration, login, phone/email verification
    learning.py             Quizzes, scoring, learning-level pages
    games.py                Simulations and mini-games
    pages.py                General pages
  selectors/                Reusable database query functions
  services/                 Shared business operations
  templates/                Django HTML templates
  static/css/               Stylesheets
  static/js/                Browser-side behaviour
  static/image/             Existing images
  migrations/               Historical migrations
```

The historical Django app label (`mousey`) and migration files are intentionally preserved. Renaming models, the app label, or migration files requires a separate schema/data migration and is outside this low-risk refactor.

## Setup

```bash
git clone https://github.com/MESLIMOHAMEDM22005188/SaeS5.git
cd SaeS5
python -m venv .venv
```

Activate with `.venv\\Scripts\\Activate.ps1` on Windows PowerShell or `source .venv/bin/activate` on macOS/Linux.

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py check
python manage.py migrate
python manage.py runserver
```

Create `.env` from `.env.example` and generate a secret key:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

## Configuration

Set environment variables through the hosting provider. Never commit real secrets.

- `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`
- `DB_ENGINE`, `DB_NAME`; and `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` for an external database
- `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL`
- `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER` for optional SMS

## Quality checks

```bash
python -m compileall -q config academy
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py collectstatic --noinput
python manage.py test
```

## Security notes

- Never commit `.env`, production credentials, real passwords, or verification codes.
- The password-strength game persists only the strength category, never the submitted password.
- Verification codes expire after ten minutes and must never be logged.
- Keep `DEBUG=False` in production.
- Confirm database migrations, static-file collection, email/SMS delivery, registration, and verification before deployment.
- Asset filenames are retained in this structural pass; rename them in a dedicated change alongside all template/CSS/JavaScript references.
