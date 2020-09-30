from github import Github, GithubException
from requests.exceptions import ConnectionError
import io
import json
import traceback
import csv
import time
import re

github_token = "bc6c00431fda07373db60ca7aa00d55ba77a5a3a"
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
"""

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
        for lines in lines[1:]:
            row = lines.split(",", keys_length)
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
    """
    #   Generating organized JSON data from pull requests related csv files
    """
    pulls_json = generate_json_from_csv("pull_no","pulls.csv")
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

#get_pulls(g)
#get_issues(g)
#get_issues_comments(g)
#get_pulls_comments(g)
#link_pulls_and_issues()
#get_issues_and_pulls(g)
get_issues_and_pulls_events(g);
