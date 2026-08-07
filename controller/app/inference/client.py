import httpx
from ..app.config import settings


class InferenceClient:
    def __init__(self):
        self.base_url = settings.inference_api_url
        self.api_key = settings.inference_api_key

    async def _headers(self):
        return {"X-API-Key": self.api_key, "Content-Type": "application/json"}

    async def decision(self, prompt: str, tier: str = "fast", context: Optional[dict] = None, max_tokens: int = 256) -> dict:
        payload = {
            "tier": tier,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": 0.7,
            "context": context or {},
        }
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(f"{self.base_url}/v1/decision", json=payload, headers=await self._headers())
            resp.raise_for_status()
            return resp.json()

    async def chat(self, prompt: str, tier: str = "fast", max_tokens: int = 128) -> dict:
        payload = {"tier": tier, "prompt": prompt, "max_tokens": max_tokens, "temperature": 0.8}
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(f"{self.base_url}/v1/chat", json=payload, headers=await self._headers())
            resp.raise_for_status()
            return resp.json()

    async def embedding(self, text: str) -> list:
        payload = {"prompt": text, "max_tokens": 1}
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{self.base_url}/v1/embedding", json=payload, headers=await self._headers())
            resp.raise_for_status()
            data = resp.json()
            return data.get("embedding", [])


inference_client = InferenceClient()
