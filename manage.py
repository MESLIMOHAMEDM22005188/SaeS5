#!/usr/bin/env python
"""Run Django management commands."""
import os
import sys


def main():
    """Run the command-line utility."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django could not be imported. Install the requirements and activate "
            "the virtual environment before running management commands."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
