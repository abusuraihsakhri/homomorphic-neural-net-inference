"""
FastAPI REST API Server for Homomorphic Neural Net Inference.
"""
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from .base import AuditLogger, PHIGuard
from .models import SystemTaskPayload, ConsensusDossier
from .supervisor import SystemSupervisor
from .metrics import GLOBAL_METRICS

supervisor = SystemSupervisor(model_provider="mock")

app = FastAPI(
    title="Homomorphic Neural Net Inference API",
    description="Enterprise Distributed Component Platform (Post-Quantum Cryptography & Hardware Security)",
    version="3.0.0-ENTERPRISE",
)


class ChatRequest(BaseModel):
    query: str


@app.get("/health")
def health():
    return {"status": "HEALTHY", "service": "homomorphic-neural-net-inference", "domain": "Post-Quantum Cryptography & Hardware Security", "standard": "NIST FIPS 203/204/205 / ISO/IEC 17825 Standards", "version": "3.0.0-ENTERPRISE"}


@app.get("/metrics")
def metrics():
    GLOBAL_METRICS.tasks_total = len(supervisor.dossier_registry)
    GLOBAL_METRICS.audit_blocks_total = len(AuditLogger.get_trail())
    return Response(
        content=GLOBAL_METRICS.export_prometheus_text(),
        media_type="text/plain; version=0.0.4; charset=utf-8",
    )


@app.post("/api/audit")
def api_audit(payload: SystemTaskPayload):
    dossier = supervisor.process_task(payload)
    return dossier.to_dict()


@app.post("/api/chat")
def api_chat(req: ChatRequest):
    try:
        ans = supervisor.query_supervisory_chat(req.query)
        return {"response": ans}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/audit/logs")
def api_audit_logs():
    return {"audit_trail": AuditLogger.get_trail(), "verified": AuditLogger.verify_integrity()}
