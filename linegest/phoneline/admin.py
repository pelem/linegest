from django.contrib import admin
from .models import Period, StatusTaxatLine, Category

# Register your models here.

# Register your models here.
@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    pass


@admin.register(StatusTaxatLine)
class StatusTaxatLineAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
