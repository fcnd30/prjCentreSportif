# Generated by Django 5.0.6 on 2024-06-28 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CentreSportif', '0011_client_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='username',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
