# Generated by Django 4.1.2 on 2022-12-12 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apps", "0012_remove_user_organizations_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user", name="type", field=models.CharField(max_length=20),
        ),
    ]
