# Generated by Django 5.1.5 on 2025-02-25 10:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_1', '0020_remove_racehtml_race_remove_racehtml_raceid'),
    ]

    operations = [
        migrations.AddField(
            model_name='racehtml',
            name='race',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='racehtml', to='App_1.race', verbose_name='レース'),
        ),
    ]
