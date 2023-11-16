import sys
import time

from django.core.management import call_command, CommandError
from django.db import connection
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Django command that waits for database to be available"""

    def handle(self, *args, **options):
        """Handle the command"""
        self.stdout.write('Waiting for database...')
        db_conn = None
        while not db_conn:
            try:
                connection.ensure_connection()
                db_conn = True
            except OperationalError:
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(2)
        try:
            call_command('migrate')
        except CommandError as e:
            sys.exit(str(e))

        self.stdout.write(self.style.SUCCESS('Database available!'))