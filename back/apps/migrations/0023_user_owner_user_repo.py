# Generated by Django 4.1.2 on 2022-12-14 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apps", "0022_rename_sha_commit_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="owner",
            field=models.CharField(default="pytorch", max_length=50),
        ),
        migrations.AddField(
            model_name="user",
            name="repo",
            field=models.CharField(default="pytorch", max_length=50),
        ),
    ]
