# Generated by Django 5.1.4 on 2024-12-27 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_result_total_marks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='total_marks',
            field=models.FloatField(null=True),
        ),
    ]
