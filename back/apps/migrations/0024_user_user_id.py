# Generated by Django 4.1.2 on 2022-12-14 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apps", "0023_user_owner_user_repo"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="user_id",
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
    ]
