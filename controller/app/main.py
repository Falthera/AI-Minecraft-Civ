from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Literal
import uuid
import time

from .config import settings

app = FastAPI(title="AI Controller", version="1.0.0")


class AgentCreateRequest(BaseModel):
    username: str
    personality: dict = Field(default_factory=dict)


class AgentResponse(BaseModel):
    id: str
    username: str
    uuid: str
    life_state: str
    civilization_id: Optional[str] = None
    settlement_id: Optional[str] = None


class ActionRequest(BaseModel):
    agent_id: str
    action: Literal[
        "MOVE", "NAVIGATE", "MINE", "CHOP", "FARM", "CRAFT", "SMELT",
        "BUILD", "FIGHT", "EXPLORE", "TRADE", "EQUIP", "EAT", "STORE",
        "RETRIEVE", "INTERACT", "COMMUNICATE"
    ]
    target: Optional[str] = None
    params: dict = Field(default_factory=dict)


async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/ready")
async def ready():
    return {"status": "ready"}


@app.post("/agents", response_model=AgentResponse)
async def create_agent(request: AgentCreateRequest, api_key: str = Depends(verify_api_key)):
    agent_id = str(uuid.uuid4())
    agent_uuid = str(uuid.uuid4())
    # In production, persist to PostgreSQL here.
    return AgentResponse(
        id=agent_id,
        username=request.username,
        uuid=agent_uuid,
        life_state="ACTIVE",
    )


@app.get("/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str, api_key: str = Depends(verify_api_key)):
    # Placeholder: fetch from DB.
    return AgentResponse(id=agent_id, username="unknown", uuid="00000000-0000-0000-0000-000000000000", life_state="ACTIVE")


@app.post("/actions")
async def execute_action(request: ActionRequest, api_key: str = Depends(verify_api_key)):
    # Placeholder: validate agent is not DEAD, then forward to Minecraft plugin or bot runtime.
    if request.action not in [
        "MOVE", "NAVIGATE", "MINE", "CHOP", "FARM", "CRAFT", "SMELT",
        "BUILD", "FIGHT", "EXPLORE", "TRADE", "EQUIP", "EAT", "STORE",
        "RETRIEVE", "INTERACT", "COMMUNICATE"
    ]:
        raise HTTPException(status_code=400, detail="Invalid action")
    return {"request_id": str(uuid.uuid4()), "status": "queued"}


@app.get("/experiments/{experiment_id}/status")
async def experiment_status(experiment_id: str, api_key: str = Depends(verify_api_key)):
    return {"experiment_id": experiment_id, "state": "RUNNING", "living_agents": 0, "dead_agents": 0}


@app.get("/admin/metrics")
async def admin_metrics(api_key: str = Depends(verify_api_key)):
    return {
        "living_agents": 0,
        "dead_agents": 0,
        "ai_queue_length": 0,
        "minecraft_tps": 20.0,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)
