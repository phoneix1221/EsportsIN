# Generated by Django 3.1.1 on 2020-12-04 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modmain', '0013_auto_20201201_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='team_description',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]