# Generated by Django 5.1.4 on 2024-12-27 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_rename_subject1_subject_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='percentage',
        ),
    ]