import uuid
from datetime import datetime
from typing import List, Optional
from ..agent.manager import Agent, agent_manager


class Civilization:
    def __init__(self, experiment_id: str, name: str):
        self.id: str = str(uuid.uuid4())
        self.experiment_id: str = experiment_id
        self.name: str = name
        self.government_type: Optional[str] = None
        self.leader_id: Optional[str] = None
        self.territory_center: Optional[dict] = None
        self.created_at: datetime = datetime.utcnow()
        self.dissolved_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "government_type": self.government_type,
            "leader_id": self.leader_id,
        }


class CivilizationSystem:
    async def create_civilization(self, experiment_id: str, name: str, founder_id: str) -> Civilization:
        civ = Civilization(experiment_id=experiment_id, name=name)
        civ.leader_id = founder_id
        # In production: persist to PostgreSQL.
        return civ

    async def get_civilization(self, civilization_id: str) -> Optional[Civilization]:
        return None

    async def dissolve(self, civilization_id: str):
        pass

    async def list_civilizations(self, experiment_id: str) -> List[Civilization]:
        return []


civilization_system = CivilizationSystem()
