# Generated by Django 4.1.4 on 2023-02-28 03:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fot', '0006_wage_aprooved'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wage',
            options={'ordering': ('employee', 'aprooved')},
        ),
    ]