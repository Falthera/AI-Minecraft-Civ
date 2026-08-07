import uuid
from datetime import datetime
from typing import List, Optional
from ..agent.manager import Agent, agent_manager


class Memory:
    def __init__(self, agent_id: str, category: str, content: dict, importance: float = 0.5):
        self.id: str = str(uuid.uuid4())
        self.agent_id: str = agent_id
        self.category: str = category
        self.content: dict = content
        self.importance: float = max(0.0, min(1.0, importance))
        self.embedding: Optional[List[float]] = None
        self.created_at: datetime = datetime.utcnow()
        self.last_accessed: datetime = datetime.utcnow()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "category": self.category,
            "content": self.content,
            "importance": self.importance,
        }


class MemorySystem:
    async def create_memory(self, agent_id: str, category: str, content: dict, importance: float = 0.5) -> Memory:
        # In production: persist to PostgreSQL with embedding.
        memory = Memory(agent_id=agent_id, category=category, content=content, importance=importance)
        return memory

    async def get_recent(self, agent_id: str, limit: int = 20) -> List[Memory]:
        return []

    async def get_by_category(self, agent_id: str, category: str) -> List[Memory]:
        return []

    async def summarize(self, agent_id: str) -> str:
        return "No memories yet."


memory_system = MemorySystem()
