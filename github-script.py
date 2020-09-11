from github import Github, GithubException
from requests.exceptions import ConnectionError
import io
import json
import traceback
import csv
import time
import re

github_token = ""
github_repo = "dotnet/roslyn"
workspace = ""

def check_rate_limit(g):
    g.get_rate_limit()
    (remaining, maximum) = g.rate_limiting
    while remaining <= 20:
        print("    ", "Process is sleeping 1 hour due maximum rate limit reached.\n")
        time.sleep(3660)
        g = Github(github_token)
        g.per_page = 100
        g.get_rate_limit()
        (remaining, maximum) = g.rate_limiting
        print(g.rate_limiting)
    return g

"""
def get_issues(g):
    g = check_rate_limit(g)
    
    roslyn = g.get_repo(github_repo)
    g = check_rate_limit(g)
    
    # Get issues
    issues = roslyn.get_issues(state='all')
    g = check_rate_limit(g)

    print("Total issues to retrieve: ", issues.totalCount)
    print("    ", "0%")

    adv = 0
    
    flag = 20

    outCsvFile = open(workspace + 'issues.csv',  'w')
    csv_writer = csv.writer(outCsvFile)
    rows = [['issue_id', 'issue_no', 'pull_request_no', 'title', 'body']]

    try:
        c = 0
        attempt = 1
        seconds = 1
        while c < issues.totalCount:
            try:
                issue = issues[c]
                g = check_rate_limit(g)

                if issue.pull_request is None:
                    url = [ None ]
                else:
                    url = issue.pull_request.html_url.split("/")
                    url.reverse()
                title = '' if issue.title is None else issue.title.encode('utf8')
                body = '' if issue.body is None else issue.body.encode('utf8')
                rows.append([str(issue.id), issue.number, url[0], title, body])
                adv += 1
                if adv % int(issues.totalCount/10) == 0:
                    (remaining, maximum) = g.rate_limiting
                    print("    ", adv*100/issues.totalCount, "%,    remaining:", remaining)
                c = c + 1
                attempt = 1
                seconds = 1
            except GithubException as g:
                if g.status == 502 and attempt < 10:
                    print("Sleeping " + str(seconds) + " seconds.")
                    time.sleep(seconds)
                    seconds = seconds * 2
                    attempt = attempt + 1
                    continue
                else:
                    print(traceback.format_exc())
                    break
            except ConnectionError as ce:
                g = Github(github_token)
                g.per_page = 100
                continue
    except Exception as e:
        print(traceback.format_exc())

    csv_writer.writerows(rows)
    outCsvFile.close()

    print(g.rate_limiting)


def get_pulls(g):
    g = check_rate_limit(g)
    
    roslyn = g.get_repo(github_repo)
    g = check_rate_limit(g)

    # Get pull requests
    pulls = roslyn.get_pulls(state='all')
    
    g = check_rate_limit(g)

    print("Total pull requests to retrieve: ", pulls.totalCount)
    print("    ", "0%")

    adv = 0

    outCsvFile = open(workspace + 'pulls.csv',  'w')
    csv_writer = csv.writer(outCsvFile)
    rows = [['pull_id', 'pull_no', 'issue_no', 'title', 'body']]

    try:
        c = 0
        attempt = 1
        seconds = 1
        while c < pulls.totalCount:
            try:
                pull = pulls[c]
                g = check_rate_limit(g)
                if pull.issue_url is None:
                    url = [ None ]
                else:
                    url = pull.issue_url.split("/")
                    url.reverse()
                title = '' if pull.title is None else pull.title.encode('utf8')
                body = '' if pull.body is None else pull.body.encode('utf8')
                rows.append([str(pull.id), pull.number, url[0], title, body])
                adv += 1
                if adv % int(pulls.totalCount/10) == 0:
                    (remaining, maximum) = g.rate_limiting
                    print("    ", adv*100/pulls.totalCount, "%,    remaining:", remaining)
                c = c + 1
                attempt = 1
                seconds = 1
            except GithubException as g:
                if g.status == 502 and attempt < 10:
                    print("Sleeping " + str(seconds) + " seconds.")
                    time.sleep(seconds)
                    seconds = seconds * 2
                    attempt = attempt + 1
                    continue
                else:
                    print(traceback.format_exc())
                    break
            except ConnectionError as ce:
                g = Github(github_token)
                g.per_page = 100
                continue
    except Exception as e:
        print(traceback.format_exc())

    csv_writer.writerows(rows)
    outCsvFile.close()

    print(g.rate_limiting)


def get_issues_comments(g):
    g = check_rate_limit(g)
    
    roslyn = g.get_repo(github_repo)
    
    g = check_rate_limit(g)

    # Get issues comments
    issues_comments = roslyn.get_issues_comments()
    
    g = check_rate_limit(g)

    print("Total comments to retrieve: ", issues_comments.totalCount)
    print("    ", "0%")

    adv = 0

    outCsvFile = open(workspace + 'issues_comments.csv',  'w')
    csv_writer = csv.writer(outCsvFile)
    rows = [['issue_no', 'comment_no', 'comment_body']]

    try:
        c = 0
        attempt = 1
        seconds = 1
        while c < issues_comments.totalCount:
            try:
                comment = issues_comments[c]
                g = check_rate_limit(g)
                url = comment.issue_url.split("/")
                url.reverse()
                body = '' if comment.body is None else comment.body.encode('utf8')
                rows.append([url[0], str(comment.id), body])
                adv += 1
                if adv % int(issues_comments.totalCount/10) == 0:
                    (remaining, maximum) = g.rate_limiting
                    print("    ", adv*100/issues_comments.totalCount, "%,    remaining:", remaining)
                c = c + 1
                attempt = 1
                seconds = 1
            except GithubException as g:
                if g.status == 502 and attempt < 10:
                    print("Sleeping " + str(seconds) + " seconds.")
                    time.sleep(seconds)
                    seconds = seconds * 2
                    attempt = attempt + 1
                    continue
                else:
                    print(traceback.format_exc())
                    break
            except ConnectionError as ce:
                g = Github(github_token)
                g.per_page = 100
                continue
    except Exception as e:
        print(traceback.format_exc())

    csv_writer.writerows(rows)
    outCsvFile.close()

    print(g.rate_limiting)
"""
def get_pulls_comments(g):
    g = check_rate_limit(g)
    
    roslyn = g.get_repo(github_repo)
    
    g = check_rate_limit(g)

    # Get pulls comments
    pulls_comments = roslyn.get_pulls_review_comments()
    
    g = check_rate_limit(g)
    print("Total comments to retrieve: ", pulls_comments.totalCount)

    outCsvFile = open(workspace + 'pulls_comments.csv',  'r')
    csv_reader = csv.reader(outCsvFile)
    c = len(list(csv_reader))
    print("    There are already", c, "lines of data\n")
    outCsvFile = open(workspace + 'pulls_comments.csv',  'a')
    log_file = open("log.file","w")
    csv_writer = csv.writer(outCsvFile)
    rows = [['pull_no', 'comment_no', 'comment_body']]

    try:
        attempt = 1
        seconds = 1
        while c < pulls_comments.totalCount:
            try:
                comment = pulls_comments[c]
                g = check_rate_limit(g)
                url = comment.pull_request_url.split("/")
                url.reverse()
                body = '' if comment.body is None else comment.body.encode('utf8')
                rows.append([url[0], str(comment.id), body])
                progress = (c * 100) / pulls_comments.totalCount
                print("    ", progress, "%    ", end="\r")
                log_file.seek(0)
                log_file.write("Task progress: " + str(progress) + "\n")
                log_file.truncate()
                c += 1
                attempt = 1
                seconds = 1
            except GithubException as ge:
                if ge.status == 502 and attempt < 10:
                    print("    ", "Process is sleeping ", str(seconds), " seconds due GithubException.\n")
                    time.sleep(seconds)
                    seconds = seconds * 2
                    attempt = attempt + 1
                    continue
                else:
                    print("    ", "Process finished by unspected reason:", traceback.format_exc(), "\n")
                    break
            except ConnectionError as ce:
                print("    ", "Connection error. Resuming task.", end="\n")
                g = Github(github_token)
                g.per_page = 100
                continue
    except Exception as e:
        print("    ", "Process finished by unspected reason:", traceback.format_exc(), "\n")

    csv_writer.writerows(rows)
    outCsvFile.close()
    log_file.close()
    (remaining, maximum) = g.rate_limiting
    print("Remaining: " + str(remaining) + "Maximum: " + str(maximum) + "\n")

def link_pulls_and_issues():
    outCsvFile = open(workspace + 'link_pulls_issues.csv',  'w')
    csv_writer = csv.writer(outCsvFile)
    rows = [['pull_no', 'issue_no']]
    with open('pulls_comments.csv', newline='', encoding='utf-8') as inCsvFile:
        csv_reader = csv.reader(inCsvFile)
        for row in csv_reader:
            links = re.findall(r"([C|c]lose[s|d]?|[R|r]esolve[s|d]?|[F|f]ix|[F|f]ixe[s|d])\s+([\w|\-|/]*)?#(\d+)", str(row))
            print("    Analyzing line ", csv_reader.line_num, "    ", end="\r")
            for link in links:
                rows.append([row[0], link[2]])
    csv_writer.writerows(rows)
    inCsvFile.close()
    outCsvFile.close()


g = Github(github_token)
(remaining, maximum) = g.rate_limiting
print("Remaining: " + str(remaining) + " Maximum: " + str(maximum) + "\n")
g.per_page = 100

    
#get_pulls(g)
#get_issues(g)
#get_issues_comments(g)
get_pulls_comments(g)
#link_pulls_and_issues()
