import os
import requests
import json
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load key from .env
load_dotenv()

logger = logging.getLogger('OpenRouterAgent')

class OpenRouterAgent:
    def __init__(self, model="meta-llama/llama-3.1-8b-instruct:free"):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        
        if not self.api_key:
            raise ValueError("❌ OPENROUTER_API_KEY not found in .env file!")

    def chat(self, prompt, context=""):
        """Sends a prompt to OpenRouter and returns the response."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://hackathon-ai-employee.local", # Optional
            "X-Title": "Personal AI Employee Hackathon", # Optional
            "Content-Type": "application/json"
        }

        system_prompt = (
            "You are an Autonomous AI Employee (Gold Tier). Your workspace is an Obsidian Vault. "
            "You must process tasks by reading and writing markdown files. "
            "Context from the vault: \n" + context
        )

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        }

        try:
            response = requests.post(self.base_url, headers=headers, data=json.dumps(payload))
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0]['message']['content']
                else:
                    logger.error(f"❌ Unexpected OpenRouter response structure: {result}")
                    return None
            else:
                logger.error(f"❌ OpenRouter Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.error(f"❌ Connection Error: {e}")
            return None

if __name__ == "__main__":
    # Test
    agent = OpenRouterAgent()
    print(agent.chat("Say hello and tell me you are ready for the Gold Tier."))
