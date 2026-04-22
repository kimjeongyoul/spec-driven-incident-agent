import os
import time
from dotenv import load_dotenv

try:
    from github import Github, GithubException
except ImportError:
    Github = GithubException = None

load_dotenv()

class GitHubProvider:
    """GitHub 서비스 전용 구현체"""
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.repo_name = os.getenv("GITHUB_REPO")
        self.base_branch = os.getenv("GITHUB_BASE_BRANCH", "main")
        self.repo = None
        if Github and self.token and self.repo_name:
            try:
                self.g = Github(self.token)
                self.repo = self.g.get_repo(self.repo_name)
            except Exception:
                self.repo = None

    def create_branch(self, branch_name):
        if not self.repo: return True # Simulation mode
        source = self.repo.get_branch(self.base_branch)
        self.repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=source.commit.sha)
        return True

    def update_file(self, branch_name, file_path, content, message):
        if not self.repo: return True # Simulation mode
        contents = self.repo.get_contents(file_path, ref=branch_name)
        self.repo.update_file(path=contents.path, message=message, content=content, sha=contents.sha, branch=branch_name)
        return True

    def create_pr(self, branch_name, title, body):
        if not self.repo: return "https://github.com/mock/pr/123"
        pr = self.repo.create_pull(title=title, body=body, head=branch_name, base=self.base_branch)
        return pr.html_url

class GitLabProvider:
    """GitLab 서비스 전용 구현체 (확장용)"""
    def create_branch(self, branch_name): return True
    def update_file(self, branch_name, file_path, content, message): return True
    def create_pr(self, branch_name, title, body): return "https://gitlab.com/mock/pr/123"

class GitProvider:
    """
    [Factory Provider] 
    환경 변수(GIT_PROVIDER)에 따라 적절한 Git 서비스 엔진을 제공합니다.
    """
    def __init__(self):
        self.provider_type = os.getenv("GIT_PROVIDER", "github").lower()
        if self.provider_type == "github":
            self.instance = GitHubProvider()
        elif self.provider_type == "gitlab":
            self.instance = GitLabProvider()
        else:
            self.instance = GitHubProvider() # Default

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
