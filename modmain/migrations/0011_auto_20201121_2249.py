# Generated by Django 3.1.1 on 2020-11-21 17:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('modmain', '0010_auto_20201121_2234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team_memeber_details',
            name='date_of_request',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='team_memeber_details',
            name='verified',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
