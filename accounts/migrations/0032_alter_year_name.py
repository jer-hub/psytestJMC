# Generated by Django 3.2.7 on 2022-05-05 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0031_year_educationallevel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='year',
            name='name',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='Year'),
        ),
    ]