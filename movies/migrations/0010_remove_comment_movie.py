# Generated by Django 3.2.9 on 2023-01-11 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0009_alter_comment_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='movie',
        ),
    ]