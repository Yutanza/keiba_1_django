# Generated by Django 5.1.5 on 2025-01-22 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_1', '0003_alter_race_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jockey',
            name='name',
            field=models.CharField(max_length=100, unique=None, verbose_name='騎手名'),
        ),
        migrations.AlterField(
            model_name='race',
            name='course',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='開催コース'),
        ),
        migrations.AlterField(
            model_name='race',
            name='date',
            field=models.DateField(blank=True, null=True, verbose_name='開催日'),
        ),
        migrations.AlterField(
            model_name='race',
            name='distance',
            field=models.IntegerField(blank=True, null=True, verbose_name='距離'),
        ),
        migrations.AlterField(
            model_name='race',
            name='no',
            field=models.IntegerField(blank=True, null=True, verbose_name='No'),
        ),
        migrations.AlterField(
            model_name='race',
            name='race_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='レース名'),
        ),
        migrations.AlterField(
            model_name='race',
            name='race_number',
            field=models.IntegerField(blank=True, null=True, verbose_name='開催回'),
        ),
        migrations.AlterField(
            model_name='race',
            name='race_type',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='レース'),
        ),
        migrations.AlterField(
            model_name='race',
            name='track_condition',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='馬場'),
        ),
        migrations.AlterField(
            model_name='race',
            name='weather',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='天候'),
        ),
        migrations.AlterField(
            model_name='race',
            name='year',
            field=models.IntegerField(blank=True, null=True, verbose_name='開催年'),
        ),
        migrations.AlterField(
            model_name='trainer',
            name='name',
            field=models.CharField(max_length=100, unique=None, verbose_name='調教師名'),
        ),
    ]
