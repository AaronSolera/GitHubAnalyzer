import csv
import re
from time import *
from os import path
from datetime import date

def write_execution_time_log(github_repo, method_name, execution_time):
    workspace = github_repo.split("/")[1] + '/statistics/'
    if path.exists(workspace + 'execution_time_log.csv'):
        timeLogCsvFile = open(workspace + 'execution_time_log.csv','a')
    else:
        timeLogCsvFile = open(workspace + 'execution_time_log.csv','w+')
        timeLogCsvFile.write('method_name,date,execution_time')
    timeLogCsvFile.write('\n' + method_name +','+ date.today().strftime("%d/%m/%Y") +','+ str(execution_time))
    timeLogCsvFile.close()

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

def analyze_issues_and_pulls(github_repo):
    start_time = time()
    workspace = github_repo.split("/")[1] + '/files/'
    log_file = open("log.file","w")
    """
    #   Generating organized JSON data from issues related csv files
    """
    issues_json = generate_json_from_csv("issue_no", workspace + "issues.csv")
    issues_json.update(generate_json_from_csv("issue_no", workspace + "issues_comments.csv"))
    """
    #   Generating organized JSON data from pull requests related csv files
    """
    pulls_json = generate_json_from_csv("pull_no", workspace + "pulls.csv")
    pulls_json.update(generate_json_from_csv("pull_no", workspace + "pulls_comments.csv"))
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
                    log_file.seek(0)
                    log_file.write("Current Method: analyze_issues_and_pulls\n    Task progress: " + str((issue_progress_counter * 100)/len(issues_json)) + "\n")
                    log_file.truncate()
                    #print("    Analyzing issues data. Progress ", (issue_progress_counter * 100)/len(issues_json), "    ", end="\r")
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
                    log_file.seek(0)
                    log_file.write("Current Method: analyze_issues_and_pulls\n    Task progress: " + str((pull_progress_counter * 100)/len(pulls_json)) + "\n")
                    log_file.truncate()
                    #print("    Analyzing pull requests data. Progress ", (pull_progress_counter * 100)/len(pulls_json), "    ", end="\r")
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
    log_file.close()

    write_execution_time_log(github_repo, "analyze_issues_and_pulls", time() - start_time)

def analyze_linking_events(github_repo):
    start_time = time()
    workspace = github_repo.split("/")[1] + '/files/'
    issues_events_list = csv_to_json_list(workspace + 'issues_events.csv')
    pulls_events_list = csv_to_json_list(workspace + 'pulls_events.csv')

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

    write_execution_time_log(github_repo, "analyze_linking_events", time() - start_time)

def link_commits_pulls_and_issues(github_repo):
    start_time = time()
    workspace = github_repo.split("/")[1] + '/files/'
    outCsvFile = open(workspace + 'linked_commits_pulls_and_issues.csv',  'w')
    log_file = open("log.file","w")

    csv_writer = csv.writer(outCsvFile)

    commits_pulls = generate_json_from_csv("commit_sha", workspace + "commits_pulls.csv")
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
    c = 0
    for (commit_sha, attributes) in commits_pulls.items():
        if len(attributes['pull_no']) == 0:
            # If there is not pulls for this commit
            rows.append([commit_sha, 'None', 'None'])
        else:
            # If there are ...
            for pull_no in attributes['pull_no']:
                # Saving all posible boolean scenarios for a pull-issue linking event
                there_are_issues = pull_no in linked_pull_issues
                there_are_manual_issues = pull_no in manual_linked_pull_issues
                there_are_not_issues = (not there_are_issues) and (not there_are_manual_issues)
                # Taking action according boolean scenario
                if there_are_issues:
                    found_id = linked_pull_issues[pull_no]['found_id']
                    is_issue = linked_pull_issues[pull_no]['is_issue']
                    for i in range(len(is_issue)):
                        if is_issue[i] == 'True':
                            rows.append([commit_sha, pull_no, found_id[i]])
                if there_are_manual_issues:
                    for link in manual_linked_pull_issues:
                        if pull_no == link['pull_no']:
                            rows.append([commit_sha, pull_no, link['issue_no']])
                if there_are_not_issues:
                    rows.append([commit_sha, pull_no, 'None'])
        progress = (c * 100) / len(commits_pulls)
        log_file.seek(0)
        log_file.write("Current Method: link_commits_pulls_and_issues\n    Task progress: " + str(progress) + "\n")
        log_file.truncate()
        #print("    ", progress, "%    ", end="\r")
        c += 1
    # ---------------------------------------------------------------
    # This codes link all pulls without commits with issues
    # ---------------------------------------------------------------
    if '0' in pulls_without_commits:
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

    write_execution_time_log(github_repo, "link_commits_pulls_and_issues", time() - start_time)

def group_pulls_and_commits(github_repo):
    """
    This function returns a JSON structure like
    {
        { group_1: { pulls: [data_1, data_2, ... , data_n], commits: [data_1, data_2, ... , data_n] } },
        { group_2: { pulls: [data_1, data_2, ... , data_n], commits: [data_1, data_2, ... , data_n] } },
        ... ,
        { group_n: { pulls: [data_1, data_2, ... , data_n], commits: [data_1, data_2, ... , data_n] } },
    }
    """
    workspace  = github_repo.split("/")[1] + '/files/'
    linked_elements = csv_to_json_list(workspace + "linked_commits_pulls_and_issues.csv")[::-1]
    log_file   = open("log.file","w")
    groups = {}
    group_counter = 0
    progress_counter = 0

    for element in linked_elements:
        found = False
        if element['pull_no'] != 'None' and element['commit_sha'] != 'None':
            for (group, attributes) in groups.items():
                if element['pull_no'] in attributes['pulls']:
                    groups[group]['commits'].append(element['commit_sha'])
                    found = True
                    break
                if element['commit_sha'] in attributes['commits']:
                    groups[group]['pulls'].append(element['pull_no'])
                    found = True
                    break
            if not found:
                groups[group_counter] = {}
                groups[group_counter]['commits'] = [element['commit_sha']]
                groups[group_counter]['pulls']   = [element['pull_no']]
                group_counter += 1
        progress = (progress_counter * 100) / len(linked_elements)
        log_file.seek(0)
        log_file.write("Current Method: get_pulls_commits_groups\n    Task progress: " + str(progress) + "\n")
        log_file.truncate()
        #print("    ", progress, "%    ", end="\r")
        progress_counter += 1
    log_file.close()
    return groups

def get_pulls_commits_groups(github_repo):
    start_time = time()
    workspace  = github_repo.split("/")[1] + '/files/'
    groupsTotalCsvFile = open(workspace + 'pulls_commits_groups_total.csv',  'w')
    groupsCsvFile = open(workspace + 'pulls_commits_groups.csv',  'w')
    groups_total_csv_writer = csv.writer(groupsTotalCsvFile)
    groups_csv_writer = csv.writer(groupsCsvFile)

    groups_total_rows = [['group','oldest_pull','pulls_total','commits_total']]
    groups_rows = [['group','elements']]

    groups = group_pulls_and_commits(github_repo)

    for (group, attributes) in groups.items():
        # Turn into integers all elements in attributes['pulls']
        int_pulls = [int(e) for e in attributes['pulls']]
        groups_total_rows.append([group, min(int_pulls), len(attributes['pulls']), len(attributes['commits'])])
        groups_rows.append([group] + attributes['pulls'] + attributes['commits'])

    groups_total_csv_writer.writerows(groups_total_rows)
    groups_csv_writer.writerows(groups_rows)

    groupsTotalCsvFile.close()
    groupsCsvFile.close()

    write_execution_time_log(github_repo, "get_pulls_commits_groups", time() - start_time)