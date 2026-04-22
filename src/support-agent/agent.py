import os
from tools.spec_tool import spec_search, code_read

class SupportAgent:
    def __init__(self, system_prompt_path: str):
        with open(system_prompt_path, "r", encoding="utf-8") as f:
            self.system_prompt = f.read()
        self.history = []

    def react(self, user_query: str):
        """
        사용자의 질문에 대해 ReAct 루프를 수행합니다.
        (이 루프는 실제로는 LLM에 의해 제어되지만, 여기서는 핵심 흐름을 시뮬레이션합니다.)
        """
        print(f"\n[USER]: {user_query}")
        
        # 1. Thought (첫 번째 생각)
        print("\n[Thought]: 사용자의 질문을 분석하고 관련 명세를 확인해야 합니다.")
        
        # 2. Action (명세 검색)
        keyword = user_query.split()[-1] # 간단한 키워드 추출 예시
        print(f"[Action]: spec_search('{keyword}') 실행 중...")
        observation = spec_search(keyword)
        
        # 3. Observation
        print(f"[Observation]: 명세 검색 결과가 확인되었습니다.")
        
        # 4. Final Conclusion (최종 답변)
        if "--- File:" in observation:
            print("\n[Conclusion]: 명세에 근거하여 답변을 드립니다.")
            print(f"참조 문서: {observation.split('---')[1].strip()}")
            print("-" * 50)
            print("사용자님의 질문에 대한 답변은 해당 명세에 정의되어 있습니다.")
        else:
            print("\n[Conclusion]: 현재 명세에서 관련 내용을 찾을 수 없습니다. 새로운 명세 작성이 필요해 보입니다.")

if __name__ == "__main__":
    # 실행 경로 설정
    prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "system_prompt.txt")
    agent = SupportAgent(prompt_path)
    
    # 예시 질문
    agent.react("아키텍처에 대해 알려줘")
