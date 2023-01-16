# Generated by Django 3.2.9 on 2023-01-16 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0023_auto_20230116_1307'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='comments',
        ),
        migrations.AddField(
            model_name='comment',
            name='movie',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='movies.movie'),
        ),
    ]
