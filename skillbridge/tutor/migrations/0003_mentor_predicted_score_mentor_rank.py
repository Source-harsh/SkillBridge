# Generated by Django 5.1.4 on 2024-12-20 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0002_remove_mentor_availability_end_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentor',
            name='predicted_score',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mentor',
            name='rank',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
