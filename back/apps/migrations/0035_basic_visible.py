# Generated by Django 4.1.2 on 2022-12-16 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apps", "0034_company_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="basic", name="visible", field=models.BooleanField(default=True),
        ),
    ]
