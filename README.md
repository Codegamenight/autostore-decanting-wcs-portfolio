# AutoStore-Style Decanting WCS (Portfolio)

This project demonstrates a simplified, production-style **AutoStore decanting workflow**
implemented as a **Warehouse Control System (WCS)** service.

## What this shows
- Event-driven decant order orchestration
- Deterministic state machine (CREATED → COMPLETED)
- Simulated robot interaction and port behavior
- Traceable execution log (operator / integrator visibility)
- API-first design aligned with WMS/WCS integration patterns

## Why this matters
Decanting is a real operational bottleneck in AutoStore environments.
This project models how a WCS coordinates orders, robot actions, and system state
without relying on proprietary AutoStore internals.

---

## What this is

A simplified, production-style **AutoStore decanting workflow** implemented as a
**Warehouse Control System (WCS)** service.

The service accepts decant orders via API, simulates robot and port behavior,
and returns a full execution trace from order creation to completion.

## Key features

- API-first design aligned with WMS/WCS integration patterns
- Deterministic state machine (CREATED → IN_PROGRESS → COMPLETED)
- Traceable execution log for operational visibility
- Simulated robot and port interaction
- Automated health validation using pytest

## How to run

```bash
# Activate virtual environment
.venv\Scripts\activate

# Start API
python -m uvicorn app.main:app --app-dir src --reload


## Demo

Open Swagger:
- http://127.0.0.1:8000/docs

Run:
- POST `/decant/order`

Request:
```json
{
  "sku": "SKU-123",
  "quantity": 5,
  "bin_id": "BIN-A01"
}
<<<<<<< HEAD
## Project Milestones

- Initial AutoStore-style decanting WCS with deterministic state machine
- API-first design with Swagger-based demo
- Fault injection for tote availability and robot pick failures
- Operator-centric fault handling with guidance and recovery actions
- Lightweight runtime metrics for observability
=======


>>>>>>> 86760b4 (Document project milestones and operational capabilities)
