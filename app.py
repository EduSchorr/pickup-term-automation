from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from backend.term_service import build_case, render_pickup_term
from backend.tracking import list_recent, register

app = FastAPI(title="Pickup Term Automation", version="portfolio")

@app.get("/api/health")
def health():
    return {"ok": True, "portfolio": True}

@app.post("/api/terms/preview", response_class=HTMLResponse)
def preview(payload: dict):
    try:
        case = build_case(payload)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    tracking_id = f"PORTFOLIO-{uuid4().hex[:12].upper()}"
    register(tracking_id, case.order_id, case.store_email)
    return render_pickup_term(case)

@app.get("/api/dispatches")
def dispatches():
    return list_recent()
