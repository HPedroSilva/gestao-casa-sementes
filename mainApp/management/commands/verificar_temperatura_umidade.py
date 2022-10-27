import kronos
from django.core.management.base import BaseCommand
from datetime import datetime

@kronos.register("0 0 * * *")
class Command(BaseCommand):
    help=""
    def handle(self, *args, **options):
        """
        
        """
        