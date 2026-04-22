import subprocess
import os

class SelfTester:
    def __init__(self, target_file="src/app.py"):
        self.target_file = target_file

    def run_syntax_check(self):
        """
        수정된 코드의 문법(Syntax)을 체크합니다.
        """
        try:
            # compile()을 사용하여 실행 없이 문법만 체크
            with open(self.target_file, "r", encoding="utf-8") as f:
                compile(f.read(), self.target_file, 'exec')
            return True, "Syntax OK"
        except SyntaxError as e:
            error_msg = f"SyntaxError at line {e.lineno}: {e.msg}\nCode: {e.text}"
            return False, error_msg
        except Exception as e:
            return False, str(e)

    def run_unit_tests(self):
        """
        (시뮬레이션) 실제 유닛 테스트(pytest 등)를 실행합니다.
        """
        # 여기서는 간단히 성공을 반환하거나, 특정 조건에서 실패를 유도할 수 있습니다.
        # 실제로는 subprocess.run(["pytest", ...]) 등을 사용합니다.
        print(f"[Tester] {self.target_file}에 대한 유닛 테스트 실행 중...")
        
        # 시뮬레이션: 파일 내용에 'Timeout'이 없으면 실패하게 설정
        with open(self.target_file, "r", encoding="utf-8") as f:
            if "Timeout" not in f.read():
                return False, "Error: Timeout logic is missing in the code."
        
        return True, "All tests passed."

if __name__ == "__main__":
    tester = SelfTester()
    success, msg = tester.run_syntax_check()
    print(f"Test Result: {success}, Message: {msg}")
