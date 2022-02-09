# Generated by Django 3.2.7 on 2022-01-30 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0005_auto_20220129_2149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userfeedback',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='userfeedback',
            name='question',
        ),
        migrations.AddField(
            model_name='userfeedback',
            name='e_1',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userfeedback',
            name='e_2',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userfeedback',
            name='e_3',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userfeedback',
            name='e_4',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userfeedback',
            name='q_1',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userfeedback',
            name='q_2',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userfeedback',
            name='q_3',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userfeedback',
            name='q_4',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userfeedback',
            name='q_5',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userfeedback',
            name='q_6',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userfeedback',
            name='q_7',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userfeedback',
            name='q_8',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='UserRating',
        ),
    ]