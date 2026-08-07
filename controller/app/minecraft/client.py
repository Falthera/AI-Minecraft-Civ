import httpx
from ..app.config import settings


class MinecraftApiClient:
    def __init__(self):
        self.base_url = settings.minecraft_api_url
        self.api_key = settings.minecraft_api_key

    async def _headers(self):
        return {"X-API-Key": self.api_key, "Content-Type": "application/json"}

    async def get_agent_state(self, agent_id: str) -> dict:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base_url}/api/v1/agents/{agent_id}", headers=await self._headers())
            resp.raise_for_status()
            return resp.json()

    async def execute_action(self, agent_id: str, action: str, params: dict) -> dict:
        payload = {"action": action, "params": params}
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{self.base_url}/api/v1/agents/{agent_id}/actions", json=payload, headers=await self._headers())
            resp.raise_for_status()
            return resp.json()

    async def get_nearby(self, agent_id: str) -> dict:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base_url}/api/v1/agents/{agent_id}/nearby", headers=await self._headers())
            resp.raise_for_status()
            return resp.json()


minecraft_client = MinecraftApiClient()
