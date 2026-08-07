import pytest


@pytest.mark.asyncio
async def test_agent_creation():
    from controller.app.agent.manager import agent_manager
    agent = await agent_manager.create_agent("TestAgent", {"aggression": 0.5})
    assert agent.username == "TestAgent"
    assert agent.life_state == "ACTIVE"


@pytest.mark.asyncio
async def test_agent_persistence():
    from controller.app.agent.manager import agent_manager
    agent = await agent_manager.create_agent("PersistAgent", {})
    fetched = await agent_manager.get_agent(agent.id)
    assert fetched is not None
    assert fetched.username == "PersistAgent"


@pytest.mark.asyncio
async def test_permanent_death():
    from controller.app.agent.manager import agent_manager
    agent = await agent_manager.create_agent("DieAgent", {})
    result = await agent_manager.mark_dead(agent.id, {"cause": "lava"})
    assert result is True
    assert agent.life_state == "DEAD"
    result2 = await agent_manager.mark_dead(agent.id, {})
    assert result2 is False


@pytest.mark.asyncio
async def test_memory_creation():
    from controller.app.systems.memory import memory_system
    memory = await memory_system.create_memory("agent-1", "events", {"event": "found settlement"}, 0.9)
    assert memory.category == "events"
    assert memory.importance == 0.9


@pytest.mark.asyncio
async def test_relationship_score():
    from controller.app.systems.relationships import relationship_system
    rel = await relationship_system.set_relationship("exp-1", "a", "b", "friendship", 0.7)
    assert rel.score == 0.7
    assert rel.relationship_type == "friendship"


@pytest.mark.asyncio
async def test_settlement_creation():
    from controller.app.systems.settlements import settlement_system
    settlement = await settlement_system.create_settlement("exp-1", "Alpha", "agent-1", {"x": 0, "z": 0})
    assert settlement.name == "Alpha"
    assert settlement.population == 1


@pytest.mark.asyncio
async def test_civilization_creation():
    from controller.app.systems.civilizations import civilization_system
    civ = await civilization_system.create_civilization("exp-1", "TestCiv", "agent-1")
    assert civ.name == "TestCiv"
    assert civ.leader_id == "agent-1"


@pytest.mark.asyncio
async def test_territory_claim():
    from controller.app.systems.territory import territory_system
    claim = await territory_system.claim("exp-1", "civ-1", 0, 0, "overworld")
    assert claim.chunk_x == 0
    assert claim.chunk_z == 0


@pytest.mark.asyncio
async def test_war_declaration():
    from controller.app.systems.war import war_system
    war = await war_system.declare_war("exp-1", "civ-a", "civ-b", [{"chunk_x": 1, "chunk_z": 1}])
    assert war.status == "ACTIVE"
    assert war.attacker_civilization_id == "civ-a"


@pytest.mark.asyncio
async def test_event_publishing():
    from controller.app.systems.events import event_system
    received = []
    event_system.subscribe(lambda e: received.append(e))
    await event_system.minecraft_event("exp-1", "PLAYER_JOINED", "agent-1", {"username": "Test"})
    assert len(received) == 1
    assert received[0].event_type == "PLAYER_JOINED"
