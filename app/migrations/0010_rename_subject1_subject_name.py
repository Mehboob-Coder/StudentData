# Generated by Django 5.1.4 on 2024-12-27 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_result_marks'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subject',
            old_name='subject1',
            new_name='name',
        ),
    ]
