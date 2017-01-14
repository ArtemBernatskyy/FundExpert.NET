import json

from django.utils import timezone
from django.db import transaction
from django.core.management.base import BaseCommand

from mutual_funds.finance.models import FinanceSector
from mutual_funds.finance.parsers.sectors_parser import SectorsParser


class Command(BaseCommand):
    help = 'update daily sectors'

    def handle(self, *args, **options):
        # daily updating sectors data via cron
        sectors_parser = SectorsParser()
        sectors_parser.parse()

        with transaction.atomic():
            for parsed_name, sector_data in sectors_parser.parsed_data.items():
                data_update = {
                    'cumulative_usd': json.dumps(sector_data[0]),
                    'cumulative_eur': json.dumps(sector_data[1]),
                    'discrete_usd': json.dumps(sector_data[2]),
                    'discrete_eur': json.dumps(sector_data[3]),
                }
                data_default = {
                    'name': parsed_name,
                    'cumulative_usd': json.dumps(sector_data[0]),
                    'cumulative_eur': json.dumps(sector_data[1]),
                    'discrete_usd': json.dumps(sector_data[2]),
                    'discrete_eur': json.dumps(sector_data[3]),
                }
                instance, created = FinanceSector.objects.get_or_create(
                    parsed_name=parsed_name,
                    defaults=data_default,
                )
                if not created:
                    for attr, value in data_update.items():
                        setattr(instance, attr, value)
                    instance.last_parsed = timezone.now()
                    instance.save()
            self.stdout.write(self.style.SUCCESS("Sectors Updated: {0} ".format(timezone.now())))
