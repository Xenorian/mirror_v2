from django.db import models


# contributor
class Contributor(models.Model):
    contributor_id = models.CharField(max_length=50, null=False, primary_key=True)
    login = models.CharField(max_length=50, null=True)
    project = models.CharField(max_length=50, null=True)
    company = models.CharField(max_length=50, null=True)
    contributions = models.IntegerField()


class Issues(models.Model):
    repo_name = models.CharField(max_length=50, default="pytorch")
    issue_id = models.CharField(max_length=50, null=False, primary_key=True)
    number = models.CharField(max_length=10)
    title = models.CharField(max_length=300)
    locked = models.BooleanField()
    state = models.CharField(max_length=10)
    comments = models.IntegerField()
    created_at = models.DateTimeField()
    update_time = models.DateTimeField()
    close_time = models.DateTimeField()
    first_reply_time = models.DateTimeField()
    user_login = models.CharField(max_length=50)
    user_id = models.CharField(max_length=50)


class Basic(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    repo_name = models.CharField(max_length=50)
    user = models.CharField(max_length=50)
    language_detail = models.CharField(max_length=1000)
    language = models.CharField(max_length=10)
    stars = models.IntegerField()
    forks = models.IntegerField()
    issues = models.IntegerField()
    topic = models.CharField(max_length=1000)
    description = models.CharField(max_length=500, default=None)
    open_pulls = models.IntegerField(null=True)
    close_pulls = models.IntegerField(null=True)
    commits = models.IntegerField(null=True)
    contributor = models.IntegerField(null=True)
    updated_at = models.DateTimeField(null=True)
    visible = models.BooleanField(default=True)

class Activity(models.Model):
    repo_name = models.CharField(max_length=50)
    user = models.CharField(max_length=50)
    week = models.CharField(max_length=20, primary_key=True)
    days = models.CharField(max_length=50)
    total = models.IntegerField()


class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    id = models.CharField(max_length=50, null=True)
    login = models.CharField(max_length=50, null=True)
    company = models.CharField(max_length=50, null=True)
    pulls = models.IntegerField(null=True)
    reviews = models.IntegerField(null=True)
    commit = models.IntegerField(null=True)
    issues = models.IntegerField(null=True)
    owner = models.CharField(max_length=50, null=True)
    repo = models.CharField(max_length=50, null=True)


class Commit(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    created_at = models.DateTimeField()
    reply_at = models.DateTimeField()
    message = models.CharField(max_length=1024)
    repo_name = models.CharField(max_length=50)
    user = models.CharField(max_length=50)


class Pulls(models.Model):
    repo_name = models.CharField(max_length=50)
    user = models.CharField(max_length=50)
    created_at = models.DateTimeField(null=True, default=None)
    updated_at = models.DateTimeField(null=True, default=None)
    merged_at = models.DateTimeField(null=True, default=None)
    closed_at = models.DateTimeField(null=True, default=None)
    number = models.IntegerField()
    id = models.CharField(max_length=20, primary_key=True)
    locked = models.BooleanField(default=False)
    state = models.CharField(max_length=10)
    title = models.CharField(max_length=300)


class Stars(models.Model):
    starred_at = models.DateTimeField()
    repo_name = models.CharField(max_length=50)
    user = models.CharField(max_length=50)
    login = models.CharField(max_length=50)

    class Meta:
        unique_together = ("user", "repo_name", "login")


class Company(models.Model):
    repo_name = models.CharField(max_length=50)
    user = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    counts = models.IntegerField()
    type = models.CharField(max_length=10)