# Generated by Django 5.1.5 on 2025-01-22 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_1', '0006_alter_raceentry_gate_alter_raceentry_horse_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='race',
            name='race_id',
            field=models.IntegerField(max_length=20, unique=True, verbose_name='レースID'),
        ),
    ]
