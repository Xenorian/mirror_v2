import json
import os.path
import shutil
from ast import literal_eval
from datetime import datetime, time
from urllib.request import urlopen
import date_converter
from django.contrib.sites import requests
from django.utils.timezone import get_current_timezone

tz = get_current_timezone()
import pymysql
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from back.settings import DB_name, DB_password, BASE_DIR
from apps import models
from django.contrib.auth.hashers import make_password, check_password
from apps.github_spider.Requester.ReposRequester import ReposRequester
from apps.github_spider.Requester.BaseRequester import BaseRequester
from apps.github_spider.Requester.UserRequester import UserRequester
import easy_date


@csrf_exempt
def findContributor(request):
    try:
        user = request.GET.get("user")
        repo = request.GET.get("repo")
        r = ReposRequester()
        res = r.get_contributor(user, repo)
        for i in range(len(res)):
            new_contributor = models.Contributor.objects.create(contributor_id=res[i].get('id'),
                                                                company=res[i].get('company'),
                                                                login=res[i].get('login'),
                                                                contributions=res[i].get('contributions'),
                                                                project=repo)
            new_contributor.save()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()


def delete(request):
    repo = request.GET.get("repo")
    owner = request.GET.get("owner")
    try:
        models.Basic.objects.filter(repo_name=repo, user=owner).update(
            visible=False
        )
        return HttpResponse()
    except Exception as e:
        print(e)
        return HttpResponseNotFound()
@csrf_exempt
def basic(request):
    try:
        user = request.GET.get("user")
        repo = request.GET.get("repo")
        r = ReposRequester()
        res = r.get_repo_basic(user, repo)
        if res is True:
            return HttpResponse()
        else:
            return HttpResponseNotFound()
    except:
        return HttpResponseBadRequest()


def add_new_repo(request):
    repo = request.GET.get("repo")
    owner = request.GET.get("owner")
    r = ReposRequester()
    try:
        r.get_repo_basic(owner, repo)
        print("finish basic")
        r.get_pull_detail(owner, repo)
        print("finish detail")
        r.get_issues(owner, repo)
        print("finish issues")
        r.get_commit(owner, repo)
        print("finish commit")
        r.get_activity(owner, repo)
        print("finish activity")
        #r.get_contributor(owner, repo)
        #print("finish contributor")
        r.get_companys(owner,repo)
        print("finish companys")
        r.set_up_company(owner, repo, "pulls")
        print("finish pulls")
        r.set_up_company(owner, repo, "reviews")
        print("finish reviews")
        r.set_up_company(owner, repo, "commit")
        print("finish commit")
        r.set_up_company(owner, repo, "issues")
        print("finish issues")
        r.update(owner, repo)
        return HttpResponse()
    except Exception as e:
        print(e)
        return HttpResponseNotFound(e)


def get_basic(request):
    try:
        user = request.GET.get("user")
        repo = request.GET.get("repo")
        basic = models.Basic.objects.filter(user=user, repo_name=repo)
        for i in basic:
            res_dict = dict()
            res_dict["language"] = i.language
            temp = literal_eval(i.language_detail)
            idx = list(temp)
            language_list = list()
            for j in idx:
                temp_dict = dict()
                temp_dict["value"] = temp[j]
                temp_dict["name"] = j
                language_list.append(temp_dict)
            res_dict["language_detail"] = language_list
            res_dict["stars"] = i.stars
            res_dict["commits"] = i.commits
            res_dict["issues"] = i.issues
            res_dict["forks"] = i.forks
            res_dict["open_pulls"] = int(i.open_pulls)
            res_dict["topic"] = literal_eval(i.topic)
            res_dict["contributor"] = i.contributor
            res_dict["close_pulls"] = int(i.close_pulls)
            res_dict["pulls"] = int(i.close_pulls) + int(i.open_pulls)
            res_dict["description"] = i.description
            res_dict["owner"] = user
            res_dict["repo"] = repo
            res_dict["update"] = str(i.updated_at)[:19]
            return JsonResponse(json.dumps(res_dict), safe=False)
        return HttpResponseNotFound()
    except:
        return HttpResponseBadRequest()


def pulls(request):
    repo = request.GET.get("repo")
    owner = request.GET.get("owner")
    r = ReposRequester()
    try:
        r.get_pull_detail(owner, repo)
        return HttpResponse()
    except Exception as e:
        return HttpResponse(e)
    # path = BASE_DIR + '/res/' + owner + "/" + repo
    # if not os.path.exists(path):
    #     os.mkdir(path)
    # path = path + "/pull.json"
    # with open(path) as json_file:
    #     res = json.loads(json_file.read())
    # res = list(res)
    # for j in range(len(res)):
    #     for k in range(len(res[j])):
    #         pull = res[j][k]
    #         old_pull = models.Pulls.objects.filter(id=pull["id"])
    #         if old_pull.exists():
    #             break
    #         created_at = date_converter.string_to_datetime(pull['created_at'], "%Y-%m-%dT%H:%M:%SZ")
    #         updated_at = None
    #         if pull['updated_at'] is not None:
    #             updated_at = date_converter.string_to_datetime(pull['updated_at'], "%Y-%m-%dT%H:%M:%SZ")
    #         closed_at = None
    #         if pull['closed_at'] is not None:
    #             closed_at = date_converter.string_to_datetime(pull['closed_at'], "%Y-%m-%dT%H:%M:%SZ")
    #         merged_at = None
    #         if pull['merged_at'] is not None:
    #             merged_at = date_converter.string_to_datetime(pull['merged_at'], "%Y-%m-%dT%H:%M:%SZ")
    #         user = pull["user"]
    #         t = int(pull['number'])
    #         try:
    #             new_pull = models.Pulls.objects.create(
    #                 id=pull["id"],
    #                 repo_name=repo,
    #                 user=owner,
    #                 number=t,
    #                 locked=pull["locked"],
    #                 state=pull["state"],
    #                 title=pull["title"],
    #                 created_at=created_at,
    #                 updated_at=updated_at,
    #                 closed_at=closed_at,
    #                 merged_at=merged_at,
    #             )
    #             new_pull.save()
    #         except Exception as e:
    #             print(e)
    #             continue
    #
    #         try:
    #             old_user = models.User.objects.filter(id=user["id"], owner=owner, repo=repo)
    #             if old_user.exists():
    #                 d = list(old_user.values())
    #                 t = d[0]["pulls"]+1
    #                 models.User.objects.filter(id=d[0]["id"]).update(
    #                     pulls=t
    #                 )
    #             else:
    #                 new_user = models.User.objects.create(
    #                     pulls=1, reviews=0, commit=0, issues=0,
    #                     login=user["login"],
    #                     id=user["id"],
    #                     owner=owner,
    #                     repo=repo
    #                 )
    #                 new_user.save()
    #             requested_reviewers = pull["requested_reviewers"]
    #             if requested_reviewers is None:
    #                 continue
    #             for i in range(len(requested_reviewers)):
    #                 old_user = models.User.objects.filter(id=requested_reviewers[i]["id"], owner=owner, repo=repo)
    #                 if old_user.exists():
    #                     d = list(old_user.values())
    #                     t = d[0]["reviews"] + 1
    #                     models.User.objects.filter(id=d[0]["id"]).update(
    #                         reviews=t
    #                     )
    #                 else:
    #                     new_user = models.User.objects.create(
    #                         pulls=0, reviews=1, commit=0, issues=0,
    #                         login=requested_reviewers[i]["login"],
    #                         id=requested_reviewers[i]["id"],
    #                         owner = owner, repo = repo
    #                     )
    #                     new_user.save()
    #         except Exception as e:
    #             print(e)
    #             continue
    # return HttpResponse()


def commits(request):
    repo = request.GET.get("repo")
    owner = request.GET.get("owner")
    r = ReposRequester()
    try:
        res = r.get_commit(owner, repo)
        return HttpResponse()
    except Exception as e:
        return HttpResponse(e)
    # path = BASE_DIR + '/res/' + owner + "/" + repo
    # if not os.path.exists(path):
    #     os.mkdir(path)
    # path = path + "/pull.json"
    # with open(path) as json_file:
    #     res = json.loads(json_file.read())
    # res = list(res)
    # for j in range(len(res)):
    #     for k in range(len(res[j])):
    #         commit = res[j][k]
    #         user = commit["author"]
    #         old_commit = models.Commit.objects.filter(id=commit["sha"])
    #         if old_commit.exists():
    #             break
    #         created_at = date_converter.string_to_datetime(commit['commit']["author"]["date"], "%Y-%m-%dT%H:%M:%SZ")
    #         reply_at = None
    #         if commit['commit']["committer"] is not None:
    #             reply_at = date_converter.string_to_datetime(commit['commit']["committer"]["date"], "%Y-%m-%dT%H:%M:%SZ")
    #
    #         try:
    #             new_commit = models.Commit.objects.create(
    #                 id=commit["sha"],
    #                 repo_name=repo,
    #                 user=owner,
    #                 created_at=created_at,
    #                 reply_at=reply_at,
    #                 message=commit["commit"]["message"]
    #             )
    #             new_commit.save()
    #         except Exception as e:
    #             print(e)
    #             continue
    #         try:
    #             old_user = models.User.objects.filter(id=commit["author"]["id"], owner=owner, repo=repo)
    #             if old_user.exists():
    #                 d = list(old_user.values())
    #                 t = d[0]["commit"] + 1
    #                 models.User.objects.filter(id=d[0]["id"]).update(
    #                     commit=t
    #                 )
    #             else:
    #                 new_user = models.User.objects.create(
    #                     pulls=0, reviews=0, commit=1, issues=0,
    #                     login=user["login"],
    #                     id=user["id"], owner=owner, repo=repo
    #                 )
    #                 new_user.save()
    #         except Exception as e:
    #             print(e)
    #             continue
    # return HttpResponse()


def get_user(request):
    repo = request.GET.get("repo")
    owner = request.GET.get("owner")
    res = models.User.objects.filter(repo=repo, owner=owner).values()
    res = list(res)
    res_list = list()
    for i in range(len(res)):
        temp_dict = dict()
        temp_dict["id"] = res[i]["id"]
        temp_dict["login"] = res[i]["login"]
        temp_dict["company"] = res[i]["company"]
        temp_dict["pulls"] = res[i]["pulls"]
        temp_dict["reviews"] = res[i]["reviews"]
        temp_dict["commit"] = res[i]["commit"]
        temp_dict["issues"] = res[i]["issues"]
        res_list.append(temp_dict)
    return JsonResponse(json.dumps({"result": res_list}), safe=False)


def get_commit_activity(request):
    try:
        repo = request.GET.get("repo")
        res = models.Activity.objects.filter(repo_name=repo).values()
        res = list(res)
        res_list = list()
        arr = ["Commit", "Country", "Year"]
        res_list.append(arr)
        for i in range(len(res)):
            temp_dict = dict()
            temp_dict["total"] = res[i]["total"]
            week = res[i]["week"]
            time_str = datetime.fromtimestamp(int(week)).strftime("%Y-%m-%d %H:%M:%S")
            temp_dict["week"] = time_str
            temp_dict["days"] = res[i]["days"]
            temp_list = list()
            temp_list.append(temp_dict["total"])
            temp_list.append(repo)
            temp_list.append(time_str)
            res_list.append(temp_list)
        return JsonResponse(json.dumps({"result": res_list}), safe=False)
    except:
        return HttpResponseNotFound()


def findActivity(request):
    try:
        owner = request.GET.get("owner")
        repo = request.GET.get("repo")
        r = ReposRequester()
        res = r.get_activity(owner, repo)
        if res is True:
            return HttpResponse()
        else:
            return HttpResponseNotFound()
    except:
        return HttpResponseBadRequest()


def get_all(request):
    basic = models.Basic.objects.filter()
    res = list()
    for i in basic:
        if i.visible == 0:
            continue
        res_dict = dict()
        res_dict["language"] = i.language
        temp = literal_eval(i.language_detail)
        idx = list(temp)
        language_list = list()
        for j in idx:
            temp_dict = dict()
            temp_dict["value"] = temp[j]
            temp_dict["name"] = j
            language_list.append(temp_dict)
        res_dict["language_detail"] = language_list
        res_dict["stars"] = i.stars
        res_dict["issues"] = i.issues
        res_dict["forks"] = i.forks
        res_dict["open_pulls"] = int(i.open_pulls)
        res_dict["topic"] = literal_eval(i.topic)
        res_dict["contributor"] = i.contributor
        res_dict["close_pulls"] = int(i.close_pulls)
        res_dict["pulls"] = int(i.close_pulls) + int(i.open_pulls)
        res_dict["description"] = i.description
        res_dict["owner"] = i.user
        res_dict["repo"] = i.repo_name
        res_dict["update"] = str(i.updated_at)
        res.append(res_dict)
    return JsonResponse(json.dumps(res), safe=False)


def get_creator2(request):
    try:
        owner = request.GET.get("owner")
        repo = request.GET.get("repo")
        type = request.GET.get("type")
        if type == "issues":
            res = models.User.objects.filter(owner=owner, repo=repo, issues__gt=0).values("company").distinct()
        elif type == "pulls":
            res = models.User.objects.filter(owner=owner, repo=repo, pulls__gt=0).values("company").distinct()
        elif type == "commit":
            res = models.User.objects.filter(owner=owner, repo=repo, commit__gt=0).values("company").distinct()
        elif type == "reviews":
            res = models.User.objects.filter(owner=owner, repo=repo, reviews__gt=0).values("company").distinct()
        else:
            return HttpResponseNotFound()
        res_list = list()
        for i in range(len(res)):
            if res[i]["company"] == None or res[i]["company"] == " ":
                continue
            temp_dict = dict()
            temp_dict["name"] = res[i]["company"]
            count = models.User.objects.filter(company=res[i]["company"], repo=repo, owner=owner).count()
            if count<4:
                continue
            temp_dict["value"] = count
            res_list.append(temp_dict)
        return JsonResponse(json.dumps({"result": res_list}), safe=False)
    except Exception as e:
        print(e)
        return HttpResponseNotFound()

def get_creator(request):
    try:
        owner = request.GET.get("owner")
        repo = request.GET.get("repo")
        type = request.GET.get("type")
        res = models.Company.objects.filter(user=owner, repo_name=repo,type=type).values("company", "counts")
        res_list = list()
        for i in range(len(res)):
            temp_dict = dict()
            temp_dict["name"] = res[i]["company"]
            if res[i]["counts"] < 4:
                continue
            temp_dict["value"] = res[i]["counts"]
            res_list.append(temp_dict)
        return JsonResponse(json.dumps({"result": res_list}), safe=False)
    except Exception as e:
        print(e)
        return HttpResponseNotFound()

@csrf_exempt
def findIssues(request):
    try:
        owner = request.GET.get("owner")
        repo = request.GET.get("repo")
        r = ReposRequester()
        res = r.get_issues(owner, repo)
        if res is None:
            return HttpResponseBadRequest()
        # res = []
        # path = BASE_DIR + '/res/' + repo + "/test.json"
        # with open(path) as json_file:
        #     res = json.loads(json_file.read())
        # create_time = date_converter.string_to_datetime(res[0]['create_time'], "%Y-%m-%dT%H:%M:%SZ")
        # for i in range(len(res)):
        #     issue = res[i]
        #     create_time = date_converter.string_to_datetime(issue['create_time'], "%Y-%m-%dT%H:%M:%SZ")
        #     update_time = None
        #     if issue['update_time'] is not None:
        #         update_time = date_converter.string_to_datetime(issue['update_time'], "%Y-%m-%dT%H:%M:%SZ")
        #     close_time = None
        #     if issue['close_time'] is not None:
        #         close_time = date_converter.string_to_datetime(issue['close_time'], "%Y-%m-%dT%H:%M:%SZ")
        #     first_reply_time = None
        #     if issue['first_reply_time'] is not None:
        #         first_reply_time = date_converter.string_to_datetime(issue['first_reply_time'], "%Y-%m-%dT%H:%M:%SZ")
        #
        #     new_issue = models.Issues.objects.create(
        #         issue_id=issue["id"],
        #         number=issue["number"],
        #         title=issue['title'],
        #         locked=issue['locked'],
        #         state=issue['state'],
        #         comments=issue['comments'],
        #         create_time=create_time,
        #         update_time=update_time,
        #         close_time=close_time,
        #         first_reply_time=first_reply_time,
        #         user_login=issue['user_login'],
        #         user_id=issue['user_id'],
        #         repo_name=repo
        #     )
        #     new_issue.save()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()


def get_day_count(request):
    owner = request.GET.get("owner")
    repo = request.GET.get("repo")
    type = request.GET.get("type")
    if type == "issues":
        created_at = models.Issues.objects.filter(repo_name=repo).order_by("created_at")
    elif type == "pulls":
        created_at = models.Pulls.objects.filter(repo_name=repo, user=owner).order_by("created_at")
    elif type == "commit":
        created_at = models.Commit.objects.filter(user=owner, repo_name=repo).order_by("created_at")
    else:
        return HttpResponseNotFound()
    created_at = list(created_at)
    temp = None
    count = 0
    res = list()
    arr = ["Commit", "Country", "Year"]
    res.append(arr)
    for i in created_at:
        if temp is None:
            temp = i.created_at.date()
            count = 1
            continue
        if temp == i.created_at.date():
            count = count + 1
            continue
        t = dict()

        t["value"] = count
        t["repo"] = repo
        t["create_at"] = str(temp)
        temp_list = list()
        temp_list.append(count)
        temp_list.append(repo)
        temp_list.append(t["create_at"])
        res.append(temp_list)
        #t["owner"] = owner
        temp = i.created_at.date()
        count = 1
        #res.append(t)
    t = dict()
    t["value"] = count
    t["repo"] = repo
    t["create_at"] = str(temp)
    #t["owner"] = owner
    temp_list = list()
    temp_list.append(count)
    temp_list.append(repo)
    temp_list.append(t["create_at"])
    res.append(temp_list)
    return JsonResponse(json.dumps(res), safe=False)
