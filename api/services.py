import httpx
from django.conf import settings

API_URL = API_URL = "https://router.huggingface.co/hf-inference/models/cardiffnlp/twitter-roberta-base-sentiment"

headers = {
    "Authorization": f"Bearer {settings.HF_API_KEY}"
}

async def analyze_sentiment(text):
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(
            API_URL,
            headers=headers,
            json={"inputs": text}
        )

        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code} - {response.text}")

        data = response.json()

        # Handle model loading case
        if isinstance(data, dict) and "error" in data:
            raise Exception(data["error"])

        return data