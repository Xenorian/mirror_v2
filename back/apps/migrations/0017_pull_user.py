# Generated by Django 4.1.2 on 2022-12-12 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apps", "0016_remove_user_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="pull",
            name="user",
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
    ]
