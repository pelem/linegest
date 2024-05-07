# Generated by Django 5.0.4 on 2024-05-06 11:56

import django.db.models.deletion
import linegest.phoneline.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phoneline', '0002_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusTaxatLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, unique=True)),
            ],
            options={
                'verbose_name': 'Status de taxation',
                'verbose_name_plural': 'Status de taxation',
            },
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label_id', models.IntegerField()),
                ('display_name', models.CharField(max_length=255, verbose_name='Nom du Label')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('category', models.ForeignKey(default=linegest.phoneline.models.Category.get_default_pk, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='labels', to='phoneline.category', verbose_name='Category')),
            ],
        ),
        migrations.CreateModel(
            name='LinePhone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=10)),
                ('label', models.ManyToManyField(blank=True, related_name='line_phones', to='phoneline.label')),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='line_phones', to='phoneline.period')),
                ('status_taxa_line', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='line_phones', to='phoneline.statustaxatline')),
            ],
        ),
    ]
