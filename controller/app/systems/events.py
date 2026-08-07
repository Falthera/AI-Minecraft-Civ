import uuid
from datetime import datetime
from typing import List, Optional
from ..config import settings


class Event:
    def __init__(self, experiment_id: str, event_type: str, source_type: str, source_id: Optional[str], data: dict):
        self.id: str = str(uuid.uuid4())
        self.experiment_id: str = experiment_id
        self.event_type: str = event_type
        self.source_type: str = source_type
        self.source_id: Optional[str] = source_id
        self.data: dict = data
        self.timestamp: datetime = datetime.utcnow()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "event_type": self.event_type,
            "source_type": self.source_type,
            "source_id": self.source_id,
            "data": self.data,
            "timestamp": self.timestamp.isoformat(),
        }


class EventSystem:
    def __init__(self):
        self._subscribers: List[callable] = []

    def subscribe(self, callback: callable):
        self._subscribers.append(callback)

    async def publish(self, event: Event):
        # In production: persist to PostgreSQL and notify subscribers.
        for cb in self._subscribers:
            try:
                await cb(event)
            except Exception:
                pass

    async def minecraft_event(self, experiment_id: str, event_type: str, source_id: Optional[str], data: dict):
        event = Event(experiment_id=experiment_id, event_type=event_type, source_type="minecraft", source_id=source_id, data=data)
        await self.publish(event)

    async def civilization_event(self, experiment_id: str, event_type: str, source_id: Optional[str], data: dict):
        event = Event(experiment_id=experiment_id, event_type=event_type, source_type="civilization", source_id=source_id, data=data)
        await self.publish(event)


event_system = EventSystem()
