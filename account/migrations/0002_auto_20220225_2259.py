# Generated by Django 3.2.6 on 2022-02-25 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clocking',
            name='clock_in',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clocking',
            name='clock_out',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
