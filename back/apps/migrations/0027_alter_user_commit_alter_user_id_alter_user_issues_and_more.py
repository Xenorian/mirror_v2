# Generated by Django 4.1.2 on 2022-12-14 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apps", "0026_alter_user_user_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user", name="commit", field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="user", name="issues", field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="login",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="owner",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="user", name="pulls", field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="repo",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="user", name="reviews", field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="user_id",
            field=models.CharField(max_length=50, null=True),
        ),
    ]
