import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class LLMProvider:
    """
    다양한 LLM 엔진을 캡슐화하여 에이전트에게 일관된 인터페이스를 제공합니다.
    """
    def __init__(self, provider_type=None):
        self.provider_type = provider_type or os.getenv("LLM_PROVIDER", "gemini")
        self.api_key = os.getenv("GOOGLE_API_KEY")
        
        if self.provider_type == "gemini":
            if self.api_key:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-pro')
            else:
                self.model = None
        # 나중에 OpenAI, Claude 등을 여기에 추가 가능
        elif self.provider_type == "openai":
            # self.model = OpenAIModel(...)
            pass

    async def ask(self, prompt: str):
        """
        LLM에게 질문하고 답변을 반환합니다.
        """
        if self.provider_type == "gemini" and self.model:
            response = self.model.generate_content(prompt)
            # 마크다운 태그 제거 로직 포함
            return response.text.replace("```python", "").replace("```", "").strip()
        
        # 시뮬레이션 모드 (API 키가 없는 경우)
        return "def main():\n    print('Mock code from Simulation')\n"

# 싱글톤 인스턴스
llm = LLMProvider()
