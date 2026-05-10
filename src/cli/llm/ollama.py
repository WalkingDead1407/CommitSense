import requests
from typing import Optional


class OllamaClient:
    DEFAULT_URL = "http://localhost:11434"
    DEFAULT_MODEL = "qwen2.5-coder:7b"

    def __init__(self, base_url: str = DEFAULT_URL, model: str = DEFAULT_MODEL):
        """args:base_url: Ollama server URL
              model: Model name to use"""
        self.base_url = base_url
        self.model = model

    def health_check(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            if response.status_code != 200:
                return False

            data = response.json()
            models = [m.get("name", "") for m in data.get("models", [])]
            # check if model is loaded
            return any(self.model in m for m in models)
        except (requests.RequestException, ValueError):
            return False

    def get_status_message(self) -> str:
        """returns: message describing available models or connection error"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            if response.status_code == 200:
                data = response.json()
                models = [m.get("name", "") for m in data.get("models", [])]
                available = ", ".join(models) if models else "none"
                return f"Available models: {available}"
        except:
            pass
        return "Ollama not responding"
