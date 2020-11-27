from github_handler import *
from data_handler import *
from statistics_handler import *
from pprint import *

github_token = "1fb2f8ccbc7b12603b98277d50fa4f7f3180173a"
github_repo = "dotnet/efcore"

g = get_repository(github_token, github_repo)

get_issues_and_pulls(g, github_repo)
get_issues_and_pulls_events(g, github_repo)
get_issues_comments(g, github_repo)
get_pulls_comments(g, github_repo)
get_commits_pulls(g, github_repo)
get_pulls_commits(g, github_repo)
analyze_linking_events(github_repo)
analyze_issues_and_pulls(github_repo)
link_commits_pulls_and_issues(github_repo)
analyze_issues_and_pulls(github_repo)
get_pulls_commits_groups(github_repo)
get_linking_statistics(github_repo)
