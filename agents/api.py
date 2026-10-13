"""
FastAPI REST API Server for Homomorphic Neural Net Inference.
"""
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from .base import AuditLogger, PHIGuard, SecurityException
from .models import SystemTaskPayload, ConsensusDossier
from .supervisor import SystemSupervisor
from .metrics import GLOBAL_METRICS

supervisor = SystemSupervisor(model_provider="mock")

app = FastAPI(
    title="Homomorphic Neural Net Inference API",
    description="Deterministic threshold-rule evaluation API. No homomorphic encryption, neural-network inference, or clinical validation.",
    version="2.0.0",
)


class ChatRequest(BaseModel):
    query: str


@app.get("/health")
def health():
    return {"status": "HEALTHY", "service": "homomorphic-neural-net-inference", "domain": "Threshold-rule demonstration", "standard": "No standards certification claimed", "version": "2.0.0"}


@app.get("/metrics")
def metrics():
    GLOBAL_METRICS.audit_blocks_total = len(AuditLogger.get_trail())
    return Response(
        content=GLOBAL_METRICS.export_prometheus_text(),
        media_type="text/plain; version=0.0.4; charset=utf-8",
    )


@app.post("/api/audit")
def api_audit(payload: SystemTaskPayload):
    try:
        dossier = supervisor.process_task(payload)
    except SecurityException as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return dossier.to_dict()


@app.post("/api/chat")
def api_chat(req: ChatRequest):
    try:
        ans = supervisor.query_supervisory_chat(req.query)
        return {"response": ans}
    except SecurityException as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/audit/logs")
def api_audit_logs():
    return {"audit_trail": AuditLogger.get_trail(), "verified": AuditLogger.verify_integrity()}
