import uuid
from datetime import datetime
from typing import List, Optional
from .civilizations import CivilizationSystem
from .territory import TerritorySystem


class War:
    def __init__(self, experiment_id: str, attacker_civ_id: str, defender_civ_id: str):
        self.id: str = str(uuid.uuid4())
        self.experiment_id: str = experiment_id
        self.attacker_civilization_id: str = attacker_civ_id
        self.defender_civilization_id: str = defender_civ_id
        self.territory_objectives: list = []
        self.status: str = "ACTIVE"
        self.started_at: datetime = datetime.utcnow()
        self.ended_at: Optional[datetime] = None
        self.peace_treaty: Optional[dict] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "attacker_civilization_id": self.attacker_civilization_id,
            "defender_civilization_id": self.defender_civilization_id,
            "status": self.status,
        }


class WarSystem:
    def __init__(self):
        self.civilization_system = CivilizationSystem()
        self.territory_system = TerritorySystem()

    async def declare_war(self, experiment_id: str, attacker_civ_id: str, defender_civ_id: str, objectives: list) -> War:
        war = War(experiment_id=experiment_id, attacker_civ_id=attacker_civ_id, defender_civ_id=defender_civ_id)
        war.territory_objectives = objectives
        # In production: persist to PostgreSQL.
        return war

    async def end_war(self, war_id: str, treaty: Optional[dict] = None):
        pass

    async def get_active_wars(self, experiment_id: str) -> List[War]:
        return []


war_system = WarSystem()
