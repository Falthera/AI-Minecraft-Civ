# AI Civilization — Large-Scale Autonomous Minecraft Experiment

A complete software infrastructure for running 1,000 (scalable to 10,000) real AI-controlled Minecraft players in a hardcore persistent world experiment.

## Architecture

```text
PTERODACTYL NODE
├── SERVER 1 — MINECRAFT (Paper 1.21.11 + Plugin)
├── SERVER 2 — AI CONTROLLER (Agent Management, Scheduler, Systems)
├── SERVER 3 — AI INFERENCE (Local LLM Serving)
└── SERVER 4 — DATABASE (PostgreSQL)
```

## Key Features

- **Real Minecraft Clients**: AI players connect as genuine Minecraft clients, not NPCs.
- **Hardcore Mode**: One life per agent. Death is permanent. No respawn.
- **Emergent Civilization**: Agents form settlements, governments, economies, and wars organically.
- **Local AI**: All inference runs locally on CPU (llama.cpp/Ollama).
- **Scalable**: Designed for 10,000 persistent agents.
- **Event-Driven**: Agent decisions triggered by events, not polling.
- **Persistent State**: PostgreSQL stores all agent and civilization state.

## Quick Start

See [docs/architecture.md](docs/architecture.md) for the full system design.

## Development Phases

1. **Database** — PostgreSQL schema and migrations
2. **Inference** — Local LLM service with model routing
3. **Controller** — Core agent management and simulation systems
4. **Plugin** — Paper plugin for Minecraft integration
5. **Client Bots** — Real Minecraft client runtime
6. **Deployment** — Docker and Pterodactyl configuration
7. **Integration** — End-to-end testing
8. **Hardcore** — Permanent death verification
9. **Scale** — Load testing to 1,000 agents

## License

MIT
