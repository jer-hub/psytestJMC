# Generated by Django 3.2.7 on 2022-10-17 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0041_remove_profile_is_assigned'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='gender',
            new_name='sex',
        ),
    ]
