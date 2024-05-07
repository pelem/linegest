from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from linegest.phoneline.models import StatusTaxatLine


class Command(BaseCommand):
    help = "Load Statuts taxa"

    def handle(self, *args, **options):
        list_status_taxa = [{'name': 'NOT_DEFINE'},
                            {'name': 'TAXANT_NON'},
                            {'name': 'TAXANT_OUI'}]

        for status_taxa in list_status_taxa:
            st, created = StatusTaxatLine.objects.get_or_create(
                name=status_taxa['name']
            )

            self.stdout.write(
                self.style.NOTICE(
                    f"{st.pk} - {st.name} => {created}"
                )
            )