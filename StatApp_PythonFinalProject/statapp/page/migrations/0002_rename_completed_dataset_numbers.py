# Generated by Django 5.0.4 on 2024-04-09 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dataset',
            old_name='completed',
            new_name='numbers',
        ),
    ]
