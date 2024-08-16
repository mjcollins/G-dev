import requests
from typing import Dict, Any

class KnowledgeBase:
    def __init__(self):
        self.api_url = "https://api.duckduckgo.com/"

    def search(self, query: str) -> Dict[str, Any]:
        params = {
            'q': query,
            'format': 'json',
            'no_html': 1,
            'skip_disambig': 1
        }
        response = requests.get(self.api_url, params=params)
        return response.json()

    def query(self, command: str) -> str:
        result = self.search(command)
        
        if result['Abstract']:
            return f"Result: {result['Abstract']}"
        elif result['RelatedTopics']:
            return f"Related: {result['RelatedTopics'][0]['Text']}"
        else:
            return "No information found for the given query."