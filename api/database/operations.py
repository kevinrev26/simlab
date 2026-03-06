from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import uuid as uuid_lib
from fastapi import HTTPException

from api.models.models import ( 
    Simulation, SimulationRuntime,
    SimulationResources, SimulationBehavior,
    SimulationStorage, SimulationObservability
)
from api.models.schemas import SimulationModel

async def create_simulation(
    db_session: AsyncSession,
    sim: SimulationModel
) -> str | None:
    uuid = ''
    simulation = Simulation(
        schema_version=sim.schema_version,
        name=sim.name,
        label=sim.label,
        priority=sim.priority,
        status=sim.status,
    )

    simulation.runtime = SimulationRuntime(
        runs_per_container=sim.runtime.runs_per_container,
        image_name=sim.runtime.image_name,
        image_tag=sim.runtime.image_tag,
    )

    simulation.resources = SimulationResources(
        cpu_limit=sim.resources.cpu_limit,
        memory_limit=sim.resources.memory_limit,
        max_containers=sim.resources.max_containers,
        max_duration_seconds=sim.resources.max_duration_seconds,
    )

    simulation.behavior = SimulationBehavior(
        seed=sim.behavior.seed,
        timeout_seconds=sim.behavior.timeout_seconds,
        max_attempts=sim.behavior.max_attempts,
    )

    simulation.storage = SimulationStorage(
        volume_name=sim.storage.volume_name,
        output_path=sim.storage.output_path,
    )

    simulation.observability = SimulationObservability(
        log_level=sim.observability.log_level,
        metrics_enabled=sim.observability.metrics_enabled,
        webhook_url=str(sim.observability.webhook_url) if sim.observability.webhook_url else None,
    )

    async with db_session.begin():
        db_session.add(simulation)
        await db_session.flush()
        uuid = str(simulation.uuid)

    return str(uuid)

async def get_simulation_by_uuid(
    db_session: AsyncSession,
    simulation_uuid: str
) -> Simulation | None:
    result = await db_session.execute(
        select(Simulation).where(Simulation.uuid == uuid_lib.UUID(simulation_uuid))
    )
    simulation = result.scalar_one_or_none()
    if simulation is None:
        raise HTTPException(status_code=404, detail="Simulation not found")
    return simulation
