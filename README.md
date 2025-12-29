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
