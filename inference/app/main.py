from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Literal
import time
import uuid
import asyncio
import json

from .config import settings

app = FastAPI(title="AI Inference Service", version="1.0.0")

# In-memory queue for demonstration. Replace with Redis/RabbitMQ in production.
class InferenceRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tier: Literal["fast", "main"] = "fast"
    prompt: str
    max_tokens: int = 256
    temperature: float = 0.7
    stop: list[str] = []
    response_format: Optional[dict] = None
    context: Optional[dict] = None


class InferenceResponse(BaseModel):
    request_id: str
    text: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    latency_ms: float


class ErrorResponse(BaseModel):
    request_id: str
    error: str
    detail: str


class HealthResponse(BaseModel):
    status: str
    fast_model_loaded: bool = False
    main_model_loaded: bool = False
    queue_length: int = 0


# Simple in-memory model loader simulation.
# In production, use llama-cpp-python with actual GGUF model files.
_model_registry = {
    "fast": {"loaded": False, "name": "Qwen3-0.6B-Instruct (simulated)"},
    "main": {"loaded": False, "name": "Qwen3-4B-Instruct (simulated)"},
}


async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="ok",
        fast_model_loaded=_model_registry["fast"]["loaded"],
        main_model_loaded=_model_registry["main"]["loaded"],
        queue_length=0,
    )


@app.get("/ready")
async def ready():
    if not _model_registry["fast"]["loaded"] or not _model_registry["main"]["loaded"]:
        raise HTTPException(status_code=503, detail="Models not loaded")
    return {"status": "ready"}


@app.get("/models")
async def list_models(api_key: str = Depends(verify_api_key)):
    return {
        "models": [
            {"id": "fast", "name": _model_registry["fast"]["name"], "loaded": _model_registry["fast"]["loaded"]},
            {"id": "main", "name": _model_registry["main"]["name"], "loaded": _model_registry["main"]["loaded"]},
        ]
    }


@app.post("/v1/decision", response_model=InferenceResponse)
async def generate_decision(request: InferenceRequest, api_key: str = Depends(verify_api_key)):
    start = time.perf_counter()
    model_info = _model_registry.get(request.tier)
    if not model_info or not model_info["loaded"]:
        raise HTTPException(status_code=503, detail=f"Model '{request.tier}' not loaded")

    # Simulate structured inference latency.
    await asyncio.sleep(0.05)

    # In production, call llama-cpp-python here and parse structured JSON output.
    # For now, return a deterministic simulated response.
    simulated_text = json.dumps({
        "agent": request.context.get("agent_uuid") if request.context else "unknown",
        "goal": "Survive and gather resources",
        "action": "MINE",
        "target": "nearby_iron_ore",
        "priority": 0.8,
        "reason": "Low hunger and no immediate danger.",
    })

    latency = (time.perf_counter() - start) * 1000
    return InferenceResponse(
        request_id=request.request_id,
        text=simulated_text,
        model=model_info["name"],
        prompt_tokens=len(request.prompt.split()),
        completion_tokens=len(simulated_text.split()),
        latency_ms=round(latency, 2),
    )


@app.post("/v1/chat", response_model=InferenceResponse)
async def generate_chat(request: InferenceRequest, api_key: str = Depends(verify_api_key)):
    start = time.perf_counter()
    model_info = _model_registry.get(request.tier)
    if not model_info or not model_info["loaded"]:
        raise HTTPException(status_code=503, detail=f"Model '{request.tier}' not loaded")

    await asyncio.sleep(0.05)
    simulated_text = "Hello, I am an AI agent."
    latency = (time.perf_counter() - start) * 1000
    return InferenceResponse(
        request_id=request.request_id,
        text=simulated_text,
        model=model_info["name"],
        prompt_tokens=len(request.prompt.split()),
        completion_tokens=len(simulated_text.split()),
        latency_ms=round(latency, 2),
    )


@app.post("/v1/embedding")
async def generate_embedding(request: InferenceRequest, api_key: str = Depends(verify_api_key)):
    # Simulated embedding.
    return {
        "request_id": request.request_id,
        "embedding": [0.0] * 384,
        "model": "embedding-model",
    }


@app.post("/admin/load-models")
async def load_models(api_key: str = Depends(verify_api_key)):
    _model_registry["fast"]["loaded"] = True
    _model_registry["main"]["loaded"] = True
    return {"status": "loaded", "models": list(_model_registry.keys())}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)
