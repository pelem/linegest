from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime


class Period(models.Model):
    class Month(models.IntegerChoices):
        JANVIER = 1, _("Janvier")
        FEVRIER = 2, _("Février")
        MARS = 3, _('Mars')
        AVRIL = 4, _("Avril")
        MAI = 5, _("Mai")
        JUIN = 6, _("Juin")
        JUILLET = 7, _("Juillet")
        AOUT = 8, _("Août")
        SEPTEMBRE = 9, _("Septembre")
        OCTOBRE = 10, _("Octobre")
        NOVEMBRE = 11, _("Novembre")
        DECEMBRE = 12, _("Décembre")

        def __str__(self):
            return f"{self.name}"

    year = models.IntegerField()
    month = models.IntegerField('Month', choices=Month)
    period_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_month_display()}-{self.year}"

    @classmethod
    def get_id_period(cls, year, month):
        periods = cls.objects.filter(year=year, month=month)
        if periods:
            return periods[0].id

    @property
    def get_period_date(self):
        return datetime.strptime(f'{self.year}-{self.month}-01', '%Y-%m-%d').date()


    @classmethod
    def get_list_month(cls):
        return [month.value for month in cls.Month]

    @classmethod
    def get_missing_month(cls, year):
        periods = cls.objects.filter(year=year)
        missing_months = [num_month for num_month in [x for x in range(1,13)] if num_month not in [period.month for period in periods]]
        return missing_months

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['year', 'month'], name='unique_period')
        ]

    def save(self, *args, **kwargs):
        if not self.period_date:
            self.period_date = self.get_period_date

        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=50)
    tag = models.CharField(max_length=20)

    @classmethod
    def get_default_pk(cls):
        category, created = cls.objects.get_or_create(
            tag='NOT_DEF',
            defaults=dict(name='Not define'),
        )
        return category.pk

    def __str__(self):
        return self.name


class StatusTaxatLine(models.Model):
    name = models.CharField(max_length=10, unique=True)

    class Meta:
        verbose_name = "Status de taxation"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Label(models.Model):
    label_id = models.IntegerField()
    display_name = models.CharField(max_length=255, verbose_name='Nom du Label')
    description = models.TextField(blank=True, verbose_name='Description')
    category = models.ForeignKey("Category",
                                   related_name='labels',
                                   on_delete=models.SET_DEFAULT,
                                   verbose_name="Category",
                                   default=Category.get_default_pk
                                   )

    def __str__(self):
        return self.display_name


class LinePhone(models.Model):
    phone_number = models.CharField(max_length=10)
    period = models.ForeignKey("Period", on_delete=models.CASCADE, related_name='line_phones')
    label = models.ManyToManyField("Label", blank=True, related_name='line_phones')
    status_taxa_line = models.ForeignKey("StatusTaxatLine", on_delete=models.CASCADE, related_name='line_phones')
