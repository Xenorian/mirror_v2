from django.shortcuts import render
from .models import Project, Commit
from ..mirror_user.models import User, UserContact, UserProfile
import requests
from github import Github
import json
import random
from django.core.mail import send_mail

# UA代理
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}


def board_settings(request, username):
    user = User.objects.get(username=username)

    try:
        userProfile = user.profile
    except:
        userProfile = UserProfile(user=user)
        userProfile.save()

    if request.method == 'GET':
        return render(request, 'board/settings.html', {'user': user, 'username': username, 'newEmail': ''})
    else:
        if request.POST.get('verification') == '':
            userProfile.verification = random.randint(1000, 9999)
            userProfile.save()
            newEmail = request.POST.get('newEmail')
            send_mail(subject="来自MIRROR公司的邮件",
                      message="【MIRROR】您的验证码是{}，请勿将验证码泄露给他人，如非本人操作请忽略".format(userProfile.verification),
                      from_email="1793013266@qq.com", recipient_list=[newEmail, ], fail_silently=False)
            return render(request, 'board/settings.html',
                          {'msg_info': "验证码已发送", 'user': user, 'username': username, 'newEmail': newEmail})
        else:
            verification = request.POST.get('verification')
            newEmail = request.POST.get('newEmail')
            if verification == userProfile.verification:
                user.email = newEmail
                user.save()
                return render(request, 'board/settings.html',
                              {'msg_info': "重置邮箱成功", 'user': user, 'username': username, 'newEmail': ''})
            else:
                return render(request, 'board/settings.html',
                              {'msg_info': "验证码错误，请重新核实", 'user': user, 'username': username, 'newEmail': newEmail})


def board_contact(request, username):
    if request.method == 'GET':
        return render(request, 'board/contact.html', {'username': username})
    else:
        user = User.objects.get(username=username)
        theme = request.POST.get('theme')
        info = request.POST.get('info')
        realname = request.POST.get('realname')
        email = request.POST.get('email')
        userContact = UserContact(realname=realname, email=email, info=info, theme=theme, user=user)
        userContact.save()
        return render(request, 'board/contact.html', {'msg_info': "成功提交", 'username': username})


def board_docs(request, username):
    return render(request, 'board/docs.html', {'username': username})


def board_addproject(request, username):
    # 用户增加项目
    if request.method == 'GET':
        return render(request, 'board/addproject.html', {'username': username})
    else:
        full_name = request.POST.get('project_name')
        Description = request.POST.get('project_description')
        project_name = request.POST.get('project_nickname')

        try:
            pro = Project.objects.get(full_name=full_name)
            users = pro.users_participated.filter(username=username)
            if len(users) > 0:
                return render(request, 'board/addproject.html', {'msg_info': "项目已加入", 'username': username})
            else:
                user = User.objects.get(username=username)
                pro.users_participated.add(user)
                return render(request, 'board/addproject.html', {'msg_info': "加入项目成功", 'username': username})
        except:
            project = get_info_from_github(username, full_name, Description, project_name)
            project.save()
            return render(request, 'board/addproject.html', {'msg_info': "项目创建成功", 'username': username})


def board_projects(request, username):
    user = User.objects.get(username=username)
    # 获取项目信息
    projects = user.usersParticipated.all()
    return render(request, 'board/projects.html', {'projects': projects, 'username': username})


def board_delete(request, username, project_name):
    project = Project.objects.get(project_name=project_name)
    user = User.objects.get(username=username)
    project.users_participated.remove(user)
    projects = user.usersParticipated.all()
    return render(request, 'board/projects.html', {'projects': projects, 'username': username})


def board_mainboard(request, username, project_name):
    project = Project.objects.get(project_name=project_name)
    return render(request, 'board/mainboard.html', {'project': project, 'username': username})


def board_calendar(request, username):
    return render(request, 'board/calendar.html', {'username': username})


def board_chart1(request, username, project_name):
    project = Project.objects.get(project_name=project_name)
    return render(request, 'board/chart1.html', {'project': project, 'username': username})


def board_chart2(request, username, project_name):
    project = Project.objects.get(project_name=project_name)
    return render(request, 'board/chart2.html', {'project': project, 'username': username})


def board_chart3(request, username, project_name):
    project = Project.objects.get(project_name=project_name)
    return render(request, 'board/chart3.html', {'project': project, 'username': username})


def board_table1(request, username, project_name):
    project = Project.objects.get(project_name=project_name)
    return render(request, 'board/table1.html', {'project': project, 'username': username})


def board_table2(request, username, project_name):
    project = Project.objects.get(project_name=project_name)
    return render(request, 'board/table2.html', {'project': project, 'username': username})


def get_info_from_github(username, full_name, Description, project_name):
    user = User.objects.get(username=username)
    # pygithub object
    g = Github()
    repo = g.get_repo(full_name)
    project_id = repo.id
    full_name = repo.full_name
    Description = repo.description
    Date_created = repo.created_at
    Date_of_lastpush = repo.pushed_at
    Language = repo.language
    Home_page = repo.homepage
    Number_of_forks = repo.forks
    # number of stars
    Number_of_stars = repo.stargazers_count
    Html_url = repo.html_url
    url = repo.commits_url.replace('{/sha}', '')
    rep = requests.get(url=url, headers=headers)
    results = json.loads(rep.text)
    project = Project(project_id=project_id, full_name=full_name, Description=Description, Date_created=Date_created,
                      Date_of_lastpush=Date_of_lastpush, Language=Language,
                      Home_page=Home_page, Number_of_forks=Number_of_forks, Number_of_stars=Number_of_stars,
                      Html_url=Html_url, project_name=project_name)
    project.save()
    project.users_participated.add(user)
    project.save()

    for result in results:
        sha = result.get('sha')
        author_name = result.get('author').get('name')
        author_email = result.get('author').get('email')
        author_date = result.get('author').get('date')
        message = result.get('message')
        comment_count = result.get('comment_count')
        if result.get('commiter') is None:
            commit = Commit(sha=sha, author_name=author_name, author_email=author_email, author_date=author_date,
                            message=message, comment_count=comment_count, project=project)

        else:
            commiter_name = result.get('commiter').get('name')
            commiter_email = result.get('commiter').get('email')
            commiter_date = result.get('commiter').get('date')
            commit = Commit(sha=sha, author_name=author_name, author_email=author_email, author_date=author_date,
                            commiter_name=commiter_name,
                            commiter_email=commiter_email, commiter_date=commiter_date, message=message,
                            comment_count=comment_count, project=project)

        commit.save()

    return project
