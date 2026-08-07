from typing import Dict, List, Optional
import asyncio
import uuid
from datetime import datetime
from ..config import settings


class Agent:
    def __init__(self, username: str, personality: Optional[dict] = None):
        self.id: str = str(uuid.uuid4())
        self.username: str = username
        self.uuid: str = str(uuid.uuid4())
        self.personality: dict = personality or {}
        self.skills: list = []
        self.needs: dict = {}
        self.goals: list = []
        self.current_action: Optional[str] = None
        self.occupation: Optional[str] = None
        self.civilization_id: Optional[str] = None
        self.settlement_id: Optional[str] = None
        self.political_position: Optional[str] = None
        self.wealth: float = 0.0
        self.reputation: float = 0.0
        self.knowledge: list = []
        self.life_state: str = "ACTIVE"
        self.created_at: datetime = datetime.utcnow()
        self.updated_at: datetime = datetime.utcnow()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "uuid": self.uuid,
            "life_state": self.life_state,
            "civilization_id": self.civilization_id,
            "settlement_id": self.settlement_id,
            "wealth": self.wealth,
            "reputation": self.reputation,
        }


class AgentManager:
    def __init__(self):
        self._agents: Dict[str, Agent] = {}
        self._lock = asyncio.Lock()

    async def create_agent(self, username: str, personality: Optional[dict] = None) -> Agent:
        async with self._lock:
            agent = Agent(username=username, personality=personality)
            self._agents[agent.id] = agent
            # In production: persist to PostgreSQL here.
            return agent

    async def get_agent(self, agent_id: str) -> Optional[Agent]:
        return self._agents.get(agent_id)

    async def get_agents_by_state(self, life_state: str) -> List[Agent]:
        return [a for a in self._agents.values() if a.life_state == life_state]

    async def mark_dead(self, agent_id: str, death_data: Optional[dict] = None) -> bool:
        agent = self._agents.get(agent_id)
        if not agent or agent.life_state == "DEAD":
            return False
        agent.life_state = "DEAD"
        agent.updated_at = datetime.utcnow()
        # In production: persist death record to PostgreSQL here.
        return True

    async def living_count(self) -> int:
        return sum(1 for a in self._agents.values() if a.life_state == "ACTIVE")

    async def dead_count(self) -> int:
        return sum(1 for a in self._agents.values() if a.life_state == "DEAD")


agent_manager = AgentManager()
