# Generated by Django 3.2.9 on 2023-01-17 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0024_auto_20230116_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='rate',
            field=models.FloatField(choices=[(1, '⭐'), (2, '⭐⭐'), (3, '⭐⭐⭐'), (4, '⭐⭐⭐⭐'), (5, '⭐⭐⭐⭐⭐')]),
        ),
    ]
