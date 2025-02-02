#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mickey.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # Si la commande est "runserver" et que la variable d'environnement PORT est définie,
    # on modifie les arguments pour écouter sur 0.0.0.0:$PORT
    if len(sys.argv) > 1 and sys.argv[1] == "runserver":
        port = os.environ.get("PORT")
        if port:
            # Si aucun port n'est précisé dans la commande, on l'ajoute.
            if len(sys.argv) == 2:
                sys.argv.append("0.0.0.0:" + port)
            else:
                # Sinon, on remplace le port spécifié par celui défini dans l'environnement.
                sys.argv[2] = "0.0.0.0:" + port
    main()
