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


g = Github(github_token)
(remaining, maximum) = g.rate_limiting
print("Remaining: " + str(remaining) + " Maximum: " + str(maximum) + "\n")
g.per_page = 100

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

def get_pulls_comments(g):
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

def get_issues_and_pulls(g):
    g = check_rate_limit(g)
    
    roslyn = g.get_repo("dotnet/roslyn")
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
                log_file.write("Task progress: " + str(c*100/issues.totalCount) + "\n")
                log_file.truncate()
                c = c + 1
                attempt = 1
                seconds = 1
            except GithubException as ge:
                if ge.status == 502 and attempt < 10:
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

    csv_writerpull.writerows(rowspull)
    outCsvFilepull.close()

    log_file.close()

    print(g.rate_limiting)

def get_issues_and_pulls_events(g):
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
                log_file.write("Task progress: " + str(progress) + "\n")
                log_file.truncate()
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

    issues_events_csv_writer.writerows(issues_events_rows)
    pulls_events_csv_writer.writerows(pulls_events_rows)
    
    issuesEventsCsvFile.close()
    pullsEventsCsvFile.close()
    log_file.close()
"""
def del_duplicates(l):
    return list(dict.fromkeys(l))

def csv_to_json_list(csv_path):
    with open(csv_path, "r") as csvfile:
        lines = csvfile.read().splitlines()
        keys = lines[0].split(",")
        keys_length = len(keys)
        cvs_list = []
        for line in lines[1:]:
            temp_json = {}
            row = line.split(",", keys_length)
            if not (len(row) < keys_length):
                for index in range(keys_length):
                    temp_json[keys[index]] = row[index]
                cvs_list.append(temp_json)
    return cvs_list
    
def generate_json_from_csv(key_attribute, csv_path):
    """
    This function returns a JSON structure like
    {
        {key_1: { atr1: [data_1, data_2, ... , data_n], atr_2: [data_1, data_2, ... , data_n], ... , atr_n: [data_1, data_2, ... , data_n]}},
        {key_2: { atr1: [data_1, data_2, ... , data_n], atr_2: [data_1, data_2, ... , data_n], ... , atr_n: [data_1, data_2, ... , data_n]}},
        ... ,
        {key_n: { atr1: [data_1, data_2, ... , data_n], atr_2: [data_1, data_2, ... , data_n], ... , atr_n: [data_1, data_2, ... , data_n]}},
    }
    """
    json = {}
    with open(csv_path, "r") as csvfile:
        lines = csvfile.read().splitlines()
        keys = lines[0].split(",")
        keys_length = len(keys)
        key_id_index = keys.index(key_attribute)
        keys.remove(key_attribute)
        for line in lines[1:]:
            row = line.split(",", keys_length)
            if not (len(row) < keys_length):
                key = row[key_id_index]
                row.remove(key)
                if not key in json:
                    json[key] = {}
                    for column in range(0, keys_length - 1):
                        json[key][keys[column]] = [row[column]]
                else:
                    for column in range(0, keys_length - 1):
                        json[key][keys[column]].append(row[column])
    return json

def analyze_issues_and_pulls():
    """
    #   Generating organized JSON data from issues related csv files
    """
    issues_json = generate_json_from_csv("issue_no","issues.csv")
    issues_json.update(generate_json_from_csv("issue_no","issues_comments.csv"))
    """
    #   Generating organized JSON data from pull requests related csv files
    """
    pulls_json = generate_json_from_csv("pull_no","pulls.csv")
    pulls_json.update(generate_json_from_csv("pull_no","pulls_comments.csv"))
    """
    #   Analysing issue data JSON
    """
    rows = [['issue_no','found_id','is_issue','is_pull_request']]
    statistics = {"issue numbers":0,"pull request numbers":0,"both":0,"unknown":0}
    issue_progress_counter = 0

    for (issue_no, attributes) in issues_json.items():
        for attr in ["title","body","comment_body"]:
            if attr in attributes:
                for attribute in attributes[attr]:
                    links = re.findall(r"([C|c]lose[s|d]?|[R|r]esolve[s|d]?|[F|f]ix|[F|f]ixe[s|d])?\s+([\w|\-|/]*)?#(\d+)", attribute)
                    print("    Analyzing issues data. Progress ", (issue_progress_counter * 100)/len(issues_json), "    ", end="\r")
                    for link in links:
                        is_issue = link[2] in issues_json
                        is_pull_request = link[2] in pulls_json
                        if is_issue: statistics["issue numbers"] += 1 
                        if is_pull_request: statistics["pull request numbers"] += 1 
                        if is_issue and is_pull_request: statistics["both"] += 1 
                        if not is_issue and not is_pull_request: statistics["unknown"] += 1 
                        rows.append([issue_no, link[2], is_issue, is_pull_request])
        issue_progress_counter += 1
    """
    #   Printing statistics
    """
    print("\n","-"*30)
    print("Statistics for issue data analysis")
    print("-"*30)
    print("Total links found:",len(rows))
    for (text, value) in statistics.items():
        print("Links that are",text,":",value)
    print("-"*30,"\n\n")
    """
    #   Creating cvs file
    """
    outCsvFile = open(workspace + 'issues_analysis.csv',  'w')
    csv_writer = csv.writer(outCsvFile)
    csv_writer.writerows(rows)
    outCsvFile.close()
    """
    #   Analysing pull request data JSON
    """
    rows = [['pull_no','found_id','is_issue','is_pull_request']]
    statistics = {"issue numbers":0,"pull request numbers":0,"both":0,"unknown":0}
    pull_progress_counter = 0

    for (pull_no, attributes) in pulls_json.items():
        for attr in ["title","body","comment_body"]:
            if attr in attributes:
                for attribute in attributes[attr]:
                    links = re.findall(r"([C|c]lose[s|d]?|[R|r]esolve[s|d]?|[F|f]ix|[F|f]ixe[s|d])?\s+([\w|\-|/]*)?#(\d+)", attribute)
                    print("    Analyzing pull requests data. Progress ", (pull_progress_counter * 100)/len(pulls_json), "    ", end="\r")
                    for link in links:
                        is_issue = link[2] in issues_json
                        is_pull_request = link[2] in pulls_json
                        if is_issue: statistics["issue numbers"] += 1 
                        if is_pull_request: statistics["pull request numbers"] += 1 
                        if is_issue and is_pull_request: statistics["both"] += 1 
                        if not is_issue and not is_pull_request: statistics["unknown"] += 1 
                        rows.append([pull_no, link[2], is_issue, is_pull_request])
        pull_progress_counter += 1
    """
    #   Printing statistics
    """
    print("\n","-"*30)
    print("Statistics for pull request data analysis")
    print("-"*30)
    print("Total links found:",len(rows))
    for (text, value) in statistics.items():
        print("Links that are",text,":",value)
    print("-"*30)
    """
    #   Creating cvs file
    """
    outCsvFile = open(workspace + 'pull_request_analysis.csv',  'w')
    csv_writer = csv.writer(outCsvFile)
    csv_writer.writerows(rows)
    outCsvFile.close()

def analyze_linking_events():
    issues_events_list = csv_to_json_list('issues_events.csv')
    pulls_events_list = csv_to_json_list('pulls_events.csv')

    filtered_issues_events_list = []
    filtered_pulls_events_list = []

    for issue_event in issues_events_list:
        if issue_event['event'] in ['connected','disconnected']:
            filtered_issues_events_list.append(issue_event)

    for pull_event in pulls_events_list:
        if pull_event['event'] in ['connected','disconnected']:
            filtered_pulls_events_list.append(pull_event) 

    linked_issues_and_pull_events = [['issue_no', 'pull_no', 'actor', 'created_at', 'event']]

    for issue_event in filtered_issues_events_list:
        for pull_event in filtered_pulls_events_list:

            issue_relevant_data = [issue_event['actor'], issue_event['created_at'], issue_event['event']]
            pull_relevant_data = [pull_event['actor'], pull_event['created_at'], pull_event['event']]

            if issue_relevant_data == pull_relevant_data:
                linked_issues_and_pull_events.append([issue_event['issue_no'], pull_event['pull_no']] + issue_relevant_data) 
    
    analyzedEventsCsvFile = open(workspace + 'linking_analysis.csv',  'w')

    issues_events_csv_writer = csv.writer(analyzedEventsCsvFile)
    issues_events_csv_writer.writerows(linked_issues_and_pull_events)
    
    analyzedEventsCsvFile.close()

def get_pulls_commits(g):
    g = check_rate_limit(g)
    
    roslyn = g.get_repo(github_repo)
    g = check_rate_limit(g)
    
    # Get issues
    issues = roslyn.get_issues(state = "all")
    g = check_rate_limit(g)

    print("Total issues and pull requests to retrieve: ", issues.totalCount)

    pullCommitsCsvFile = open(workspace + 'pulls_commits.csv',  'w')
    log_file = open("log.file","w")
    commit_csv_writer = csv.writer(pullCommitsCsvFile)
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
                    for commit in commits.__iter__():
                        pull_commits_rows.append([pull.id, pull.number, commit.sha])
                log_file.seek(0)
                log_file.write("Task progress: " + str(c*100/issues.totalCount) + "\n")
                log_file.truncate()
                c = c + 1
                attempt = 1
                seconds = 1
            except GithubException as ge:
                if ge.status == 502 and attempt < 10:
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

    commit_csv_writer.writerows(pull_commits_rows)
    commits_total_csv_writer.writerows(pull_commits_total_rows)

    pullCommitsCsvFile.close()
    pullCommitsTotalCsvFile.close()
    log_file.close()

    print(g.rate_limiting)

def get_commits_pulls(g):
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


def link_commits_pulls_and_issues(g):
    g = check_rate_limit(g)
    
    roslyn = g.get_repo(github_repo)
    # Get commits
    commits = roslyn.get_commits()
    
    g = check_rate_limit(g)
    print("Total comments to retrieve: ", commits.totalCount)

    outCsvFile = open(workspace + 'linked_commits_pulls_and_issues.csv',  'w')
    log_file = open("log.file","w")

    csv_writer = csv.writer(outCsvFile)

    linked_pull_issues = generate_json_from_csv("pull_no", workspace + "pull_request_analysis.csv")
    pulls_without_commits = generate_json_from_csv("total_commits", workspace + "pulls_commits_total.csv")
    manual_linked_pull_issues = csv_to_json_list(workspace + "linking_analysis.csv")

    rows = [['commit_sha', 'pull_no', 'issue_no']]
    # ---------------------------------------------------------------
    # This code deletes disconnected events from linking_analysis.csv 
    # ---------------------------------------------------------------
    index = 0
    while index < len(manual_linked_pull_issues):
        current_element = manual_linked_pull_issues[index]
        if current_element['event'] == 'disconnected':
            delete_index = 0
            element = manual_linked_pull_issues[delete_index]
            while delete_index < len(manual_linked_pull_issues) and element['issue_no'] != current_element['issue_no'] and element['pull_no'] != current_element['issue_no'] and element['event'] != 'connected':
                delete_index += 1
                element = manual_linked_pull_issues[delete_index]
            del manual_linked_pull_issues[index]
            del manual_linked_pull_issues[delete_index]
        index += 1
    # ---------------------------------------------------------------
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
                    rows.append([commit.sha, 'None', 'None'])
                else:
                    # If there are ...
                    for pull in pulls.__iter__():
                        # Saving all posible boolean scenarios for a pull-issue linking event
                        there_are_issues = str(pull.number) in linked_pull_issues
                        there_are_manual_issues = str(pull.number) in manual_linked_pull_issues
                        there_are_not_issues = (not there_are_issues) and (not there_are_manual_issues)
                        # Taking action according boolean scenario
                        if there_are_issues:
                            found_id = linked_pull_issues[str(pull.number)]['found_id']
                            is_issue = linked_pull_issues[str(pull.number)]['is_issue']
                            for i in range(len(is_issue)):
                                if is_issue[i] == 'True':
                                    rows.append([commit.sha, pull.number, found_id[i]])
                        if there_are_manual_issues:
                            for link in manual_linked_pull_issues:
                                if str(pull.number) == link['pull_no']:
                                    rows.append([commit.sha, pull.number, link['issue_no']])
                        if there_are_not_issues:
                            rows.append([commit.sha, pull.number, 'None'])
            
                progress = (c * 100) / commits.totalCount
                #print("    ", progress, "%    ", end="\r")
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
    # ---------------------------------------------------------------
    # This codes link all pulls without commits with issues
    # ---------------------------------------------------------------
    for pull in pulls_without_commits['0']['pull_no']:
        # Saving all posible boolean scenarios for a pull-issue linking event
        there_are_issues = pull in linked_pull_issues
        there_are_manual_issues = pull in manual_linked_pull_issues
        there_are_not_issues = not there_are_issues and not there_are_manual_issues
        # Taking action according boolean scenario
        if there_are_issues:
            found_id = linked_pull_issues[pull]['found_id']
            is_issue = linked_pull_issues[pull]['is_issue']
            for i in range(len(is_issue)):
                if is_issue[i] == 'True':
                    rows.append(['None', pull, found_id[i]])
        if there_are_manual_issues:
            for link in manual_linked_pull_issues:
                if pull == link['pull_no']:
                    rows.append(['None', pull, link['issue_no']])
        if there_are_not_issues:
            rows.append(['None', pull, 'None'])
    # ---------------------------------------------------------------
    csv_writer.writerows(rows)

    outCsvFile.close()
    log_file.close()

    (remaining, maximum) = g.rate_limiting
    print("Remaining: " + str(remaining) + "Maximum: " + str(maximum) + "\n")

def get_linking_statistics():
    # ------------------------------------------------
    # Getting updated total number of issues, commits and pulls
    # ------------------------------------------------
    issues = generate_json_from_csv('issue_no', 'issues.csv')
    pulls = generate_json_from_csv('pull_no', 'pulls.csv')
    commits = generate_json_from_csv('commit_sha', 'linked_commits_pulls_and_issues.csv')
    issues_total = len(issues)
    pulls_total = len(pulls)
    commits_total = len(commits) - 1 #This minus 1 is for None value commits
    # ------------------------------------------------
    linking_statistics = open("linking_statistics.txt","w")
    pair = { 'issues-pulls':[], 'pulls-commits':[], 'commits-issues':[], 'only-pulls':[], 'only-issues':[] }
    linking_data = csv_to_json_list('linked_commits_pulls_and_issues.csv')
    # Progress variable
    progress = 0
    # Storing all pair in pair dictionary if they are possible to build
    for link in linking_data:
        print("    Task progress: ", progress  * 100 / len(linking_data), "%    ", end="\r")

        if link['pull_no'] != 'None' and link['issue_no'] != 'None':
            pair['issues-pulls'].append(link['issue_no'] + "-" + link['pull_no'])

        if link['pull_no'] != 'None' and link['commit_sha'] != 'None':
            pair['pulls-commits'].append(link['pull_no'] + "-" + link['commit_sha'])
            pair['only-pulls'].append(link['pull_no'])

        if link['commit_sha'] != 'None' and link['issue_no'] != 'None':
            pair['commits-issues'].append(link['commit_sha'] + "-" + link['issue_no'])
            pair['only-issues'].append(link['issue_no'])

        progress += 1
    # Getting the number of non-repeated elements in each pair 
    pair['issues-pulls'] = len(del_duplicates(pair['issues-pulls']))
    pair['pulls-commits'] = len(del_duplicates(pair['pulls-commits']))
    pair['commits-issues'] = len(del_duplicates(pair['commits-issues']))
    pair['only-pulls'] = len(del_duplicates(pair['only-pulls']))
    pair['only-issues'] = len(del_duplicates(pair['only-issues']))

    # Computing pair percentages
    issues_pulls_percentage = pair['issues-pulls'] * 100 / issues_total
    pulls_issues_percentage = pair['issues-pulls'] * 100 / pulls_total
    pulls_commits_percentage = pair['only-pulls']    * 100 / pulls_total
    commits_pulls_percentage = pair['pulls-commits'] * 100 / commits_total
    issues_commits_percentage = pair['only-issues']    * 100 / issues_total
    commits_issues_percentage = pair['commits-issues'] * 100 / commits_total
    # Storing all statistics in one string
    statistics =  "--------------------------------------------------------------"
    statistics += "\nNúmero de pares issues-pulls: "                + str(pair['issues-pulls'])
    statistics += "\nNúmero de issues no asociados a pulls: "       + str(issues_total - pair['issues-pulls']) 
    statistics += "\nNúmero de pulls no asociados a issues: "       + str(pulls_total  - pair['issues-pulls']) + "\n"
    statistics += "\nPorcentaje de issues asociados a pulls: "      + str(issues_pulls_percentage)
    statistics += "\nPorcentaje de issues no asociados a pulls: "   + str(100 - issues_pulls_percentage)
    statistics += "\nPorcentaje de pulls asociados a issues: "      + str(pulls_issues_percentage)
    statistics += "\nPorcentaje de pulls no asociados a issues: "   + str(100 - pulls_issues_percentage)
    statistics += "\n--------------------------------------------------------------"
    statistics += "\nNúmero de pares pulls-commits: "               + str(pair['pulls-commits'])
    statistics += "\nNúmero de pulls no asociados a commits: "      + str(pulls_total    - pair['only-pulls']) 
    statistics += "\nNúmero de commits no asociados a pulls: "      + str(commits_total  - pair['pulls-commits']) + "\n"
    statistics += "\nPorcentaje de pulls asociados a commits: "     + str(pulls_commits_percentage)
    statistics += "\nPorcentaje de pulls no asociados a commits: "  + str(100 - pulls_commits_percentage)
    statistics += "\nPorcentaje de commits asociados a pulls: "     + str(commits_pulls_percentage)
    statistics += "\nPorcentaje de commits no asociados a pulls: "  + str(100 - commits_pulls_percentage)
    statistics += "\n--------------------------------------------------------------"
    statistics += "\nNúmero de pares commits-issues: "              + str(pair['commits-issues'])
    statistics += "\nNúmero de commits no asociados a issues: "     + str(commits_total - pair['commits-issues']) 
    statistics += "\nNúmero de issues no asociados a commits: "     + str(issues_total  - pair['only-issues']) + "\n"
    statistics += "\nPorcentaje de commits asociados a issues: "    + str(commits_issues_percentage)
    statistics += "\nPorcentaje de commits no asociados a issues: " + str(100 - commits_issues_percentage)
    statistics += "\nPorcentaje de issues asociados a commits: "    + str(issues_commits_percentage)
    statistics += "\nPorcentaje de issues no asociados a commits:"  + str(100 - issues_commits_percentage)
    statistics += "\n--------------------------------------------------------------"

    linking_statistics.write(statistics)

    linking_statistics.close()

#get_pulls(g)
#get_issues(g)
#get_issues_comments(g)
#get_pulls_comments(g)
#get_issues_and_pulls(g)
#get_issues_and_pulls_events(g)

get_commits_pulls(g)

#link_commits_pulls_and_issues(g)
#analyze_issues_and_pulls()
#get_linking_statistics()

#input("Press any key to close...")