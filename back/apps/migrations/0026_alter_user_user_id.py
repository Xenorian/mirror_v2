# Generated by Django 4.1.2 on 2022-12-14 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apps", "0025_alter_user_id_alter_user_user_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="user_id",
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]