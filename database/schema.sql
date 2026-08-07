-- ============================================================
-- AI Civilization — PostgreSQL Schema
-- ============================================================

-- Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================
-- Experiments
-- ============================================================
CREATE TABLE experiments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    experiment_id VARCHAR(64) UNIQUE NOT NULL,
    world_seed BIGINT NOT NULL,
    start_timestamp TIMESTAMPTZ NOT NULL DEFAULT now(),
    end_timestamp TIMESTAMPTZ,
    initial_population INTEGER NOT NULL,
    current_state VARCHAR(32) NOT NULL DEFAULT 'START', -- START, PAUSED, RUNNING, STOPPED, COMPLETED
    completion_state JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_experiments_state ON experiments(current_state);

-- ============================================================
-- Agents
-- ============================================================
CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    experiment_id UUID NOT NULL REFERENCES experiments(id) ON DELETE CASCADE,
    username VARCHAR(64) UNIQUE NOT NULL,
    uuid VARCHAR(36) UNIQUE NOT NULL,
    personality JSONB NOT NULL DEFAULT '{}',
    skills JSONB NOT NULL DEFAULT '[]',
    needs JSONB NOT NULL DEFAULT '{}',
    goals JSONB NOT NULL DEFAULT '[]',
    current_action VARCHAR(128),
    occupation VARCHAR(128),
    civilization_id UUID,
    settlement_id UUID,
    political_position VARCHAR(128),
    wealth NUMERIC(20,2) NOT NULL DEFAULT 0,
    reputation NUMERIC(10,2) NOT NULL DEFAULT 0,
    knowledge JSONB NOT NULL DEFAULT '[]',
    life_state VARCHAR(16) NOT NULL DEFAULT 'ACTIVE', -- ACTIVE, OFFLINE, DEAD
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_agents_experiment ON agents(experiment_id);
CREATE INDEX idx_agents_life_state ON agents(life_state);
CREATE INDEX idx_agents_settlement ON agents(settlement_id);
CREATE INDEX idx_agents_civilization ON agents(civilization_id);

-- ============================================================
-- Agent State History
-- ============================================================
CREATE TABLE agent_state_history (
    id BIGSERIAL PRIMARY KEY,
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    state JSONB NOT NULL,
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_agent_state_history_agent ON agent_state_history(agent_id, recorded_at DESC);

-- ============================================================
-- Deaths
-- ============================================================
CREATE TABLE deaths (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    experiment_id UUID NOT NULL REFERENCES experiments(id) ON DELETE CASCADE,
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    death_timestamp TIMESTAMPTZ NOT NULL DEFAULT now(),
    death_location JSONB,
    dimension VARCHAR(64),
    cause VARCHAR(128),
    killer VARCHAR(256),
    civilization_id UUID,
    settlement_id UUID,
    political_position VARCHAR(128),
    inventory_snapshot JSONB,
    equipment JSONB,
    historical_events JSONB
);

CREATE INDEX idx_deaths_experiment ON deaths(experiment_id);
CREATE INDEX idx_deaths_agent ON deaths(agent_id);

-- ============================================================
-- Memories
-- ============================================================
CREATE TABLE memories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    category VARCHAR(32) NOT NULL, -- people, places, events, conversations, discoveries, betrayals, promises, wars, deaths, trades
    content JSONB NOT NULL,
    importance NUMERIC(5,4) NOT NULL DEFAULT 0.5,
    embedding VECTOR(384),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_accessed TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_memories_agent ON memories(agent_id);
CREATE INDEX idx_memories_category ON memories(agent_id, category);
CREATE INDEX idx_memories_importance ON memories(agent_id, importance DESC);
CREATE INDEX idx_memories_embedding ON memories USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- ============================================================
-- Relationships
-- ============================================================
CREATE TABLE relationships (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    experiment_id UUID NOT NULL REFERENCES experiments(id) ON DELETE CASCADE,
    agent_a UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    agent_b UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    relationship_type VARCHAR(32) NOT NULL, -- friendship, trust, respect, fear, hatred, loyalty, rivalry, debt
    score NUMERIC(5,4) NOT NULL DEFAULT 0,
    metadata JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(agent_a, agent_b, relationship_type)
);

CREATE INDEX idx_relationships_experiment ON relationships(experiment_id);
CREATE INDEX idx_relationships_agent_a ON relationships(agent_a);
CREATE INDEX idx_relationships_agent_b ON relationships(agent_b);

-- ============================================================
-- Civilizations
-- ============================================================
CREATE TABLE civilizations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    experiment_id UUID NOT NULL REFERENCES experiments(id) ON DELETE CASCADE,
    name VARCHAR(128) UNIQUE NOT NULL,
    government_type VARCHAR(64), -- tribe, chiefdom, monarchy, council, republic, democracy, dictatorship, military
    leader_id UUID REFERENCES agents(id),
    territory_center JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    dissolved_at TIMESTAMPTZ
);

CREATE INDEX idx_civilizations_experiment ON civilizations(experiment_id);
CREATE INDEX idx_civilizations_leader ON civilizations(leader_id);

-- ============================================================
-- Settlements
-- ============================================================
CREATE TABLE settlements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    experiment_id UUID NOT NULL REFERENCES experiments(id) ON DELETE CASCADE,
    civilization_id UUID REFERENCES civilizations(id) ON DELETE SET NULL,
    name VARCHAR(128) NOT NULL,
    founder_id UUID REFERENCES agents(id),
    population INTEGER NOT NULL DEFAULT 0,
    center JSONB NOT NULL,
    territory JSONB NOT NULL DEFAULT '{}',
    buildings JSONB NOT NULL DEFAULT '[]',
    resources JSONB NOT NULL DEFAULT '{}',
    leader_id UUID REFERENCES agents(id),
    members JSONB NOT NULL DEFAULT '[]',
    history JSONB NOT NULL DEFAULT '[]',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    abandoned_at TIMESTAMPTZ
);

CREATE INDEX idx_settlements_experiment ON settlements(experiment_id);
CREATE INDEX idx_settlements_civilization ON settlements(civilization_id);

-- ============================================================
-- Territory Claims
-- ============================================================
CREATE TABLE territory_claims (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    experiment_id UUID NOT NULL REFERENCES experiments(id) ON DELETE CASCADE,
    civilization_id UUID NOT NULL REFERENCES civilizations(id) ON DELETE CASCADE,
    chunk_x INTEGER NOT NULL,
    chunk_z INTEGER NOT NULL,
    dimension VARCHAR(64) NOT NULL DEFAULT 'overworld',
    claimed_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    contested_at TIMESTAMPTZ,
    captured_at TIMESTAMPTZ,
    UNIQUE(experiment_id, chunk_x, chunk_z, dimension)
);

CREATE INDEX idx_territory_claims_civilization ON territory_claims(civilization_id);
CREATE INDEX idx_territory_claims_coords ON territory_claims(chunk_x, chunk_z, dimension);

-- ============================================================
-- Political Positions
-- ============================================================
CREATE TABLE political_positions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    experiment_id UUID NOT NULL REFERENCES experiments(id) ON DELETE CASCADE,
    civilization_id UUID NOT NULL REFERENCES civilizations(id) ON DELETE CASCADE,
    settlement_id UUID REFERENCES settlements(id) ON DELETE CASCADE,
    title VARCHAR(128) NOT NULL,
    agent_id UUID REFERENCES agents(id),
    assigned_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    ended_at TIMESTAMPTZ
);

CREATE INDEX idx_political_positions_experiment ON political_positions(experiment_id);
CREATE INDEX idx_political_positions_agent ON political_positions(agent_id);

-- ============================================================
-- Laws
-- ============================================================
CREATE TABLE laws (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    experiment_id UUID NOT NULL REFERENCES experiments(id) ON DELETE CASCADE,
    civilization_id UUID NOT NULL REFERENCES civilizations(id) ON DELETE CASCADE,
    title VARCHAR(256) NOT NULL,
    description TEXT NOT NULL,
    enacted_by UUID REFERENCES agents(id),
    enacted_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    repealed_at TIMESTAMPTZ
);

CREATE INDEX idx_laws_civilization ON laws(civilization_id);

-- ============================================================
-- Economy
-- ============================================================
CREATE TABLE economies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    experiment_id UUID NOT NULL REFERENCES experiments(id) ON DELETE CASCADE,
    civilization_id UUID NOT NULL REFERENCES civilizations(id) ON DELETE CASCADE,
    currency_name VARCHAR(64),
    treasury JSONB NOT NULL DEFAULT '{}',
    tax_rate NUMERIC(5,4) NOT NULL DEFAULT 0,
    trade_routes JSONB NOT NULL DEFAULT '[]',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_economies_civilization ON economies(civilization_id);

-- ============================================================
-- Wars
-- ============================================================
CREATE TABLE wars (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    experiment_id UUID NOT NULL REFERENCES experiments(id) ON DELETE CASCADE,
    attacker_civilization_id UUID NOT NULL REFERENCES civilizations(id),
    defender_civilization_id UUID NOT NULL REFERENCES civilizations(id),
    territory_objectives JSONB NOT NULL DEFAULT '[]',
    status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE', -- ACTIVE, ENDED
    started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    ended_at TIMESTAMPTZ,
    peace_treaty JSONB
);

CREATE INDEX idx_wars_experiment ON wars(experiment_id);
CREATE INDEX idx_wars_attacker ON wars(attacker_civilization_id);
CREATE INDEX idx_wars_defender ON wars(defender_civilization_id);

-- ============================================================
-- Alliances
-- ============================================================
CREATE TABLE alliances (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    experiment_id UUID NOT NULL REFERENCES experiments(id) ON DELETE CASCADE,
    civilization_a UUID NOT NULL REFERENCES civilizations(id) ON DELETE CASCADE,
    civilization_b UUID NOT NULL REFERENCES civilizations(id) ON DELETE CASCADE,
    treaty_terms JSONB NOT NULL DEFAULT '{}',
    formed_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    broken_at TIMESTAMPTZ,
    UNIQUE(experiment_id, civilization_a, civilization_b)
);

CREATE INDEX idx_alliances_experiment ON alliances(experiment_id);

-- ============================================================
-- Events
-- ============================================================
CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    experiment_id UUID NOT NULL REFERENCES experiments(id) ON DELETE CASCADE,
    event_type VARCHAR(64) NOT NULL,
    source_type VARCHAR(32), -- minecraft, civilization, controller
    source_id UUID,
    data JSONB NOT NULL DEFAULT '{}',
    timestamp TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_events_experiment ON events(experiment_id);
CREATE INDEX idx_events_type ON events(experiment_id, event_type);
CREATE INDEX idx_events_timestamp ON events(timestamp DESC);

-- ============================================================
-- Statistics
-- ============================================================
CREATE TABLE statistics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    experiment_id UUID NOT NULL REFERENCES experiments(id) ON DELETE CASCADE,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT now(),
    living_agents INTEGER NOT NULL DEFAULT 0,
    dead_agents INTEGER NOT NULL DEFAULT 0,
    survival_percentage NUMERIC(5,2) NOT NULL DEFAULT 100,
    average_lifespan_seconds INTEGER,
    longest_lifespan_seconds INTEGER,
    deaths INTEGER NOT NULL DEFAULT 0,
    kills INTEGER NOT NULL DEFAULT 0,
    war_casualties INTEGER NOT NULL DEFAULT 0,
    resources_mined JSONB NOT NULL DEFAULT '{}',
    resources_consumed JSONB NOT NULL DEFAULT '{}',
    blocks_placed INTEGER NOT NULL DEFAULT 0,
    blocks_destroyed INTEGER NOT NULL DEFAULT 0,
    chunks_explored INTEGER NOT NULL DEFAULT 0,
    territory_claimed INTEGER NOT NULL DEFAULT 0,
    settlements INTEGER NOT NULL DEFAULT 0,
    cities INTEGER NOT NULL DEFAULT 0,
    civilizations INTEGER NOT NULL DEFAULT 0,
    rulers INTEGER NOT NULL DEFAULT 0,
    government_changes INTEGER NOT NULL DEFAULT 0,
    wars INTEGER NOT NULL DEFAULT 0,
    alliances INTEGER NOT NULL DEFAULT 0,
    minecraft_tps NUMERIC(6,2),
    minecraft_mspt NUMERIC(6,2),
    ai_queue_length INTEGER,
    ai_inference_latency_ms INTEGER,
    tokens_per_second NUMERIC(10,2),
    database_latency_ms INTEGER,
    events_per_second NUMERIC(10,2),
    actions_per_second NUMERIC(10,2)
);

CREATE INDEX idx_statistics_experiment ON statistics(experiment_id, timestamp DESC);

-- ============================================================
-- World Exhaustion
-- ============================================================
CREATE TABLE world_exhaustion (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    experiment_id UUID NOT NULL REFERENCES experiments(id) ON DELETE CASCADE,
    world_exploration_percent NUMERIC(5,2) NOT NULL DEFAULT 0,
    territory_claimed_percent NUMERIC(5,2) NOT NULL DEFAULT 0,
    resource_depletion_percent NUMERIC(5,2) NOT NULL DEFAULT 0,
    blocks_modified INTEGER NOT NULL DEFAULT 0,
    settlement_density NUMERIC(10,4) NOT NULL DEFAULT 0,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_world_exhaustion_experiment ON world_exhaustion(experiment_id);

-- ============================================================
-- Functions
-- ============================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers
CREATE TRIGGER update_experiments_updated_at BEFORE UPDATE ON experiments FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_agents_updated_at BEFORE UPDATE ON agents FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_relationships_updated_at BEFORE UPDATE ON relationships FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_world_exhaustion_updated_at BEFORE UPDATE ON world_exhaustion FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
