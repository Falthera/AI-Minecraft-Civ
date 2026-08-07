import uuid
from datetime import datetime
from typing import List, Optional
from ..agent.manager import Agent, agent_manager


class TerritoryClaim:
    def __init__(self, experiment_id: str, civilization_id: str, chunk_x: int, chunk_z: int, dimension: str = "overworld"):
        self.id: str = str(uuid.uuid4())
        self.experiment_id: str = experiment_id
        self.civilization_id: str = civilization_id
        self.chunk_x: int = chunk_x
        self.chunk_z: int = chunk_z
        self.dimension: str = dimension
        self.claimed_at: datetime = datetime.utcnow()
        self.contested_at: Optional[datetime] = None
        self.captured_at: Optional[datetime] = None


class TerritorySystem:
    async def claim(self, experiment_id: str, civilization_id: str, chunk_x: int, chunk_z: int, dimension: str = "overworld") -> TerritoryClaim:
        claim = TerritoryClaim(experiment_id=experiment_id, civilization_id=civilization_id, chunk_x=chunk_x, chunk_z=chunk_z, dimension=dimension)
        # In production: persist to PostgreSQL.
        return claim

    async def unclaim(self, claim_id: str):
        pass

    async def contest(self, claim_id: str):
        pass

    async def capture(self, claim_id: str, new_civilization_id: str):
        pass

    async def get_claims_for_civilization(self, civilization_id: str) -> List[TerritoryClaim]:
        return []


territory_system = TerritorySystem()
