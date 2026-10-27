# CyberMouse — plateforme pédagogique de cybersécurité

CyberMouse est une application web Django conçue comme une expérience d'apprentissage ludique autour des réflexes de cybersécurité. Elle propose des niveaux et des exercices, des quiz et des mécanismes de compte utilisateur.

> Projet universitaire (SAE S5). Le dépôt est en cours de modernisation : certaines fonctions historiques peuvent nécessiter une configuration locale avant d'être pleinement exécutables.

## Stack

- Python et Django
- Templates HTML, CSS et JavaScript
- Authentification Django
- Base de données configurable par variables d'environnement
- Gunicorn pour l'exécution WSGI en production

## Fonctionnalités présentes dans le code

- Création de compte et connexion
- Vérification de compte par e-mail et SMS (intégrations externes à configurer)
- Parcours pédagogique découpé en niveaux
- Quiz et enregistrement des scores
- Interface d'administration Django

## Installation locale

Python 3.11 ou plus récent est recommandé. Les versions exactes compatibles devront être validées dans l'environnement du projet.

```bash
git clone https://github.com/MESLIMOHAMEDM22005188/SaeS5.git
cd SaeS5
python -m venv .venv
```

Active l'environnement :

- Windows PowerShell : `.venv\\Scripts\\Activate.ps1`
- macOS / Linux : `source .venv/bin/activate`

Puis installe les dépendances :

```bash
python -m pip install -r requirements.txt
```

Crée un fichier `.env` à la racine à partir de cet exemple minimal :

```dotenv
SECRET_KEY=replace-with-a-long-random-secret
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

Ne publie jamais le fichier `.env`. Génère une vraie clé secrète avec :

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

Lance ensuite les vérifications et migrations :

```bash
python manage.py check
python manage.py migrate
python manage.py runserver
```

Le serveur local est disponible sur http://127.0.0.1:8000/.

## Configuration de production

Définis les variables d'environnement dans le tableau de bord de ton hébergeur, jamais dans Git :

- `SECRET_KEY` : clé secrète aléatoire
- `DEBUG=False`
- `ALLOWED_HOSTS` : domaines sans protocole, séparés par des virgules
- `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` : paramètres de base de données
- `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL`
- `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER` pour le SMS

Avant de déployer, vérifie les migrations, les fichiers statiques, l'envoi d'e-mail, les flux d'inscription et de vérification et les paramètres de sécurité Django. L'application utilise des données persistantes : configure une base distante pour la production plutôt qu'un fichier SQLite éphémère.

## Contrôles qualité

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

## Sécurité

- Aucun secret ne doit être stocké dans les fichiers suivis par Git.
- N'enregistre jamais des mots de passe utilisateurs en clair.
- Les codes de vérification doivent expirer, être limités en tentatives et ne pouvoir valider que le compte associé.
- Ne déploie pas avec `DEBUG=True`.
- La base SQLite locale n'est pas un environnement de données de production.

## Limites connues / prochaines étapes

- Ajouter des tests automatisés sur l'inscription, les vérifications et les quiz.
- Extraire la logique métier des vues et supprimer les duplications entre niveaux.
- Corriger et sécuriser la sauvegarde des données de mot de passe du jeu.
- Remplacer les identifiants de démonstration codés en dur.
- Documenter la procédure de déploiement réelle et vérifier l'hébergement actuel.
