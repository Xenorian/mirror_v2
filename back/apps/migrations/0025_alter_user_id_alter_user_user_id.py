# Generated by Django 4.1.2 on 2022-12-14 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apps", "0024_user_user_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user", name="id", field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="user",
            name="user_id",
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
