# Generated by Django 3.2.7 on 2022-05-16 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0034_alter_program_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='level',
            field=models.CharField(blank=True, choices=[('COLLEGE', 'College Department'), ('IBED', 'Integrated Basic Education Department')], max_length=64, null=True),
        ),
    ]