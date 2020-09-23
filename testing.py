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
issue_no = 1
pull_no = 3
issu = roslyn.get_issue(issue_no)
pull = roslyn.get_pull(pull_no)

issues_comments = roslyn.get_issues_comments()
pulls_comments = roslyn.get_pulls_comments()
pulls_review_comments = roslyn.get_pulls_review_comments()

for issues_comment in issues_comments.__iter__():
    print("Issues comment:",issues_comment.body)

for pulls_comment in pulls_comments.__iter__():
    print("Pulls comment:",pulls_comment.body)

for pulls_review_comment in pulls_review_comments.__iter__():
    print("Pulls review comment:", pulls_review_comment.body)

"""
pull_commnets = roslyn.get_pulls_review_comments()
issue_commnets = roslyn.get_issues_comments()

for pull_commnet in pull_commnets.__iter__():
    print(pull_commnet)

print("-"*30)

for issue_commnet in issue_commnets.__iter__():
    print(issue_commnet)


issue_events = issue.get_events()
pull_events = pull.get_issue_events() 

print("pull as issue -> ", pull.as_issue())

for issue_event in issue_events.__iter__():
    print("issue ", issue_no, " event -> ", issue_event.event)

for pull_event in pull_events.__iter__():
    print("pull -> ", pull_no, " event -> ", pull_event.event)
"""

input("\nPress any key to close...")
