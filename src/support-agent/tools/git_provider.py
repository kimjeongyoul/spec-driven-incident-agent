import os
import time
from dotenv import load_dotenv

try:
    from github import Github, GithubException
except ImportError:
    Github = GithubException = None

load_dotenv()

class GitHubProvider:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.repo_name = os.getenv("GITHUB_REPO")
        self.base_branch = os.getenv("GITHUB_BASE_BRANCH", "main")
        self.repo = None
        if Github and self.token and self.repo_name:
            self.g = Github(self.token)
            self.repo = self.g.get_repo(self.repo_name)

    def create_branch(self, branch_name):
        if not self.repo: return True # Mock success
        source = self.repo.get_branch(self.base_branch)
        self.repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=source.commit.sha)
        return True

    def update_file(self, branch_name, file_path, content, message):
        if not self.repo: return True # Mock success
        contents = self.repo.get_contents(file_path, ref=branch_name)
        self.repo.update_file(path=contents.path, message=message, content=content, sha=contents.sha, branch=branch_name)
        return True

    def create_pr(self, branch_name, title, body):
        if not self.repo: return "https://github.com/mock/pr/123"
        pr = self.repo.create_pull(title=title, body=body, head=branch_name, base=self.base_branch)
        return pr.html_url

class GitProvider:
    def __init__(self):
        self.instance = GitHubProvider()

    def create_hotfix_branch(self):
        timestamp = int(time.time())
        branch_name = f"hotfix/incident-{timestamp}"
        if self.instance.create_branch(branch_name):
            return branch_name
        return None

    def update_file_and_commit(self, branch_name, file_path, content, message):
        return self.instance.update_file(branch_name, file_path, content, message)

    def create_pull_request(self, branch_name, title, body):
        return self.instance.create_pr(branch_name, title, body)
