from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from linegest.phoneline.models import Category


class Command(BaseCommand):
    help = "Load Category"

    def handle(self, *args, **options):
        list_categories = [{'name': 'Site Géographique', 'tag': 'GEO'},
                           {'name': 'Bâtiment', 'tag': 'BAT'},
                           {'name': 'Ligne Techniques', 'tag': 'TECH_LIGNE'},
                           {'name': 'Statut de taxation', 'tag': 'STATUT_TAXA'},
                           {'name': 'Centre de taxation', 'tag': 'CENTRE_TAXA'},
                           {'name': 'Not define', 'tag': 'NOT_DEF'}]
        for category in list_categories:
            cat, created = Category.objects.get_or_create(
                tag=category['tag'],
                defaults=dict(name=category['name']),
            )

            self.stdout.write(
                self.style.NOTICE(
                    f"{cat.pk} - {cat.tag} - {cat.name} => {created}"
                )
            )