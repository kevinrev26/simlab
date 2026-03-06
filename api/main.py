from fastapi import FastAPI
from .models.schemas import Simulation

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/api/simulation")
def create_simulation(sim: Simulation):
    return f"Json schema received: {sim.uuid}"