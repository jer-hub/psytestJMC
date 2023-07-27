# Generated by Django 3.2.7 on 2023-07-26 14:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0045_remove_educationlevel_name2'),
        ('personalityTest', '0023_alter_result_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='personality_result_user', to='accounts.profile'),
        ),
    ]
