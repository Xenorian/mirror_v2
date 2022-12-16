# Generated by Django 4.1.2 on 2022-12-10 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apps", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Contributor",
            fields=[
                (
                    "contributor_id",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                ("login", models.CharField(max_length=50, null=True)),
                ("project", models.CharField(max_length=50, null=True)),
                ("company", models.CharField(max_length=50, null=True)),
                ("contributions", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Issues",
            fields=[
                ("repo_name", models.CharField(default="pytorch", max_length=50)),
                (
                    "issue_id",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                ("number", models.CharField(max_length=10)),
                ("title", models.CharField(max_length=300)),
                ("locked", models.BooleanField()),
                ("state", models.CharField(max_length=10)),
                ("comments", models.IntegerField()),
                ("create_time", models.DateTimeField()),
                ("update_time", models.DateTimeField()),
                ("close_time", models.DateTimeField()),
                ("first_reply_time", models.DateTimeField()),
                ("user_login", models.CharField(max_length=50)),
                ("user_id", models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(model_name="house", name="user",),
        migrations.RemoveField(model_name="room", name="house",),
        migrations.DeleteModel(name="Device",),
        migrations.DeleteModel(name="House",),
        migrations.DeleteModel(name="Room",),
        migrations.DeleteModel(name="User",),
    ]
