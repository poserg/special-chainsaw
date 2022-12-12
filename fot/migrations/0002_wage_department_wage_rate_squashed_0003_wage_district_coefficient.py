# Generated by Django 4.1.4 on 2022-12-12 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('fot', '0002_wage_department_wage_rate'), ('fot', '0003_wage_district_coefficient')]

    dependencies = [
        ('fot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wage',
            name='department',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='wage',
            name='rate',
            field=models.FloatField(default=1),
        ),
        migrations.AddField(
            model_name='wage',
            name='district_coefficient',
            field=models.FloatField(default=1),
        ),
    ]