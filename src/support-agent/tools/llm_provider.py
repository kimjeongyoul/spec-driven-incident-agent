import os
from dotenv import load_dotenv

try:
    import google.generativeai as genai
except ImportError:
    genai = None

load_dotenv()

class LLMProvider:
    def __init__(self, provider_type=None):
        self.provider_type = provider_type or os.getenv("LLM_PROVIDER", "gemini")
        self.api_key = os.getenv("GOOGLE_API_KEY")
        
        self.model = None
        if self.provider_type == "gemini" and genai:
            if self.api_key:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-pro')

    async def ask(self, prompt: str):
        if self.provider_type == "gemini" and self.model:
            response = self.model.generate_content(prompt)
            return response.text.replace("```python", "").replace("```", "").strip()
        return "def main():\n    # Mock code for testing\n    print('Running with 5s Timeout...')\n"

llm = LLMProvider()
