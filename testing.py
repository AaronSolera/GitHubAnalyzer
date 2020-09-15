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
pull = roslyn.get_pull(2)
issue = pull.as_issue()
print(issue.as_pull_request())

input("\nPress any key to close...")
