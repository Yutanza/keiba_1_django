# Generated by Django 5.1.5 on 2025-01-22 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_1', '0008_alter_cornerpassagerank_corner_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payout',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=12, null=True, verbose_name='金額'),
        ),
    ]
