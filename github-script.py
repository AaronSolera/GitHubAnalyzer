from github_handler import *
from data_handler import *
from statistics_handler import *
from pprint import *

github_token = "33c7e378a1a6bb6b892b8c1533dbac100de04c9f"
github_repo = input("Write repository's name (format: creator/repository): ")

g = get_repository(github_token, github_repo)

get_issues_and_pulls(g, github_repo)
get_issues_and_pulls_events(g, github_repo)
get_issues_comments(g, github_repo)
get_pulls_comments(g, github_repo)
get_commits_pulls(g, github_repo)
get_pulls_commits(g, github_repo)
analyze_linking_events(github_repo)
link_commits_pulls_and_issues(github_repo)
analyze_issues_and_pulls(github_repo)
get_pulls_commits_groups(github_repo)
get_linking_statistics(github_repo)