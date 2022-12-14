# Generated by Django 4.1.4 on 2022-12-12 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [(
        'fot',
        '0002_wage_department_wage_rate_squashed_'
        '0003_wage_district_coefficient'
    ),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wage',
            options={'ordering': ('employee', 'created')},
        ),
        migrations.AlterField(
            model_name='wage',
            name='monthly_premium',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='wage',
            name='quarterly_premium',
            field=models.FloatField(default=0),
        ),
    ]
