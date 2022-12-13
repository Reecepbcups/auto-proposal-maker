import requests, datetime, os
from util import get_env

from dotenv import load_dotenv
load_dotenv()

current_dir = os.path.dirname(os.path.realpath(__file__))
todays_date = datetime.datetime.now()


BEARER_TOKEN = get_env("BEARER_TOKEN")
REPO = get_env("REPO_API")
LAST_UPGRADE_TIME = datetime.datetime.strptime(get_env("LAST_UPGRADE_TIME"), "%Y-%m-%dT%H:%M:%SZ")

headers = {
    'Accept': 'application/vnd.github+json',    
    'Authorization': f'Bearer {BEARER_TOKEN}',    
    'X-GitHub-Api-Version': '2022-11-28',
}


def get_number_of_commits(commit_api_url: str) -> int:
    # https://api.github.com/repos/CosmosContracts/juno/pulls/368/commits
    response = requests.get(commit_api_url, headers=headers).json()
    return len(response)   


sorted_by_num_commits = {}
def get_prs_output(show_body=False, ignore_dependabot=True):
    url = f"{REPO}/pulls?state=closed?page=2?per_page=100" # Loop through multiple pages? ?page=1
    # OUTPUT = ""

    response = requests.get(url, headers=headers).json()
    for idx, pr in enumerate(response):
        print(f"Processing PR {idx+1}/{len(response)}")


        title = pr.get("title", None)
        pr_url = pr.get("url", None)
        if 'pull' not in pr_url: continue

        body = pr.get("body", None)
        if body is None: body = ""
        body = body.replace("```", "")
        
        state = pr.get("state", None)
        if state != "closed": continue

        opening_user = pr.get("user", {}).get("login", None)
        opening_user_url = pr.get("user", {}).get("html_url", None)

        if opening_user == "dependabot[bot]": 
            if ignore_dependabot == True: continue
            body = ""         

        commits_url = pr.get("commits_url", None)

        # ensure branch is base? base.label == CosmosContracts:main

        # We only want merged PRs since the last upgrade
        merged_at = pr.get("merged_at", None)
        if merged_at is None:
            continue
        
        if datetime.datetime.strptime(merged_at, "%Y-%m-%dT%H:%M:%SZ") < LAST_UPGRADE_TIME:
            print(f"Skipping PR {title} as it is older than last upgrade")
            continue


        num_of_commits = get_number_of_commits(commits_url)        

        v = sorted_by_num_commits.get(num_of_commits, "")
        v += f"""\n### [{title}]({pr_url}) ([{opening_user}]({opening_user_url}))\n\nCommits: {num_of_commits}\n"""
        if show_body == True:
            v += f"""{body}\n"""
        sorted_by_num_commits[num_of_commits] = v

    # return OUTPUT

    # return sorted_by_num_commits sorted by the key 
    return " ".join([v for k, v in sorted(sorted_by_num_commits.items(), key=lambda item: item[0], reverse=True)])