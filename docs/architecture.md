# AI Civilization — Architecture

## Overview

This document describes the complete software infrastructure for the AI Civilization experiment.

The system consists of four isolated services communicating over a private network:

```text
PTERODACTYL NODE
│
├── SERVER 1 — MINECRAFT
│   ├── Paper 1.21.11
│   ├── AI Civilization Plugin
│   ├── Persistent World
│   └── Real AI Minecraft clients connect here
│
├── SERVER 2 — AI CONTROLLER
│   ├── Agent Manager
│   ├── 10,000-Agent State Architecture
│   ├── Scheduler
│   ├── Goal System
│   ├── Skill System
│   ├── Memory System
│   ├── Relationship System
│   ├── Civilization System
│   ├── Settlement System
│   ├── Territory System
│   ├── Political System
│   ├── Government System
│   ├── Economy
│   ├── Military
│   ├── War
│   ├── Event System
│   └── Minecraft API Client
│
├── SERVER 3 — AI INFERENCE
│   ├── Model Router
│   ├── Fast Model
│   ├── Main Model
│   ├── Inference Queue
│   ├── Context Builder
│   └── Local Inference API
│
└── SERVER 4 — DATABASE
    └── PostgreSQL
```

## Design Principles

1. **Separation of concerns**: Each service has one responsibility.
2. **Real clients**: AI players are real Minecraft clients, not server-side entities.
3. **Local inference**: No external AI API dependency.
4. **Persistence**: All state is durable in PostgreSQL.
5. **Hardcore**: Death is permanent. No resurrection.
6. **Event-driven**: Agent decisions are triggered by events, not tick-based polling.
7. **Scalable**: Designed for 10,000 agents from day one.
8. **Secure**: All internal APIs are authenticated.

## Service Responsibilities

### Minecraft Server (Server 1)
- Runs Paper 1.21.11 with the AI Civilization plugin.
- Manages the physical Minecraft world.
- Receives connections from real Minecraft client bots.
- Validates agent actions server-side.
- Publishes Minecraft events to the AI Controller.
- Exposes an authenticated REST/WebSocket API for the AI Controller.

### AI Controller (Server 2)
- Manages persistent agent state for up to 10,000 agents.
- Runs the scheduler, goals, needs, skills, memory, relationships, civilizations, settlements, territory, politics, economy, military, war, and event systems.
- Communicates with the Minecraft plugin to observe world state and execute actions.
- Requests AI decisions from the Inference service.
- Never performs LLM inference itself.

### AI Inference (Server 3)
- Loads and serves local LLM models.
- Routes requests between Fast and Main model tiers.
- Queues inference requests with priority and backpressure.
- Returns structured AI output.
- Provides embedding generation for memory retrieval.

### PostgreSQL (Server 4)
- Stores all persistent experiment state.
- Agents, civilizations, settlements, territories, wars, events, etc.
- Provides efficient querying for the AI Controller.

## Communication

```text
Minecraft Plugin ──(REST/WS)──► AI Controller
AI Controller   ──(REST)───────► AI Inference
AI Controller   ──(SQL)─────────► PostgreSQL
```

All internal communication requires API key authentication.

## Data Flow

1. A Minecraft client bot connects to the Paper server.
2. The Paper plugin detects the connection and notifies the AI Controller.
3. The AI Controller creates/loads the agent state in PostgreSQL.
4. The agent's scheduler determines when a decision is needed.
5. The AI Controller builds a context and sends it to the Inference service.
6. The Inference service returns a structured decision.
7. The AI Controller translates the decision into a high-level action.
8. The AI Controller sends the action to the Minecraft plugin.
9. The Minecraft plugin validates and executes the action on the real client bot.
10. Minecraft publishes resulting events back to the AI Controller.
11. The AI Controller updates agent state and persists changes.

## Failure Recovery

- PostgreSQL: durable transactions, WAL archiving.
- AI Inference: stateless, restartable.
- AI Controller: state in PostgreSQL, recovers on restart.
- Minecraft: world persistence, plugin state recovery on restart.

## Security

- All internal APIs use static API keys from environment variables.
- PostgreSQL is not exposed publicly.
- Inference service is not exposed publicly.
- AI Controller admin API is not exposed publicly.
- Only Minecraft server ports are public.
- All AI output is validated before execution.
