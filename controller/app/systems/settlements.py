import uuid
from datetime import datetime
from typing import List, Optional
from ..agent.manager import Agent, agent_manager


class Settlement:
    def __init__(self, experiment_id: str, name: str, founder_id: str, center: dict):
        self.id: str = str(uuid.uuid4())
        self.experiment_id: str = experiment_id
        self.name: str = name
        self.founder_id: str = founder_id
        self.population: int = 1
        self.center: dict = center
        self.territory: dict = {}
        self.buildings: list = []
        self.resources: dict = {}
        self.leader_id: Optional[str] = founder_id
        self.members: list = [founder_id]
        self.history: list = []
        self.created_at: datetime = datetime.utcnow()
        self.abandoned_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "leader_id": self.leader_id,
        }


class SettlementSystem:
    async def create_settlement(self, experiment_id: str, name: str, founder_id: str, center: dict) -> Settlement:
        settlement = Settlement(experiment_id=experiment_id, name=name, founder_id=founder_id, center=center)
        # In production: persist to PostgreSQL.
        return settlement

    async def get_settlement(self, settlement_id: str) -> Optional[Settlement]:
        return None

    async def add_member(self, settlement_id: str, agent_id: str):
        pass

    async def remove_member(self, settlement_id: str, agent_id: str):
        pass


settlement_system = SettlementSystem()
