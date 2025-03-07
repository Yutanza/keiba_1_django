# Generated by Django 5.1.5 on 2025-01-27 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_1', '0013_alter_payout_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='raceentry',
            name='OrderOfFinish',
        ),
        migrations.AddField(
            model_name='raceentry',
            name='order_of_finish',
            field=models.IntegerField(blank=True, null=True, verbose_name='順位'),
        ),
        migrations.AlterField(
            model_name='jockey',
            name='name',
            field=models.CharField(max_length=100, verbose_name='騎手名'),
        ),
        migrations.AlterField(
            model_name='race',
            name='race_id',
            field=models.CharField(max_length=20, unique=True, verbose_name='レースID'),
        ),
        migrations.AlterField(
            model_name='race',
            name='race_type',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='レースタイプ'),
        ),
        migrations.AlterField(
            model_name='trainer',
            name='name',
            field=models.CharField(max_length=100, verbose_name='調教師名'),
        ),
    ]
