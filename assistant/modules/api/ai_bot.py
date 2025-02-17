import aiohttp
import json
from assistant.utils.config import Config

class OpenRouterAI:
    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(self):
        self.api_key = Config.OPENROUTER_API_KEY
        self.model = Config.OPENROUTER_MODEL

    async def ai_ask(self, prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": True
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.BASE_URL, headers=headers, json=data) as response:
                if response.status != 200:
                    return f"Ошибка API: {response.status}"
                
                full_response = []
                async for line in response.content:
                    chunk = line.decode('utf-8').replace('data: ', '')
                    try:
                        chunk_json = json.loads(chunk)
                        if "choices" in chunk_json:
                            content = chunk_json["choices"][0]["delta"].get("content", "")
                            if content:
                                full_response.append(content)
                    except:
                        continue
                return ''.join(full_response)
            

