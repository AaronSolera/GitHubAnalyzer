import csv
from math import *
from data_handler import *
from time import *

def get_linking_statistics(github_repo):
    start_time = time()
    workspace = github_repo.split("/")[1]
    # ------------------------------------------------
    # Getting updated total number of issues, commits and pulls
    # ------------------------------------------------
    issues = generate_json_from_csv('issue_no', workspace + '/files/issues.csv')
    pulls = generate_json_from_csv('pull_no', workspace + '/files/pulls.csv')
    commits = generate_json_from_csv('commit_sha', workspace + '/files/linked_commits_pulls_and_issues.csv')
    issues_total = len(issues)
    pulls_total = len(pulls)
    commits_total = len(commits) - 1 #This minus 1 is for None value commits
    # ------------------------------------------------
    linking_statistics = open(workspace + '/statistics/linking_statistics.txt','w')
    pair = { 'issues-pulls':[], 'pulls-commits':[], 'commits-issues':[], 'only-pulls':[], 'only-issues':[] }
    linking_data = csv_to_json_list(workspace + '/files/linked_commits_pulls_and_issues.csv')
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
    # Getting al pull data in a JSON with key as pull_no
    pulls = generate_json_from_csv('pull_no', workspace + '/files/linked_commits_pulls_and_issues.csv')
    # Statistics variables
    commit_min = {'sha':'','value': inf}
    commit_max = {'sha':'','value': 0}
    commit_average = 0 
    pull_min = {'no':'','value': inf}
    pull_max = {'no':'','value': 0}
    pull_average = 0
    # Getting min, max and average pulls values for commits
    for (commit_sha, attributes) in commits.items():
        if not 'None' in attributes['pull_no'] and commit_sha != 'None':
            pulls_len = len(del_duplicates(attributes['pull_no']))
            if pulls_len < commit_min['value']:
                commit_min['sha'] = commit_sha
                commit_min['value'] = pulls_len
            if pulls_len > commit_max['value']:
                commit_max['sha'] = commit_sha
                commit_max['value'] = pulls_len
            commit_average += pulls_len / len(commits)
    # Getting min, max and average commits values for pulls
    for (pull_no, attributes) in pulls.items():
        if not 'None' in attributes['commit_sha'] and pull_no != 'None':
            commits_len = len(del_duplicates(attributes['commit_sha']))
            if commits_len < pull_min['value']:
                pull_min['no'] = pull_no
                pull_min['value'] = commits_len
            if commits_len > pull_max['value']:
                pull_max['no'] = pull_no
                pull_max['value'] = commits_len
            pull_average += commits_len / len(pulls)
    # Getting the number of non-repeated elements in each pair 
    pair['issues-pulls'] = len(del_duplicates(pair['issues-pulls']))
    pair['pulls-commits'] = len(del_duplicates(pair['pulls-commits']))
    pair['commits-issues'] = len(del_duplicates(pair['commits-issues']))
    pair['only-pulls'] = len(del_duplicates(pair['only-pulls']))
    pair['only-issues'] = len(del_duplicates(pair['only-issues']))
    # Computing pair percentages
    if issues_total != 0:
        issues_pulls_percentage = pair['issues-pulls'] * 100 / issues_total
        issues_commits_percentage = pair['only-issues']    * 100 / issues_total
    else:
        issues_pulls_percentage = 0
        issues_commits_percentage = 0
    if pulls_total != 0:
        pulls_issues_percentage = pair['issues-pulls'] * 100 / pulls_total
        pulls_commits_percentage = pair['only-pulls']    * 100 / pulls_total
    else:
        pulls_issues_percentage = 0
        pulls_commits_percentage = 0
    if commits_total != 0:
        commits_pulls_percentage = pair['pulls-commits'] * 100 / commits_total
        commits_issues_percentage = pair['commits-issues'] * 100 / commits_total
    else:
        commits_pulls_percentage = 0
        commits_issues_percentage = 0
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
    statistics += "\nEl commit " + commit_min['sha'] + " tiene asociado " + str(commit_min['value']) + " pulls, lo cual es la mímima cantidad de pulls asociados a commits"
    statistics += "\nEl commit " + commit_max['sha'] + " tiene asociado " + str(commit_max['value']) + " pulls, lo cual es la máxima cantidad de pulls asociados a commits"
    statistics += "\nLa cantidad promedio de pull requests asociados a commits es " + str(commit_average) + "\n"
    statistics += "\nEl pull request " + pull_min['no'] + " tiene asociado " + str(pull_min['value']) + " commits, lo cual es la mímima cantidad de commits asociados a pulls"
    statistics += "\nEl pull request " + pull_max['no'] + " tiene asociado " + str(pull_max['value']) + " commits, lo cual es la máxima cantidad de commits asociados a pulls"
    statistics += "\nLa cantidad promedio de commits asociados a pull requests es " + str(pull_average)
    statistics += "\n--------------------------------------------------------------"

    linking_statistics.write(statistics)

    linking_statistics.close()

    write_execution_time_log(github_repo, "get_linking_statistics", time() - start_time)
