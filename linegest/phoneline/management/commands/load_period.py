from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from linegest.phoneline.models import Period


class Command(BaseCommand):
    help = "Create Period for Years in Range 2023 to Years today + 1"

    def add_arguments(self, parser):
        # begin year
        parser.add_argument(
            'start_year',
            type=int,
            help="Start year of range to period",
        )

        parser.add_argument(
            '-e', '--end_year',
            default=None,
            type=int,
            help="End year of range to create period",
        )



    def handle(self, *args, **options):
        # Récupération des arguments :
        start_year = options.get('start_year')
        end_year = options.get('end_year')
        self.stdout.write(
            self.style.NOTICE(
                f"===== Fin Année : {end_year} ====="
            )
        )

        if end_year is None:
            end_year = start_year + 1
        else:
            end_year = end_year + 1

        new_years = [year for year in range(start_year, end_year)]
        for new_year in new_years:
            missing_months = Period.get_missing_month(year=new_year)
            self.stdout.write(
                self.style.NOTICE(
                    f"===== Année : {new_year} ====="
                )
            )
            if missing_months:
                for missing_month in missing_months:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Création de la période : {new_year}-{missing_month}"
                        )
                    )
                    p = Period.objects.create(year=new_year, month=missing_month)
                    p.save()
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Les période de l'année : {new_year} existe déjà"
                    )
                )
