# Homomorphic Neural Net Inference

**Implementation status:** This repository currently implements configurable-in-code **threshold and descriptor evaluations**, not homomorphic encryption or neural-network inference. There is no CKKS, BFV, encrypted model execution, clinical-model validation, or claimed standards certification. The repository name is retained for continuity.

## What is implemented

- Primary Python evaluation pipeline in `agents/`: checks primary metric **> 25**, secondary metric **> 12** or an explicit critical flag, and status descriptors containing `DISCORDANT`, `ANOMALY`, `MUTANT`, `VIOLATION`, `FAIL`, or `REJECT`. Returns a structured evaluation dossier.
- Alternative legacy rule coordinator in `he_neural_inference/` with its own thresholds. It is not an encrypted-computation engine.
- CLI audit, mock chat, CSV batch processing, and audit-integrity verification.
- FastAPI endpoints for health, rule evaluation, mock chat, Prometheus-style metrics, and process-local audit logs.
- HMAC-SHA256 chained audit entries and pattern-based identifier screening; see limitations below.
- A static browser demonstration in `web/` that evaluates the primary rules locally and exports JSON. No backend or browser Python runtime is required.

## Browser demonstration

Run a local static HTTP server:

```bash
python -m http.server 8765 --directory web
```

Open **http://localhost:8765/**. The page runs JavaScript locally, without remote API calls. It does not encrypt inputs or sign audit records. Only use synthetic data. A GitHub Pages deployment workflow is included; the existence of the workflow does not itself verify that Pages is enabled.

## Install and use

Requires Python 3.9 or newer; CI exercises Python 3.10–3.13.

```bash
python -m pip install -e ".[server,test]"
python cli.py audit --task-id DEMO-01 --target SYNTHETIC-01 --primary 29.4 --secondary 14.8 --status DISCORDANT
python cli.py batch -i sample.csv -o results.csv
python cli.py verify-audit
python cli.py chat "What is the status?"
```

The installed `homomorphic-neural-net-inference` command retains the alternative `he_neural_inference.cli` entry point for compatibility. Use `python cli.py` for the primary pipeline documented above. Both CSV implementations explicitly parse `True` and `False`, report malformed values, and escape spreadsheet-formula-like input on export.

Start the API:

```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

Visit **http://127.0.0.1:8000/docs** for generated OpenAPI documentation. The main endpoints are `GET /health`, `POST /api/audit`, `POST /api/chat`, `GET /metrics`, and `GET /api/audit/logs`. `/api/chat` provides a deterministic mock response, not a live model.

## Security and data handling

- **Do not submit identifiable patient data.** The pattern-based identifier filter catches some emails, MRNs, phone numbers, SSNs, and names, but is neither comprehensive de-identification nor a HIPAA-compliance guarantee.
- The API has **no authentication or transport-layer configuration**. It must not be exposed to the public internet or used for protected health information without an appropriate security architecture.
- Audit records are HMAC-signed and checked against their signed contents and predecessor hash. They are **in-memory only**, lost on restart, and cannot prove completeness against deletion of final entries. They are not an immutable or externally anchored audit ledger.
- Set a strong `AUDIT_SECRET_KEY` environment variable to preserve signing-key identity across restarts. Without it, the process generates a random temporary key.
- No user records are sent from the static browser demo, stored by its server, or written to browser storage. The page can export a JSON file on request.
- The repository previously contained a hard-coded Compose signing key. **Rotate that key if it was ever used.** Removing it from the current configuration does not erase Git history.

For Docker Compose, set the key in the shell environment before starting:

```bash
export AUDIT_SECRET_KEY="$(openssl rand -hex 32)"
docker compose up --build
```

Docker also supports `docker build -t homomorphic-neural-net-inference .` and running the image with a supplied `AUDIT_SECRET_KEY`.

## Tests and development

```bash
python -m pip install -e ".[server,test]"
python -m pytest -q
node --test web/app.test.cjs
python -m compileall -q agents he_neural_inference cli.py enrichment.py simulator.py
```

No npm install or JavaScript bundler is needed. The GitHub Actions CI workflow runs Python regression tests and browser-rule tests. Runtime rule logic remains source-authoritative; statements about CKKS or clinical performance in older commits are not evidence that those capabilities exist.

## Technology and license

Python, Pydantic 2, FastAPI (optional server), standard-library HMAC-SHA256, plain HTML/CSS/JavaScript, and GitHub Actions. The standalone browser demo targets modern evergreen browsers; comprehensive cross-browser validation has not been performed.

MIT license; see [LICENSE](LICENSE).
