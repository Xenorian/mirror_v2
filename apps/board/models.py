from django.db import models
import django
from django.contrib.auth.models import User


# # Create your models here.
class Project(models.Model):
    users_participated = models.ManyToManyField(to=User, related_name='usersParticipated')

    project_id = models.CharField(max_length=50, null=True)
    # repository full name
    full_name = models.CharField(max_length=50, null=True)
    # repository description
    Description = models.CharField(max_length=100, null=True)
    # the date of when the repo was created
    Date_created = models.DateTimeField(default=django.utils.timezone.now, null=True)
    # the date of the last git push
    Date_of_lastpush = models.DateTimeField(default=django.utils.timezone.now, null=True)
    # programming language
    Language = models.CharField(max_length=50, null=True)
    # number of forks
    Number_of_forks = models.IntegerField(null=True)
    # number of stars
    Number_of_stars = models.IntegerField(null=True)
    # home page
    Home_page = models.CharField(max_length=50, null=True)
    # html url
    Html_url = models.URLField(null=True)
    # 项目名称
    project_name = models.CharField(max_length=50, null=True)

    class Meta:
        verbose_name_plural = '项目'

    def __str__(self):
        return self.full_name


class Commit(models.Model):
    author_name = models.CharField(max_length=100, null=True)
    author_email = models.EmailField(null=True)
    author_date = models.DateTimeField(default=django.utils.timezone.now, null=True)

    commiter_name = models.CharField(max_length=100, null=True)
    commiter_email = models.EmailField(null=True)
    commiter_date = models.DateTimeField(default=django.utils.timezone.now, null=True)

    sha = models.CharField(max_length=200, primary_key=True)
    message = models.CharField(max_length=100, null=True)
    comment_count = models.IntegerField(null=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, null=True)


# # Create your models here.
class Contributor(models.Model):
    contributor_id = models.CharField(max_length=50, null=False, primary_key=True)
    login = models.CharField(max_length=50, null=True)
    project = models.CharField(max_length=50, null=True)
