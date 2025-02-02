"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mickey.settings')
    port = os.environ.get('PORT', '10000')

    from django.core.management import execute_from_command_line

    if len(sys.argv) == 1:
        sys.argv.extend(['runserver', f'0.0.0.0:{port}'])

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
