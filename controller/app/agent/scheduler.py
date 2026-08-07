import asyncio
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime, timedelta
from .manager import Agent, agent_manager
from ..config import settings


class ScheduledTask:
    def __init__(self, agent_id: str, run_at: datetime, priority: float, callback: Callable):
        self.agent_id = agent_id
        self.run_at = run_at
        self.priority = priority
        self.callback = callback
        self.cancelled = False

    def __lt__(self, other):
        if self.run_at != other.run_at:
            return self.run_at < other.run_at
        return self.priority > other.priority


class Scheduler:
    def __init__(self):
        self._queue: List[ScheduledTask] = []
        self._lock = asyncio.Lock()
        self._running = False
        self._task = None

    async def start(self):
        if self._running:
            return
        self._running = True
        self._task = asyncio.create_task(self._run_loop())

    async def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    async def _run_loop(self):
        while self._running:
            now = datetime.utcnow()
            async with self._lock:
                ready = [t for t in self._queue if not t.cancelled and t.run_at <= now]
                if ready:
                    ready.sort()
                    for task in ready:
                        self._queue.remove(task)
                        asyncio.create_task(self._execute(task))
            await asyncio.sleep(settings.scheduler_tick_seconds)

    async def _execute(self, task: ScheduledTask):
        if task.cancelled:
            return
        agent = await agent_manager.get_agent(task.agent_id)
        if not agent or agent.life_state != "ACTIVE":
            return
        try:
            await task.callback(agent)
        except Exception:
            pass

    async def schedule(self, agent_id: str, delay_seconds: float, priority: float, callback: Callable):
        run_at = datetime.utcnow() + timedelta(seconds=delay_seconds)
        task = ScheduledTask(agent_id=agent_id, run_at=run_at, priority=priority, callback=callback)
        async with self._lock:
            self._queue.append(task)
            self._queue.sort()

    async def cancel_for_agent(self, agent_id: str):
        async with self._lock:
            for task in self._queue:
                if task.agent_id == agent_id:
                    task.cancelled = True


scheduler = Scheduler()
