import os
import time
from github import Github, GithubException
from dotenv import load_dotenv

load_dotenv()

class GitHubProvider:
    """GitHub 구현체"""
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.repo_name = os.getenv("GITHUB_REPO")
        self.base_branch = os.getenv("GITHUB_BASE_BRANCH", "main")
        
        if self.token and self.repo_name:
            self.g = Github(self.token)
            self.repo = self.g.get_repo(self.repo_name)
        else:
            self.repo = None

    def create_branch(self, branch_name):
        if not self.repo: return False
        source = self.repo.get_branch(self.base_branch)
        self.repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=source.commit.sha)
        return True

    def update_file(self, branch_name, file_path, content, message):
        if not self.repo: return False
        contents = self.repo.get_contents(file_path, ref=branch_name)
        self.repo.update_file(path=contents.path, message=message, content=content, sha=contents.sha, branch=branch_name)
        return True

    def create_pr(self, branch_name, title, body):
        if not self.repo: return "http://mock-pr-url.com"
        pr = self.repo.create_pull(title=title, body=body, head=branch_name, base=self.base_branch)
        return pr.html_url

class GitProvider:
    """Git 통합 캡슐화 레이어"""
    def __init__(self):
        self.provider_type = os.getenv("GIT_PROVIDER", "github")
        if self.provider_type == "github":
            self.instance = GitHubProvider()
        # 나중에 GitLabProvider, CodeCommitProvider 등을 여기에 추가

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
