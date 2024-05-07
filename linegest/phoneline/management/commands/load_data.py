from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from linegest.phoneline.models import Period, LinePhone, Label, StatusTaxatLine
from pathlib import Path
import csv



class Command(BaseCommand):
    help = "load data with csv file"

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            help="Path to the csv file",
        )



    def handle(self, *args, **options):
        # Récupération des arguments :
        csv_file = options.get('csv_file')
        self.stdout.write(
            self.style.NOTICE(
                f"==== Traitement du fichier {csv_file} ===="
            )
        )

        csv_file = Path(csv_file)
        if not csv_file.exists():
            raise CommandError()

        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                list_label = [Label.objects.get(display_name=label.lower()) for label in row.get('labels').split(';')]
                period = Period.objects.get(period_date=datetime.strptime(row.get('period'), '%Y-%m-%d').date())
                if row.get('statu_taxa'):
                    name_status_line = row.get('statu_taxa')
                else:
                    name_status_line = 'NOT_DEFINE'

                status_taxa_line = StatusTaxatLine.objects.get(name=name_status_line)
                line_phone = LinePhone.objects.create(phone_number=row.get('phone_number'), period=period, status_taxa_line=status_taxa_line)
                line_phone.save()
                line_phone.label.add(*list_label)
                line_phone.save()

