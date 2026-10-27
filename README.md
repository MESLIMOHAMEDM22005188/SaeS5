# CyberMouse Academy

CyberMouse Academy is a Django web application for learning practical cybersecurity habits through guided levels, quizzes, and interactive simulations.

## Technology stack

- Python and Django
- Django templates, CSS, and JavaScript
- Django authentication and session management
- SQLite for local development; configurable external databases for deployment
- Gunicorn and WhiteNoise for production serving
- Optional Twilio integration for SMS verification

## Project structure

```text
config/                 Django project configuration (settings, URLs, ASGI, WSGI)
academy/                Application views, forms, models, tests, templates, and static assets
academy/migrations/     Historical database migrations
manage.py               Django management entry point
Procfile                Production web process
requirements.txt         Python dependencies
.env.example            Environment-variable template
```

The application keeps the historical Django app label `mousey` to preserve existing database table names and migration history. The Python package itself is now named `academy`.

## Local setup

Python 3.12 is recommended.

```bash
git clone https://github.com/MESLIMOHAMEDM22005188/SaeS5.git
cd SaeS5
python -m venv .venv
```

Activate the environment:

- Windows PowerShell: `.venv\\Scripts\\Activate.ps1`
- macOS/Linux: `source .venv/bin/activate`

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Create a local `.env` file based on `.env.example`. Generate a unique secret key:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

Minimum local configuration:

```dotenv
SECRET_KEY=replace-with-a-generated-secret
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

Run checks, apply migrations, and start the development server:

```bash
python manage.py check
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/.

## Production configuration

Set environment variables in the hosting provider dashboard. Do not commit `.env` or production credentials.

Required settings:

- `SECRET_KEY`: unique, randomly generated secret
- `DEBUG=False`
- `ALLOWED_HOSTS`: comma-separated hostnames
- `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT` for an external database
- `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, and `DEFAULT_FROM_EMAIL` for SMTP
- `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, and `TWILIO_PHONE_NUMBER` for SMS delivery

A persistent external database is recommended for production. Confirm that migrations, static-file collection, email delivery, SMS delivery, registration, and verification work in the target hosting environment before launch.

## Quality checks

```bash
python -m compileall -q config academy
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py collectstatic --noinput
python manage.py test
```

GitHub Actions runs these checks on pushes and pull requests.

## Security notes

- Never commit secrets or real user credentials.
- The password-strength game stores only a non-sensitive game state, not the submitted password.
- Verification codes expire and should never be logged.
- Keep `DEBUG=False` in production.
- Historical migration filenames retain their original names to avoid breaking existing migration records.
- Some legacy game pages and database fields still need a dedicated follow-up refactor; validate the complete application before deploying.
