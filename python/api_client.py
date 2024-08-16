import requests
import json
from typing import List, Dict, Generator
from config import API_KEY, API_URL

class AnthropicAPIClient:
    def __init__(self):
        self.api_key = API_KEY
        self.api_url = API_URL

    def send_message(self, message: str, system_prompt: str, conversation_history: List[Dict[str, str]]) -> str:
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key,
        }

        data = {
            "messages": conversation_history + [{"role": "user", "content": message}],
            "system": system_prompt,
            "model": "claude-2",
            "max_tokens_to_sample": 1000,
        }

        response = requests.post(self.api_url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json()["content"][0]["text"]

    def stream_message(self, message: str, system_prompt: str, conversation_history: List[Dict[str, str]]) -> Generator[str, None, None]:
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key,
        }

        data = {
            "messages": conversation_history + [{"role": "user", "content": message}],
            "system": system_prompt,
            "model": "claude-2",
            "max_tokens_to_sample": 1000,
            "stream": True,
        }

        response = requests.post(self.api_url, headers=headers, data=json.dumps(data), stream=True)
        response.raise_for_status()

        for line in response.iter_lines():
            if line:
                yield json.loads(line)["content"][0]["text"]