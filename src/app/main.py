from fastapi import FastAPI
from pydantic import BaseModel

from app.simulator.tick import run_simulation_for_seconds
from app.simulator.decant_workflow import (
    create_decant_task,
    run_decant_task,
    task_to_dict,
)

app = FastAPI(title="AutoStore Decanting WCS Portfolio")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/simulate/run")
def simulate_run(seconds: int = 5):
    events = run_simulation_for_seconds(seconds)
    return {
        "ran_seconds": seconds,
        "events": events,
    }


class DecantOrder(BaseModel):
    sku: str
    quantity: int
    bin_id: str


@app.post("/decant/order")
def decant_order(order: DecantOrder):
    task = create_decant_task(order.sku, order.quantity)
    task = run_decant_task(task)
    return task_to_dict(task)
