# Generated by Django 4.1.2 on 2022-12-12 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apps", "0010_remove_basic_pulls_basic_close_pulls_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="basic",
            name="id",
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]