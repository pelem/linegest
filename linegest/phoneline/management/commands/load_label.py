from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from linegest.phoneline.models import Label, Category


class Command(BaseCommand):
    help = "Load Label"

    def handle(self, *args, **options):
        list_labels = [
            {'id': 1, 'display_name': 'label_1', 'description': 'label taxant structure 1'},
            {'id': 2, 'display_name': 'label_2', 'description': 'label taxant structure 2'},
            {'id': 3, 'display_name': 'label_3', 'description': 'label taxant structure 3'},
            {'id': 4, 'display_name': 'label_20', 'description': 'label site 20'},
            {'id': 5, 'display_name': 'label_30', 'description': 'label bâtiment 30'}
        ]

        for label in list_labels:
            lb, created = Label.objects.get_or_create(
                label_id=label['id'],
                defaults=dict(display_name=label['display_name'], description=label['description']),
                )

            self.stdout.write(
                self.style.NOTICE(
                    f"{lb.pk} - {lb.display_name} - {lb.label_id} => {created}"
                )
            )

        list_label_structure = Label.objects.filter(display_name__regex=r'label_[1-9]$')
        cat_ct = Category.objects.get(tag='CENTRE_TAXA')
        cat_geo =  Category.objects.get(tag='GEO')
        cat_bat = Category.objects.get(tag='BAT')

        for label in list_label_structure:
            label.category = cat_ct
            label.save()

        label_geo = Label.objects.get(label_id=4)
        label_geo.category = cat_geo
        label_geo.save()
        label_bat = Label.objects.get(label_id=5)
        label_bat.category = cat_bat
        label_bat.save()





