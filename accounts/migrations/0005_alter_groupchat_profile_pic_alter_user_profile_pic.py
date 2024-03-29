# Generated by Django 5.0.1 on 2024-01-28 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_alter_user_channel_name_groupchat"),
    ]

    operations = [
        migrations.AlterField(
            model_name="groupchat",
            name="profile_pic",
            field=models.ImageField(
                blank=True, null=True, upload_to="group_profile_pics"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="profile_pic",
            field=models.ImageField(
                blank=True, null=True, upload_to="personal_profile_pics"
            ),
        ),
    ]
