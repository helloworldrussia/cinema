# Generated by Django 3.2.9 on 2023-01-05 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_auto_20230105_1328'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='directors',
        ),
        migrations.AddField(
            model_name='movie',
            name='directors',
            field=models.ManyToManyField(blank=True, null=True, to='movies.Director'),
        ),
    ]
