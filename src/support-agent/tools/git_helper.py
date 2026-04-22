import os
import time
from github import Github, GithubException
from dotenv import load_dotenv

load_dotenv()

class GitHubHelper:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.repo_name = os.getenv("GITHUB_REPO")
        self.base_branch = os.getenv("GITHUB_BASE_BRANCH", "main")
        
        if not self.token or not self.repo_name:
            raise ValueError(".env 파일에 GITHUB_TOKEN과 GITHUB_REPO를 설정해주세요.")
        
        self.g = Github(self.token)
        self.repo = self.g.get_repo(self.repo_name)

    def create_hotfix_branch(self):
        """
        새로운 hotfix 브랜치를 생성합니다. (설정된 base_branch 기준)
        """
        timestamp = int(time.time())
        branch_name = f"hotfix/incident-{timestamp}"
        
        try:
            source = self.repo.get_branch(self.base_branch)
            self.repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=source.commit.sha)
            print(f"[Git] {self.base_branch}로부터 브랜치 생성 완료: {branch_name}")
            return branch_name
        except GithubException as e:
            print(f"[Git Error] 브랜치 생성 실패: {str(e)}")
            return None

    def update_file_and_commit(self, branch_name, file_path, new_content, commit_message):
        """
        파일을 수정하고 지정된 브랜치에 커밋합니다.
        """
        try:
            contents = self.repo.get_contents(file_path, ref=branch_name)
            self.repo.update_file(
                path=contents.path,
                message=commit_message,
                content=new_content,
                sha=contents.sha,
                branch=branch_name
            )
            print(f"[Git] 파일 수정 및 커밋 완료: {file_path}")
            return True
        except Exception as e:
            print(f"[Git Error] 파일 수정 실패: {str(e)}")
            return False

    def create_pull_request(self, branch_name, title, body):
        """
        수정된 브랜치에 대해 Pull Request를 생성합니다. (설정된 base_branch로)
        """
        try:
            pr = self.repo.create_pull(
                title=title,
                body=body,
                head=branch_name,
                base=self.base_branch
            )
            print(f"[Git] Pull Request 생성 완료: {pr.html_url}")
            return pr.html_url
        except GithubException as e:
            print(f"[Git Error] PR 생성 실패: {str(e)}")
            return None
