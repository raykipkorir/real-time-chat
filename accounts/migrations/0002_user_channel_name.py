# Generated by Django 5.0.1 on 2024-01-21 09:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="channel_name",
            field=models.CharField(max_length=500, null=True),
        ),
    ]
