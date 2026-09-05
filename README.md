# Homomorphic Neural Net Inference

> **Domain:** Post-Quantum Cryptography & Zero-Knowledge Architecture
> **Reference Guidelines & Standards:** `NIST FIPS 203/204/205, NIST SP 800-90B & ISO/IEC Standards`

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Zero-PHI Guard](https://img.shields.io/badge/Guard-Zero--PHI_Outbound-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## 📖 What It Does

**Homomorphic Neural Net Inference** is an advanced analytical and computational platform implementing Polynomial activation encrypted deep learning inference on CKKS-encrypted medical images. It provides a multi-agent evaluation framework with cryptographic audit trails and PHI (Protected Health Information) protection.

---

## ⚙️ Key Capabilities & Algorithmic Modules

- **Deterministic Calculation Engine**: Strict compliance with standard reference formulations and thresholds.
- **Risk & Urgency Classification**: Multi-tier categorization (ROUTINE, ELEVATED, CRITICAL_STAT) with automated clinical/operational action recommendations.
- **Validation & Guardrails**: Rigorous input bounds checking and anomaly detection.
- **Multi-Agent Worker System**: Specialized workers (InvariantQC, SafetyEscalation, ProtocolConformance) for comprehensive evaluation.
- **Enrichment Suite**: 8 domain-specific engines for features, monitoring, escalation, deployment, audit, workflow, analytics, and outcomes.

---

## 💻 CLI Quickstart & Usage

### Installation
```bash
pip install -e .
```

### 1. Run Single Task Evaluation
```bash
python cli.py audit --task-id TASK-001 --target TARGET-01 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT
```

### 2. System Configuration Query
```bash
python cli.py chat "What is the system status?"
```

### 3. Batch Process CSV Records
```bash
python cli.py batch -i sample.csv -o results.csv
```

### 4. Verify Audit Trail Integrity
```bash
python cli.py verify-audit
```

### 5. Launch FastAPI REST Server
```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

### Input Data Schema

| Field | Type | Description | Requirement |
|:------|:-----|:------------|:------------|
| `task_id` | string | Unique task / case identifier | Required |
| `target_identifier` | string | Entity, patient key, or target | Required |
| `primary_metric` | float | Primary domain measurement or score | Required |
| `secondary_metric` | float | Secondary kinetic or confidence score | Optional (default: 0.0) |
| `is_critical_flag` | boolean | Emergency escalation trigger | Optional (default: false) |
| `status_descriptor` | string | Status code or phenotype descriptor | Optional (default: "NOMINAL") |

---

## 🛡️ Security & Enterprise Architecture

* **Zero-PHI Outbound Interceptor:** Active regex inspection blocking SSNs, MRNs, phone numbers, emails, DOBs, and patient identifiers.
* **Tamper-Evident HMAC-SHA256 Audit Trail:** Chained, cryptographically signed logs for every evaluation and state transition.
* **Air-Gapped LLM Reasoning Adapter:** Agnostic integration for local Ollama instances (`llama3`, `mistral`), Claude 3.5 Sonnet, GPT-4o, and deterministic test mocks.
* **Active Learning Bayesian Calibration:** Dynamic tracker updating worker reliability weights and monitoring Brier calibration drift.
* **FastAPI & Prometheus Telemetry:** Exposes OpenAPI 3.1 REST endpoints and operational Prometheus metrics (`/metrics`).

### Environment Variables

| Variable | Description | Default |
|:---------|:------------|:--------|
| `AUDIT_SECRET_KEY` | Secret key for HMAC-SHA256 audit signatures | Randomly generated (warning issued) |
| `MODEL_PROVIDER` | LLM provider (`mock`, `ollama`, `claude`, `openai`) | `mock` |

---

## 🧪 Testing & Verification

Run the automated test suite:

```bash
pytest -v
```

Execute high-throughput batch simulation benchmarks:

```bash
python simulator.py 1000
```

### API Endpoints

| Endpoint | Method | Description |
|:---------|:-------|:------------|
| `/health` | GET | Health and metadata check |
| `/metrics` | GET | Prometheus operational metrics |
| `/api/audit` | POST | Dispatch task payload across specialized workers |
| `/api/chat` | POST | Air-gapped supervisory conversational assistant |
| `/api/audit/logs` | GET | Retrieve and verify HMAC audit trail |

---

## 🐳 Container Deployment

```bash
docker build -t homomorphic-neural-net-inference .
docker run -p 8000:8000 -e AUDIT_SECRET_KEY=your-secret-key homomorphic-neural-net-inference
```

Or using Docker Compose:

```bash
docker-compose up -d
```

---

## 📁 Project Structure

```
homomorphic-neural-net-inference/
├── agents/                  # Core agent system
│   ├── api.py              # FastAPI REST server
│   ├── base.py             # Security, PHI guard, audit trail
│   ├── models.py           # Pydantic data models
│   ├── supervisor.py       # Multi-agent orchestrator
│   ├── workers.py          # Specialized evaluation workers
│   ├── metrics.py          # Prometheus metrics collector
│   ├── learning.py         # Bayesian calibration engine
│   ├── streamer.py         # WebSocket telemetry broadcaster
│   └── llm_factory.py      # LLM provider factory
├── he_neural_inference/    # Alternative HE-NeuralInference module
│   ├── agents.py           # Coordinator and sub-agents
│   ├── engine.py           # Core algorithmic engine
│   ├── models.py           # Data models
│   ├── cli.py              # CLI interface
│   └── server.py           # FastAPI server factory
├── tests/                  # Test suite
├── web/                    # Operations console (HTML)
├── cli.py                  # Main CLI entry point
├── simulator.py            # High-throughput simulation
├── enrichment.py           # Domain enrichment engines
├── Dockerfile              # Container build
├── docker-compose.yml      # Container orchestration
└── pyproject.toml          # Project configuration
```
