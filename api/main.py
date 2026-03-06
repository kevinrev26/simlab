from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from .database.connection import get_db_session, get_engine
from .database.operations import create_simulation, get_simulation_by_uuid
from .models.schemas import SimulationModel, SimulationResponse
from .models.models import Base

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    engine  = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/api/simulations", response_model=dict[str, str|int])
async def post_simulation(sim: SimulationModel, db_session: Annotated[AsyncSession, Depends(get_db_session)]):
    sim_uuid = await create_simulation(
        db_session,
        sim
    )
    return {'simulation_uuid': sim_uuid, 'status': 'queued'}

@app.get("/api/simulations/{uuid}", response_model=SimulationResponse)
async def get_simulation(uuid: str, db_session: Annotated[AsyncSession, Depends(get_db_session)]):
    simulation = await get_simulation_by_uuid(db_session, uuid)
    return simulation