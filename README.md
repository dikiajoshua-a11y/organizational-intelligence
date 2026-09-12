# Organizational Intelligence

An evidence-backed organizational state engine for reconstructing what is happening across complex organizations from fragmented evidence.

## Product thesis

Organizations already have systems, documents, reports, spreadsheets, audits, meetings, and people that each describe part of reality. The problem is keeping those representations coherent enough to answer:

1. What is happening?
2. What changed?
3. What is off-track or conflicting?
4. Who is responsible?
5. What requires action?

The product is not intended to replace core ERP, M&E, procurement, finance, CRM, or banking systems. It is an evidence and reconciliation layer above them.

## Core model

Organization → Programmes → Entities → Facts/Evidence → Relationships → Events
                                      ↓
                              Organizational State
                                      ↓
                                Signals/Risks
                                      ↓
                                  Actions
                                      ↓
                                  Outcomes

## Core model

ENTITY — RELATIONSHIP — ENTITY
   |
   +— FACT/CLAIM — EVIDENCE

Facts retain subject, predicate, value, unit, period/date, source, evidence, confidence, and status. New evidence creates new facts; historical facts are preserved.

Signals are evidence-backed management observations. Detection is separated from accusation, and numeric differences are not treated as contradictions until semantic comparability is established.

## Current implementation

- backend/ — persistent FastAPI/SQLite organizational runtime and deterministic signals.
- frontend/ — Control Center prototype (v1.11).
- experiments/pdm-real-data/ — real-data experiment using public Ugandan Parish Development Model evidence. This is a curated reconstruction experiment, not yet autonomous ingestion.
- docs/ — product principles and development status.

The backend currently contains seeded fictional UDERP data for controlled runtime tests. That seed is synthetic and must not be represented as real organizational evidence.

## Run the backend

    cd backend
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    pytest -q
    python -m app

Then open http://127.0.0.1:8000/docs.

## Development standard

The development loop is evidence-driven:

real evidence → observed failure → missing capability → engineering change → re-test the same evidence

The target is not a larger dashboard. The target is a reliable organizational state engine whose important conclusions remain traceable to evidence.