# Generated by Django 3.2.9 on 2023-01-05 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_auto_20230105_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='directors',
            field=models.ManyToManyField(blank=True, to='movies.Director'),
        ),
    ]
