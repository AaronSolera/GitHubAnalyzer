from github import Github, GithubException
from requests.exceptions import ConnectionError
import io
import json
import traceback
import csv
import time
import re

github_token = ""
github_repo = "AaronSolera/GitHubAnalyzer"
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

roslyn = g.get_repo(github_repo)
g = check_rate_limit(g)

# Get pull requests
issue = roslyn.get_issue(1)
pull = roslyn.get_pull(5)

issue_events = issue.get_events()
pull_events = pull.get_issue_events() 

for issue_event in issue_events.__iter__():
    print("issue -> ", issue_event.event)

for pull_event in pull_events.__iter__():
    print("pull -> ", pull_event.event, "commit_id -> ")

input("\nPress any key to close...")
