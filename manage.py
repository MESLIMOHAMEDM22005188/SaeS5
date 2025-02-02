#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    # Configure le module de réglages Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mickey.settings')

    # Récupère le port depuis la variable d'environnement PORT (par défaut "10000")
    port = os.environ.get('PORT', '10000')

    from django.core.management import execute_from_command_line

    # Si aucun argument n'est passé (autre que le nom du script), lance runserver sur 0.0.0.0:<port>
    if len(sys.argv) == 1:
        sys.argv.extend(['runserver', f'0.0.0.0:{port}'])

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
