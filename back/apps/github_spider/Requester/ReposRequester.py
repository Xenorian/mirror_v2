import json
import os
# import cookielib
# import urllib2
from bs4 import BeautifulSoup
import re
import date_converter
import django
import pymysql
from urllib.request import urlopen
from back.settings import BASE_DIR

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "back.settings")
django.setup()
from apps import models
from apps.github_spider.Requester.BaseRequester import BaseRequester
from apps.github_spider.Parser.Parser import Parser
from apps.github_spider.util.util import Util
from apps.github_spider.threadpool.ThreadPool import ThreadPool
from apps.github_spider.Entity.RepoEntity import RepoEntity
from apps.github_spider.Requester.UserRequester import UserRequester
from apps.models import Contributor, Issues
from datetime import datetime
import requests
import parsel
import time

# import http.client
# http.client.HTTPConnection._http_vsn = 10
# http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'
util = Util()
thread = ThreadPool(util.get_thread_num())
repo_entity = RepoEntity()
user_requester = UserRequester()


class ReposRequester(BaseRequester):
    def __init__(self):
        BaseRequester.__init__(self)
        self.result_path = os.path.dirname(os.getcwd()) + os.sep + "result" + os.sep

    def get_repo_detail(self, username: str, repo_name: str):
        url = f"https://api.github.com/repos/{username}/{repo_name}/"
        self._test()
        json_result = requests.get(url, headers=self._random_header()).json()
        repos_dict = Parser.parser_repos(json_result)
        return repos_dict

    def __get_single_contributor(self, username, repo_name, commit_list: list, count_list: list):
        try:
            commit_dict = {}
            commit_url = f"https://github.com/{username}/{repo_name}/contributor"
            response_text = requests.get(commit_url, headers=self._random_header()).text
            change_num_list = Parser.parser_user(response_text)
            print(change_num_list)
        except:
            commit_dict = None
        commit_list.append(commit_dict)
        count_list.append(commit_dict)

    def get_contributor(self, username: str, repo_name: str, is_save=False):
        i = 0
        contributor_list = list()
        while 1:
            url = f"https://api.github.com/repos/{username}/{repo_name}/contributors?page={i + 1}&per_page={100}"
            self._test()
            json_result = requests.get(url=url, headers=self._random_header()).json()
            if len(json_result) == 0:
                break
            contributor_dict = Parser.parser_user(json_result, single=False)
            for j in range(len(contributor_dict)):
                url2 = f"https://api.github.com/users/{contributor_dict[j].get('login')}"
                compInfo = requests.get(url=url2, headers=self._random_header()).json()
                contributor_dict[j]["company"] = compInfo.get('company')
                contributor_list.append(contributor_dict[j])
            i = i + 1
        return contributor_list

    def test(self):
        try:
            new_issue = Issues.objects.create(
                issue_id="1",
                number="1",
                title="1",
                locked=True,
                state="1",
                comments=1,
                # create_time=create_time,
                # update_time=update_time,
                # close_time=close_time,
                # first_reply_time=first_reply_time,
                user_login="1",
                user_id="1",
                repo_name="1"
            )
            new_issue.save()
            return
        except:
            return

    def get_first_commit(self, owner, repo):
        url = f"https://api.github.com/repos/{owner}/{repo}/commits"
        req = requests.get(url=url, headers=self._random_header())
        json_data = req.json()

        if req.headers.get('Link'):
            page_url = req.headers.get('Link').split(',')[1].split(';')[0].split('<')[1].split('>')[0]
            req_last_commit = requests.get(page_url)
            first_commit = req_last_commit.json()
            first_commit_hash = first_commit[-1]['sha']
        else:
            first_commit_hash = json_data[-1]['sha']
        return first_commit_hash

    def get_all_commits_count(self, owner, repo):
        # sha_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
        # res = requests.get(url=sha_url, headers=self._random_header())
        # sha = (res.json())[0]["sha"]
        sha = "8fd31ac4dade93a10822ba32c1f2293827b2b2f3"
        first_commit = self.get_first_commit(owner, repo)
        compare_url = f'https://api.github.com/repos/{owner}/{repo}/compare/{first_commit}...{sha}'
        commit_req = requests.get(url=compare_url, headers=self._random_header())
        commit_count = commit_req.json()['total_commits'] + 1
        print(commit_count)
        return commit_count

    def get_repo_basic(self, owner, repo):
        try:
            url = f"https://api.github.com/repos/{owner}/{repo}"
            json_result = requests.get(url=url, headers=self._random_header()).json()
            lang_url = f"https://api.github.com/repos/{owner}/{repo}/languages"
            lan_res = requests.get(url=lang_url, headers=self._random_header()).json()
            language_detail = json.dumps(lan_res)
            commits = self.commit_page(owner, repo)
            contributor = self.contributor_page(owner, repo)
            old_repo = models.Basic.objects.filter(user=owner, repo_name=repo)
            pull = self.pull_page(owner, repo)
            if old_repo.exists():
                old_repo.update(
                    id=json_result["id"],
                    language=json_result["language"],
                    language_detail=language_detail,
                    stars=json_result["stargazers_count"],
                    forks=json_result["forks"],
                    issues=json_result["open_issues"],
                    topic=json_result["topics"],
                    description=json_result["description"],
                    contributor=contributor,
                    commits=commits,
                    open_pulls=pull[0],
                    close_pulls=pull[1],
                    visible=True
                )
                return True
            new_repo = models.Basic.objects.create(
                id=json_result["id"],
                repo_name=repo, user=owner,
                language=json_result["language"],
                language_detail=language_detail,
                stars=json_result["stargazers_count"],
                forks=json_result["forks"],
                issues=json_result["open_issues"],
                topic=json_result["topics"],
                description=json_result["description"],
                contributor=contributor,
                commits=commits,
                open_pulls=pull[0],
                close_pulls=pull[1],
                visible=True
            )
            new_repo.save()
            return True
        except:
            return False

    def get_issues(self, owner, repo):
        i = 1
        issue_list = list()
        # url = f"https://api.github.com/repos/{owner}/{repo}/issues?page={i}&per_page={10}"
        # text_result = requests.get(url=url, headers=self._random_header()).json()
        # print(text_result)
        # print(text_result)
        res = list()
        # print(requests.get(
        #     f"https://api.github.com/rate_limit").json())
        path = BASE_DIR + '/res/' + owner + "/" + repo  # + "/issue.json"
        if not os.path.exists(path):
            os.mkdir(path)
        path = path + "/issue.json"
        open(path, 'w')
        # open(path2, 'w')

        # read exists file
        # with open(path2, 'r') as f:
        #     lines = f.readlines()
        #     for line in lines:
        #         t = json.loads(line)
        #         t_l = list()
        #         for i in range(len(t)):
        #             t_l.append(dict(t[i]))
        #         issue_list.append(t_l)
        # i = len(issue_list)

        while 1:
            url = f"https://api.github.com/repos/{owner}/{repo}/issues?page={i}&per_page={100}"
            json_result = requests.get(url=url, headers=self._random_header()).json()
            if len(json_result) == 0:
                break
            issue_list.append(json_result)
            print(i)
            i = i + 1
            with open(path, 'w+') as f:
                f.write(json.dumps(json_result))
                f.write("\n")
        count = 0
        if len(res) ==0:
            return
        try:
            for j in range(i):
                for k in range(len(issue_list[j])):
                    try:
                        first_reply_time = None
                        issue = issue_list[j][k]
                        issue_number = issue['number']
                        if count > 0:
                            response = requests.get(
                                f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments").json()
                            if len(response) != 0:
                                first_reply_time = date_converter.string_to_datetime(response[0]["created_at"],
                                                                                     "%Y-%m-%dT%H:%M:%SZ")
                            count = count - 1

                        create_time = date_converter.string_to_datetime(issue['created_at'], "%Y-%m-%dT%H:%M:%SZ")
                        update_time = None
                        if issue['updated_at'] is not None:
                            update_time = date_converter.string_to_datetime(issue['updated_at'], "%Y-%m-%dT%H:%M:%SZ")
                        close_time = None
                        if issue['closed_at'] is not None:
                            close_time = date_converter.string_to_datetime(issue['closed_at'], "%Y-%m-%dT%H:%M:%SZ")
                        str_num = str(issue_number)
                        # first_reply_time = None
                        # if issue['first_reply_time'] is not None:
                        #     first_reply_time = date_converter.string_to_datetime(issue['first_reply_time'],
                        #                                                          "%Y-%m-%dT%H:%M:%SZ")
                        old_issue = Issues.objects.filter(issue_id=issue["id"])
                        if old_issue.exists():
                            old_issue.update(
                                number=str_num,
                                title=issue['title'],
                                locked=issue['locked'],
                                state=issue['state'],
                                comments=issue['comments'],
                                created_at=create_time,
                                update_time=update_time,
                                close_time=close_time,
                                first_reply_time=first_reply_time,
                                user_login=issue['user']['login'],
                                user_id=issue['user']['id'],
                                repo_name=repo
                            )
                            continue
                        else:
                            new_issue = Issues.objects.create(
                                issue_id=issue["id"],
                                number=str_num,
                                title=issue['title'],
                                locked=issue['locked'],
                                state=issue['state'],
                                comments=issue['comments'],
                                created_at=create_time,
                                update_time=update_time,
                                close_time=close_time,
                                first_reply_time=first_reply_time,
                                user_login=issue['user']['login'],
                                user_id=issue['user']['id'],
                                repo_name=repo
                            )
                            new_issue.save()
                            temp = dict()
                            temp["id"] = issue['id'],
                            temp["number"] = issue_number,
                            temp["title"] = issue['title'],
                            temp["locked"] = issue["locked"],
                            temp["state"] = issue['state'],
                            temp["comments"] = issue['comments'],
                            # create_time=datetime.strptime(issue.json['created_at'], "%Y-%m-%dT%H:%M:%SZ"),
                            # update_time=datetime.strptime(issue.json['updated_at'], "%Y-%m-%dT%H:%M:%SZ"),
                            # close_time=datetime.strptime(issue.json['closed_at'], "%Y-%m-%dT%H:%M:%SZ"),
                            temp["created_at"] = issue['created_at'],
                            temp["update_time"] = issue['updated_at'],
                            temp["close_time"] = issue['closed_at'],
                            temp["first_reply_time"] = first_reply_time,
                            temp["user_login"] = issue['user']['login'],
                            temp["user_id"] = issue['user']['id'],
                            temp["repo_name"] = repo
                    except:
                        # continue
                        return None
        except Exception as e:
            print(e)
        self.move(owner, repo)
        return res

    def get_activity(self, owner, repo):
        try:
            url = f"https://api.github.com/repos/{owner}/{repo}/stats/commit_activity"
            res = requests.get(url=url, headers=self._random_header()).json()
            for i in range(len(res)):
                json_result = res[i]
                str_d = str(json_result["days"])
                str_w = str(json_result["week"])
                new_activity = models.Activity.objects.create(
                    repo_name=repo, user=owner, week=str_w,
                    total=json_result["total"],
                    days=str_d,
                )
                new_activity.save()
            self.update(owner, repo)
            return True
        except:
            return False

    def get_test(self):
        url = f"https://api.github.com/rate_limit"
        print(requests.get(url=url, headers=self._random_header()).json())

    def get_pull_detail(self, owner, repo):
        i = 1
        res = list()
        path = BASE_DIR + '/res/' + owner
        if not os.path.exists(path):
            os.mkdir(path)
        path = BASE_DIR + '/res/' + owner + "/" + repo
        if not os.path.exists(path):
            os.mkdir(path)
        path = path + "/pull.json"
        flag = 0
        if os.path.exists(path):
            flag = 1
        # latest = None
        # if flag:
        #     with open(path) as json_file:
        #         file = json.loads(json_file.read())
        #         file = list(file)
        #         latest = file[0]["id"]

        while 1:
            print(i)
            url = f"https://api.github.com/repos/{owner}/{repo}/pulls?page={i}&per_page=100&state=all"
            json_result = requests.get(url=url, headers=self._random_header()).json()
            if len(json_result) == 0:
                break
            # flag2 = 0
            # if flag:
            #     t = list(json_result)
            #     for j in range(json_result):
            #         if j["id"] == latest:
            #             flag2 = 1
            #             break
            # if flag2:
            #     break
            res.append(json_result)
            i = i + 1
            with open(path, 'w+') as f:
                f.write(json.dumps(json_result))
                f.write("\n")

        # f.close()
        # path = BASE_DIR + '/res/' + owner + "/" + repo
        # if not os.path.exists(path):
        #     os.mkdir(path)
        # path = path + "/pull.json"
        # with open(path) as json_file:
        #     res = json.loads(json_file.read())
        # res = list(res)
        if len(res) == 0:
            return
        try:
            for j in range(len(res)):
                for k in range(len(res[j])):
                    pull = res[j][k]
                    old_pull = models.Pulls.objects.filter(id=pull["id"])

                    created_at = date_converter.string_to_datetime(pull['created_at'], "%Y-%m-%dT%H:%M:%SZ")
                    updated_at = None
                    if pull['updated_at'] is not None:
                        updated_at = date_converter.string_to_datetime(pull['updated_at'], "%Y-%m-%dT%H:%M:%SZ")
                    closed_at = None
                    if pull['closed_at'] is not None:
                        closed_at = date_converter.string_to_datetime(pull['closed_at'], "%Y-%m-%dT%H:%M:%SZ")
                    merged_at = None
                    if pull['merged_at'] is not None:
                        merged_at = date_converter.string_to_datetime(pull['merged_at'], "%Y-%m-%dT%H:%M:%SZ")
                    user = pull["user"]
                    t = int(pull['number'])
                    try:
                        if old_pull.exists():
                            models.Pulls.objects.filter(id=pull["id"]).update(
                                number=t,
                                locked=pull["locked"],
                                state=pull["state"],
                                title=pull["title"],
                                created_at=created_at,
                                updated_at=updated_at,
                                closed_at=closed_at,
                                merged_at=merged_at,
                            )
                            continue
                        else:
                            new_pull = models.Pulls.objects.create(
                                id=pull["id"],
                                repo_name=repo,
                                user=owner,
                                number=t,
                                locked=pull["locked"],
                                state=pull["state"],
                                title=pull["title"],
                                created_at=created_at,
                                updated_at=updated_at,
                                closed_at=closed_at,
                                merged_at=merged_at,
                            )
                            new_pull.save()
                    except Exception as e:
                        print(e)
                        continue

                    try:
                        old_user = models.User.objects.filter(id=user["id"], owner=owner, repo=repo)
                        if old_user.exists():
                            d = list(old_user.values())
                            t = d[0]["pulls"] + 1
                            models.User.objects.filter(id=d[0]["id"]).update(
                                pulls=t
                            )
                        else:
                            counts = models.User.objects.values("user_id")
                            counts = list(counts)
                            new_user = models.User.objects.create(
                                pulls=1, reviews=0, commit=0, issues=0,
                                login=user["login"],
                                id=user["id"],
                                owner=owner,
                                repo=repo,
                                user_id=len(counts) + 119540768
                            )
                            new_user.save()
                        requested_reviewers = pull["requested_reviewers"]
                        if requested_reviewers is None:
                            continue
                        for i in range(len(requested_reviewers)):
                            old_user = models.User.objects.filter(id=requested_reviewers[i]["id"], owner=owner, repo=repo)
                            if old_user.exists():
                                d = list(old_user.values())
                                t = d[0]["reviews"] + 1
                                models.User.objects.filter(id=d[0]["id"]).update(
                                    reviews=t
                                )
                            else:
                                counts = models.User.objects.values("user_id")
                                counts = list(counts)
                                new_user = models.User.objects.create(
                                    pulls=0, reviews=1, commit=0, issues=0,
                                    login=requested_reviewers[i]["login"],
                                    id=requested_reviewers[i]["id"],
                                    owner=owner, repo=repo, user_id=len(counts) + 119540768

                                )
                                new_user.save()
                    except Exception as e:
                        print(e)
                        continue
        except Exception as e:
            print(e)
        self.update(owner, repo)
        return res

    def get_commit(self, owner, repo):
        i = 1
        res = list()
        flag = 0
        path = BASE_DIR + '/res/' + owner + "/" + repo
        if not os.path.exists(path):
            os.mkdir(path)
        path = path + "/pull.json"
        latest = None
        if flag:
            with open(path) as json_file:
                file = json.loads(json_file.read())
                file = list(file)
                latest = file[0]["id"]

        # if not os.path.exists(path):
        #     os.mkdir(path)
        while 1:
            print(i)
            url = f"https://api.github.com/repos/{owner}/{repo}/commits?page={i}&per_page=100"
            json_result = requests.get(url=url, headers=self._random_header()).json()
            if len(json_result) == 0:
                break
            res.append(json_result)
            i = i + 1
            with open(path, 'a+') as f:
                f.write(json.dumps(json_result))
                f.write("\n")
        if len(res) == 0:
            return
        for j in range(len(res)):
            for k in range(len(res[j])):
                commit = res[j][k]
                user = commit["author"]
                old_commit = models.Commit.objects.filter(id=commit["sha"])
                created_at = date_converter.string_to_datetime(commit['commit']["author"]["date"], "%Y-%m-%dT%H:%M:%SZ")
                reply_at = None
                if commit['commit']["committer"] is not None:
                    reply_at = date_converter.string_to_datetime(commit['commit']["committer"]["date"],
                                                                 "%Y-%m-%dT%H:%M:%SZ")
                try:
                    if old_commit.exists():
                        models.Commit.objects.filter(id=commit["sha"]).update(
                            repo_name=repo,
                            user=owner,
                            created_at=created_at,
                            reply_at=reply_at,
                            message=commit["commit"]["message"]
                        )
                        continue
                    else:
                        new_commit = models.Commit.objects.create(
                            id=commit["sha"],
                            repo_name=repo,
                            user=owner,
                            created_at=created_at,
                            reply_at=reply_at,
                            message=commit["commit"]["message"]
                        )
                        new_commit.save()
                except Exception as e:
                    print(e)
                    continue
                try:
                    old_user = models.User.objects.filter(id=commit["author"]["id"], owner=owner, repo=repo)
                    if old_user.exists():
                        d = list(old_user.values())
                        t = d[0]["commit"] + 1
                        models.User.objects.filter(id=d[0]["id"]).update(
                            commit=t
                        )
                    else:
                        counts = models.User.objects.values("user_id")
                        counts = list(counts)
                        new_user = models.User.objects.create(
                            pulls=0, reviews=0, commit=1, issues=0,
                            login=user["login"],
                            id=user["id"], owner=owner, repo=repo,
                            user_id=len(counts) + 119540768
                        )
                        new_user.save()
                except Exception as e:
                    print(e)
                    continue
        self.update(owner, repo)
        # while 1:
        #     print(i)
        #     url = f"https://api.github.com/repos/{owner}/{repo}/pulls?page={i}&per_page={100}&state=all"
        #     json_result = requests.get(url=url, headers=self._random_header()).json()
        #     if len(json_result) == 0:
        #         break
        #     res.append(json_result)
        #     i = i + 1
        # with open(path, 'a+') as f:
        #     f.write(json.dumps(json_result))
        #     f.write("\n")
        # f.close()
        return res

    def test(self):
        url = f"https://api.github.com/rate_limit"
        json_result = requests.get(url=url, headers=self._random_header()).json()
        print(json_result)

    def get_stars(self, owner, repo):
        i = 1
        res = list()
        path = BASE_DIR + '/res/' + owner
        if not os.path.exists(path):
            os.mkdir(path)
        path = BASE_DIR + '/res/' + owner + "/" + repo
        if not os.path.exists(path):
            os.mkdir(path)
        t = models.Stars.objects.values("id").count()
        if t != 0:
            t = t / 100
            if t == 0:
                t = 1
            print(t)
            i = t
        path = path + "/stars.json"
        head = {"user-agent": util.get_user_agent(),
                "Authorization": "token " + util.get_api_token(),
                "Accept": "application/vnd.github.v3.star+json"}
        while 1:
            print(i)
            url = f"https://api.github.com/repos/{owner}/{repo}/stargazers?page={i}&per_page=100&state=all"
            json_result = requests.get(url=url, headers=head).json()
            if len(json_result) == 0:
                # if i < 2:
                break
            res.append(json_result)
            i = i + 1

        for t in range(len(res)):
            for k in range(len(res[t])):
                star = res[t][k]
                user = star["user"]
                old_star = models.Stars.objects.filter(login=user["login"], user=owner, repo_name=repo)
                if old_star.exists():
                    break
                starred_at = date_converter.string_to_datetime(star['starred_at'], "%Y-%m-%dT%H:%M:%SZ")
                try:
                    new_star = models.Stars.objects.create(
                        repo_name=repo,
                        user=owner,
                        login=user["login"],
                        starred_at=starred_at
                    )
                    new_star.save()
                except Exception as e:
                    print(e)
                    continue
        return

    def commit_page(self, owner, repo):
        url = f"https://github.com/{owner}/{repo}"
        html = urlopen(url)
        html_text = bytes.decode(html.read())
        # print(html_text)
        # obj = bf(html.read(),'html.parser')
        soup = BeautifulSoup(html_text, "html.parser")
        a = soup.find('a', href=f"/{owner}/{repo}/commits/master")
        b = re.sub("\D", "", a.text)
        return b
        # print(int_a)

    def contributor_page(self, owner, repo):
        url = f"https://github.com/{owner}/{repo}"
        html = urlopen(url)
        html_text = bytes.decode(html.read())
        soup = BeautifulSoup(html_text, "html.parser")
        a = soup.find('a', href=f"/{owner}/{repo}/graphs/contributors")
        b = re.sub("\D", "", a.text)
        return b

    def callback(self, status, result):
        # print(status)
        # print(result)
        pass

    def pull_page(self, owner, repo):
        url = f"https://github.com/{owner}/{repo}/pulls"
        html = urlopen(url)
        html_text = bytes.decode(html.read())
        soup = BeautifulSoup(html_text, "html.parser")
        res = []
        a = soup.find('a', href=f"/{owner}/{repo}/issues?q=is%3Aopen+is%3Apr")
        b = re.sub("\D", "", a.text)
        res.append(int(b))
        a = soup.find('a', href=f"/{owner}/{repo}/issues?q=is%3Apr+is%3Aclosed")
        b = re.sub("\D", "", a.text)
        res.append(int(b))
        return res

    def move(self, owner, repo):
        res = models.Issues.objects.filter(repo_name=repo).values("user_login", "user_id")
        res = list(res)
        for i in res:
            old_user = models.User.objects.filter(login=i["user_login"], owner=owner, repo=repo)
            if old_user.exists():
                d = list(old_user.values())
                t = d[0]["issues"] + 1
                models.User.objects.filter(login=i["user_login"], owner=owner,repo=repo).update(
                    issues=t
                )
            else:
                counts = models.User.objects.values("user_id")
                counts = list(counts)
                new_user = models.User.objects.create(
                    pulls=0, reviews=0, commit=0, issues=1,
                    login=i["user_login"],
                    id=i["user_id"], owner=owner, repo=repo,
                    user_id=len(counts) + 119540768
                )
                new_user.save()

    def get_companys(self, owner, repo):
        login_list = models.User.objects.filter(owner=owner,repo=repo).values("login").distinct()
        login_list = list(login_list)
        for i in range(len(login_list)):
            thread.run(func=self.company_page,
                       args=(login_list[i]["login"],),
                       callback=self.callback)
        # thread.run(func=self.__get_single_commit,
        #            args=(),
        #            callback=self.callback)
        thread.close()

    def company_page(self, owner):
        url = f"https://github.com/{owner}"
        html = urlopen(url)
        html_text = bytes.decode(html.read())
        soup = BeautifulSoup(html_text, "html.parser")
        a = soup.findAll('li', attrs={"class": "vcard-detail pt-1 hide-sm hide-md"})
        a = str(a)
        index = a.find("Organization") + len("Organization: ")
        t = a[index:]
        t = t[:t.find("\"")]
        if t == "none":
            return
        if len(t) == 0:
            return
        if t.find("=") != -1:
            return
        if t.find("card-detail pt-1 hide-sm") != -1:
            return
        if t.find("@") == 0:
            t = t[1:]
        t = t.lower()
        if t.find("facebook") != -1:
            t = "facebook"
        models.User.objects.filter(login=owner).update(
            company=t
        )
        return

    def set_up_company(self, owner, repo, type):
        if type == "issues":
            res = models.User.objects.filter(owner=owner, repo=repo, issues__gt=0).values("company").distinct()
        elif type == "pulls":
            res = models.User.objects.filter(owner=owner, repo=repo, pulls__gt=0).values("company").distinct()
        elif type == "commit":
            res = models.User.objects.filter(owner=owner, repo=repo, commit__gt=0).values("company").distinct()
        elif type == "reviews":
            res = models.User.objects.filter(owner=owner, repo=repo, reviews__gt=0).values("company").distinct()
        else:
            return
        res_list = list()
        for i in range(len(res)):
            if res[i]["company"] == None or res[i]["company"] == " ":
                continue
            temp_dict = dict()
            temp_dict["name"] = res[i]["company"]
            count = models.User.objects.filter(company=res[i]["company"], repo=repo, owner=owner).count()
            temp_dict["value"] = count
            res_list.append(temp_dict)
            old = models.Company.objects.filter(repo_name=repo, user=owner, company=res[i]["company"], type=type)
            if old.exists():
                old.update(
                    counts=count
                )
            else:
                models.Company.objects.create(
                    repo_name=repo, user=owner, company=res[i]["company"], type=type,counts=count
                )
        return
        # return JsonResponse(json.dumps({"result": res_list}), safe=False)

    def update(self, owner, repo):
        now = datetime.now()
        t = models.Basic.objects.filter(user=owner, repo_name=repo)
        t.update(
            updated_at=now
        )


if __name__ == '__main__':
    r = ReposRequester()
    #r.move("ant-design","ant-design")
    r.move("pytorch","pytorch")
    #r.move("ZJU-SEC","os22fall-stu")
    # r.set_up_company("ant-design","ant-design","pulls")
    # r.set_up_company("ant-design", "ant-design", "reviews")
    # r.set_up_company("ant-design", "ant-design", "commit")
    # r.set_up_company("ant-design", "ant-design", "issues")
    # r.set_up_company("pytorch", "pytorch", "issues")
    # r.set_up_company("pytorch", "pytorch", "reviews")
    # r.set_up_company("pytorch", "pytorch", "commit")
    # r.set_up_company("pytorch", "pytorch", "pulls")
    # r.get_pull_detail("pytorch","pytorch")
    # u = UserRequester()
    # print(r.get_repos("srx-2000", is_save=True))
    # user_list = u.get_users(100)
    # print(r.get_repos(user_list, is_save=True))
    # r.get_issues("pytorch", "pytorch")
    # print(r.get_pulls("pytorch", "pytorch"))
    # 爬取contributor
    # r.get_contributor("pytorch", "pytorch")
    # print(r.get_repos("pytorch", is_save=True))
    # print(r.get_repo_commit(username="pytorch", repo_name="pytorch", is_save=True))
