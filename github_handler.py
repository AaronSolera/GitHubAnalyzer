from github import Github, GithubException
from requests.exceptions import ConnectionError
import io
import json
import traceback
import csv
import os
from statistics_handler import *
from data_handler import *
from time import *

def check_rate_limit(g):
    g.get_rate_limit()
    (remaining, maximum) = g.rate_limiting
    while remaining <= 20:
        print("    ", "Process is sleeping 1 hour due maximum rate limit reached.\n")
        sleep(3660)
        g.per_page = 100
        g.get_rate_limit()
        (remaining, maximum) = g.rate_limiting
        print(g.rate_limiting)
    return g

def get_repository(github_token, github_repo):
    workspace = github_repo.split("/")[1]
    if not os.path.exists(workspace + '/files'):
        os.makedirs(workspace + '/files')
    if not os.path.exists(workspace + '/statistics'):
        os.makedirs(workspace + '/statistics')
    g = Github(github_token)
    (remaining, maximum) = g.rate_limiting
    print("Remaining: " + str(remaining) + " Maximum: " + str(maximum) + "\n")
    g.per_page = 100
    return g

def get_issues(g, github_repo):
    start_time = time()
    workspace = github_repo.split("/")[1] + '/files/'

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
    log_file = open("log.file","w")

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
                log_file.seek(0)
                log_file.write("Current Method: get_issues\n    Task progress: " + str(c*100/issues.totalCount) + "\n")
                log_file.truncate()
                c = c + 1
                attempt = 1
                seconds = 1
            except GithubException as g:
                if g.status == 502 and attempt < 10:
                    print("Sleeping " + str(seconds) + " seconds.")
                    sleep(seconds)
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
    log_file.close()

    print(g.rate_limiting)
    write_execution_time_log(github_repo, "get_issues", time() - start_time)


def get_pulls(g, github_repo):
    start_time = time()
    workspace = github_repo.split("/")[1] + '/files/'
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
    log_file = open("log.file","w")

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
                log_file.seek(0)
                log_file.write("Current Method: get_pulls\n    Task progress: " + str(c*100/pulls.totalCount) + "\n")
                log_file.truncate()
                c = c + 1
                attempt = 1
                seconds = 1
            except GithubException as g:
                if g.status == 502 and attempt < 10:
                    print("Sleeping " + str(seconds) + " seconds.")
                    sleep(seconds)
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
    log_file.close()

    print(g.rate_limiting)
    write_execution_time_log(github_repo, "get_pulls", time() - start_time)


def get_issues_comments(g, github_repo):
    start_time = time()
    workspace = github_repo.split("/")[1] + '/files/'

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
    log_file = open("log.file","w")

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
                log_file.seek(0)
                log_file.write("Current Method: get_issues_comments\n    Task progress: " + str(c*100/issues_comments.totalCount) + "\n")
                log_file.truncate()
                c = c + 1
                attempt = 1
                seconds = 1
            except GithubException as g:
                if g.status == 502 and attempt < 10:
                    print("Sleeping " + str(seconds) + " seconds.")
                    sleep(seconds)
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
    log_file.close()

    print(g.rate_limiting)
    write_execution_time_log(github_repo, "get_issues_comments", time() - start_time)

def get_pulls_comments(g, github_repo):
    start_time = time()
    workspace = github_repo.split("/")[1] + '/files/'

    g = check_rate_limit(g)
    
    roslyn = g.get_repo(github_repo)
    
    g = check_rate_limit(g)

    # Get pulls comments
    pulls_comments = roslyn.get_pulls_review_comments()
    
    g = check_rate_limit(g)
    print("Total comments to retrieve: ", pulls_comments.totalCount)

    outCsvFile = open(workspace + 'pulls_comments.csv',  'a+')
    log_file = open("log.file","w")

    csv_writer = csv.writer(outCsvFile)
    csv_reader = csv.reader(outCsvFile)
    rows = [['pull_no', 'comment_no', 'comment_body']]

    try:
        c = len(list(csv_reader))
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
                #print("    ", progress, "%    ", end="\r")
                log_file.seek(0)
                log_file.write("Current Method: get_pulls_comments\n    Task progress: " + str(progress) + "\n")
                log_file.truncate()
                c += 1
                attempt = 1
                seconds = 1
            except GithubException as ge:
                if ge.status == 502 and attempt < 10:
                    print("    ", "Process is sleeping ", str(seconds), " seconds due GithubException.\n")
                    sleep(seconds)
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

    write_execution_time_log(github_repo, "get_pulls_comments", time() - start_time)

def get_issues_and_pulls(g, github_repo):
    start_time = time()
    workspace = github_repo.split("/")[1] + '/files/'

    g = check_rate_limit(g)
    
    roslyn = g.get_repo(github_repo)
    g = check_rate_limit(g)
    
    # Get issues
    issues = roslyn.get_issues(state = "all")
    g = check_rate_limit(g)

    print("Total issues and pull requests to retrieve: ", issues.totalCount)
    print("    ", "0%")

    outCsvFile = open(workspace + 'issues.csv',  'w')
    log_file = open("log.file","w")

    csv_writer = csv.writer(outCsvFile)
    rows = [['issue_id', 'issue_no', 'title', 'body']]
    
    outCsvFilepull = open(workspace + 'pulls.csv',  'w')
    csv_writerpull = csv.writer(outCsvFilepull)
    rowspull = [['pull_id', 'pull_no', 'title', 'body']]

    try:
        c = 0
        attempt = 1
        seconds = 1
        while c < issues.totalCount:
            try:
                issue = issues[c]
                g = check_rate_limit(g)
                
                url = issue.html_url.split("/")
                is_issue = (url[-2] == "issues")

                title = '' if issue.title is None else issue.title.encode('utf8')
                body = '' if issue.body is None else issue.body.encode('utf8')
                if is_issue:
                    rows.append([str(issue.id), issue.number, title, body])
                else:
                    rowspull.append([str(issue.id), issue.number, title, body])
                log_file.seek(0)
                log_file.write("Current Method: get_issues_and_pulls\n    Task progress: " + str(c*100/issues.totalCount) + "\n")
                log_file.truncate()
                c = c + 1
                attempt = 1
                seconds = 1
            except GithubException as ge:
                if ge.status == 502 and attempt < 10:
                    print("Sleeping " + str(seconds) + " seconds.")
                    sleep(seconds)
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

    csv_writerpull.writerows(rowspull)
    outCsvFilepull.close()

    log_file.close()

    print(g.rate_limiting)
    write_execution_time_log(github_repo, "get_issues_and_pulls", time() - start_time)

def get_issues_and_pulls_events(g, github_repo):
    start_time = time()
    workspace = github_repo.split("/")[1] + '/files/'

    g = check_rate_limit(g)
    
    roslyn = g.get_repo(github_repo)
    
    g = check_rate_limit(g)

    # Get issues comments
    issues_events = roslyn.get_issues_events()
    
    g = check_rate_limit(g)
    print("-"*30,"\n","Getting issues events from",github_repo,"\n","-"*30)
    print("Total events to retrieve: ", issues_events.totalCount)

    issuesEventsCsvFile = open(workspace + 'issues_events.csv',  'w')
    pullsEventsCsvFile = open(workspace + 'pulls_events.csv',  'w')
    log_file = open("log.file","w")

    issues_events_csv_writer = csv.writer(issuesEventsCsvFile)
    pulls_events_csv_writer = csv.writer(pullsEventsCsvFile)

    issues_events_rows = [['issue_no', 'actor', 'event', 'event_id', 'created_at']]
    pulls_events_rows = [['pull_no', 'actor', 'event', 'event_id', 'created_at']]

    try:
        c = 0
        attempt = 1
        seconds = 1
        while c < issues_events.totalCount:
            try:
                event = issues_events[c]
                g = check_rate_limit(g)
                url = event.issue.html_url.split("/")
                is_issue = (url[-2] == "issues")
                if event.actor:
                    temp_row = [event.issue.number, event.actor.login, event.event, event.id, event.created_at]
                else:
                    temp_row = [event.issue.number, None, event.event, event.id, event.created_at]
                if is_issue:
                    issues_events_rows.append(temp_row)
                else:
                    pulls_events_rows.append(temp_row)
                progress = (c * 100) / issues_events.totalCount
                #print("     Task progress: ", progress, "%    ", end="\r")
                log_file.seek(0)
                log_file.write("Current Method: get_issues_and_pulls_events\n    Task progress: " + str(progress) + "\n")
                log_file.truncate()
                c = c + 1
                attempt = 1
                seconds = 1
            except GithubException as g:
                if g.status == 502 and attempt < 10:
                    print("Sleeping " + str(seconds) + " seconds.")
                    sleep(seconds)
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

    issues_events_csv_writer.writerows(issues_events_rows)
    pulls_events_csv_writer.writerows(pulls_events_rows)
    
    issuesEventsCsvFile.close()
    pullsEventsCsvFile.close()
    log_file.close()

    print(g.rate_limiting)
    write_execution_time_log(github_repo, "get_issues_and_pulls_events", time() - start_time)

def get_pulls_commits(g, github_repo):
    start_time = time()
    workspace = github_repo.split("/")[1] + '/files/'

    g = check_rate_limit(g)
    
    roslyn = g.get_repo(github_repo)
    g = check_rate_limit(g)
    
    # Get issues
    issues = roslyn.get_issues(state = "all")
    g = check_rate_limit(g)

    print("Total issues and pull requests to retrieve: ", issues.totalCount)

    #pullCommitsCsvFile = open(workspace + 'pulls_commits.csv',  'w')
    #commit_csv_writer = csv.writer(pullCommitsCsvFile)
    log_file = open("log.file","w")

    pull_commits_rows = [['pull_id', 'pull_no', 'commit_sha']]
    
    pullCommitsTotalCsvFile = open(workspace + 'pulls_commits_total.csv',  'w')
    commits_total_csv_writer = csv.writer(pullCommitsTotalCsvFile)
    pull_commits_total_rows = [['pull_id', 'pull_no', 'total_commits']]

    try:
        c = 0
        attempt = 1
        seconds = 1
        while c < issues.totalCount:
            try:
                issue = issues[c]
                g = check_rate_limit(g)
                
                url = issue.html_url.split("/")
                is_issue = (url[-2] == "issues")

                title = '' if issue.title is None else issue.title.encode('utf8')
                body = '' if issue.body is None else issue.body.encode('utf8')
                if not is_issue:
                    pull = issue.as_pull_request()
                    commits = pull.get_commits()
                    pull_commits_total_rows.append([pull.id, pull.number, commits.totalCount])
                    """
                    for commit in commits.__iter__():
                        pull_commits_rows.append([pull.id, pull.number, commit.sha])
                    """
                log_file.seek(0)
                log_file.write("Current Method: get_pulls_commits\n    Task progress: " + str(c*100/issues.totalCount) + "\n")
                log_file.truncate()
                c = c + 1
                attempt = 1
                seconds = 1
            except GithubException as ge:
                if ge.status == 502 and attempt < 10:
                    print("Sleeping " + str(seconds) + " seconds.")
                    sleep(seconds)
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

    #commit_csv_writer.writerows(pull_commits_rows)
    commits_total_csv_writer.writerows(pull_commits_total_rows)

    #pullCommitsCsvFile.close()
    pullCommitsTotalCsvFile.close()
    log_file.close()

    print(g.rate_limiting)
    write_execution_time_log(github_repo, "get_pulls_commits", time() - start_time)

def get_commits_pulls(g, github_repo):
    start_time = time()
    workspace = github_repo.split("/")[1] + '/files/'

    g = check_rate_limit(g)
    
    roslyn = g.get_repo(github_repo)
    # Get commits
    commits = roslyn.get_commits()
    
    g = check_rate_limit(g)
    print("Total comments to retrieve: ", commits.totalCount)

    outCsvFile = open(workspace + 'commits_pulls.csv',  'w')
    log_file = open("log.file","w")

    csv_writer = csv.writer(outCsvFile)

    rows = [['commit_sha', 'pull_no']]

    try:
        c = 0
        attempt = 1
        seconds = 1
        while c < commits.totalCount:
            try:
                commit = commits[c]
                g = check_rate_limit(g)
                pulls = commit.get_pulls()
                if pulls.totalCount == 0:
                    # If there is not pulls for this commit
                    rows.append([commit.sha, 'None'])
                else:
                    # If there are ...
                    for pull in pulls.__iter__():
                         rows.append([commit.sha, pull.number])
            
                progress = (c * 100) / commits.totalCount
                #print("    ", progress, "%    ", end="\r")
                log_file.seek(0)
                log_file.write("Current Method: get_commits_pulls\n    Task progress: " + str(progress) + "\n")
                log_file.truncate()
                c += 1
                attempt = 1
                seconds = 1
            except GithubException as ge:
                if ge.status == 502 and attempt < 10:
                    print("    ", "Process is sleeping ", str(seconds), " seconds due GithubException.\n")
                    sleep(seconds)
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
    
    write_execution_time_log(github_repo, "get_commits_pulls", time() - start_time)