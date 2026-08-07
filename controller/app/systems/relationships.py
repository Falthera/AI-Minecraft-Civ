import uuid
from datetime import datetime
from typing import List, Optional
from ..agent.manager import Agent, agent_manager


class Relationship:
    def __init__(self, experiment_id: str, agent_a: str, agent_b: str, relationship_type: str, score: float = 0.0):
        self.id: str = str(uuid.uuid4())
        self.experiment_id: str = experiment_id
        self.agent_a: str = agent_a
        self.agent_b: str = agent_b
        self.relationship_type: str = relationship_type
        self.score: float = max(-1.0, min(1.0, score))
        self.metadata: dict = {}
        self.created_at: datetime = datetime.utcnow()
        self.updated_at: datetime = datetime.utcnow()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "agent_a": self.agent_a,
            "agent_b": self.agent_b,
            "relationship_type": self.relationship_type,
            "score": self.score,
        }


class RelationshipSystem:
    async def set_relationship(self, experiment_id: str, agent_a: str, agent_b: str, rel_type: str, score: float) -> Relationship:
        rel = Relationship(experiment_id=experiment_id, agent_a=agent_a, agent_b=agent_b, relationship_type=rel_type, score=score)
        # In production: upsert into PostgreSQL.
        return rel

    async def get_relationships(self, agent_id: str) -> List[Relationship]:
        return []

    async def update_score(self, relationship_id: str, delta: float) -> Optional[Relationship]:
        return None


relationship_system = RelationshipSystem()
