from datetime import datetime

from django.core.management.base import BaseCommand

from mutual_funds.finance.models import Fund
from mutual_funds.finance.parsers.funds_updater import FundParser


class Command(BaseCommand):
    help = 'update daily funds history'

    def handle(self, *args, **options):
        # daily updating via cron
        funds = Fund.objects.parsing()
        for fund in funds:
            FundParser(fund).update()
            self.stdout.write(self.style.SUCCESS("Updated fund:{1}:  {0} ".format(fund.name, datetime.now())))
