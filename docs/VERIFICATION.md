# Verification Guide

## Phase 1 — Inspect

```bash
# Verify repository structure
find . -type f -name "*.py" -o -name "*.java" -o -name "*.ts" -o -name "*.sql" -o -name "*.md" -o -name "*.yml" -o -name "*.json" | sort

# Verify no secrets are committed
grep -r "changeme" --include="*.py" --include="*.java" --include="*.ts" --include="*.yml" --include="*.json" --include="*.env*" .

# Verify gitignore exists
cat .gitignore
```

## Phase 2 — Architecture

```bash
# Verify architecture documentation exists
cat docs/architecture.md
```

## Phase 3 — Database

```bash
# Start PostgreSQL
docker run -d --name ai-civ-postgres -e POSTGRES_USER=ai_civilization -e POSTGRES_PASSWORD=changeme -e POSTGRES_DB=ai_civilization -p 5432:5432 postgres:16-alpine

# Run migrations
python database/migrate.py

# Verify tables
docker exec -it ai-civ-postgres psql -U ai_civilization -d ai_civilization -c "\dt"

# Expected tables:
# experiments, agents, agent_state_history, deaths, memories, relationships,
# civilizations, settlements, territory_claims, political_positions, laws,
# economies, wars, alliances, events, statistics, world_exhaustion
```

## Phase 4 — AI Inference

```bash
# Install dependencies
pip install -r inference/requirements.txt

# Start service
uvicorn inference.app.main:app --host 0.0.0.0 --port 8001

# Test health
curl http://localhost:8001/health

# Load models (simulated)
curl -X POST http://localhost:8001/admin/load-models -H "X-API-Key: changeme"

# Test decision endpoint
curl -X POST http://localhost:8001/v1/decision \
  -H "X-API-Key: changeme" \
  -H "Content-Type: application/json" \
  -d '{"tier":"fast","prompt":"test","context":{"agent_uuid":"123"}}'
```

## Phase 5 — AI Controller

```bash
# Install dependencies
pip install -r controller/requirements.txt

# Start service (requires PostgreSQL and Inference running)
uvicorn controller.app.main:app --host 0.0.0.0 --port 8000

# Test health
curl http://localhost:8000/health

# Create agent
curl -X POST http://localhost:8000/agents \
  -H "X-API-Key: changeme" \
  -H "Content-Type: application/json" \
  -d '{"username":"TestBot","personality":{"aggression":0.5}}'

# Test authentication rejection
curl http://localhost:8000/agents
```

## Phase 6 — Minecraft Plugin

```bash
# Build plugin
cd minecraft/plugin
mvn clean package

# Verify jar exists
ls target/*.jar

# Copy to Paper server plugins folder and start
```

## Phase 7 — Client Bots

```bash
# Install dependencies
cd minecraft/client-bots
npm install

# Build
npm run build

# Start 1 test bot
BOT_COUNT=1 npm start

# Verify bot connects to Minecraft server
```

## Phase 8 — Integration

```bash
# Start all services with docker-compose
docker compose -f deployment/docker/docker-compose.yml up

# Verify all services healthy
curl http://localhost:8000/health
curl http://localhost:8001/health

# Verify Minecraft accepts connections
mcstatus localhost:25565
```

## Phase 9 — Hardcore

```bash
# Run hardcore acceptance test
pytest tests/ -v

# Verify:
# - Agent created and connected
# - Agent dies
# - Death persisted
# - Agent cannot reconnect
# - Restart recovery keeps agent dead
```

## Phase 10 — Scale

```bash
# Run load tests
pytest tests/ -v --timeout=300

# Benchmark report should include:
# - TPS
# - MSPT
# - AI queue length
# - Database latency
# - Events/sec
```

## Continuous Verification

```bash
# Run all tests
pytest tests/ -v

# Run lint
ruff check controller/ inference/
npm run lint -- minecraft/client-bots/
mvn compile minecraft/plugin/
```
