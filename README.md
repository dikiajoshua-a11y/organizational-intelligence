# Organizational Intelligence

**An evidence-backed organizational state engine for reconstructing what is happening across complex organizations from fragmented evidence.**

Organizations run on many partial representations of reality: operational systems, spreadsheets, reports, budgets, audits, meeting notes, and people. Each may be locally useful while the overall picture remains inconsistent, incomplete, or out of date.

Organizational Intelligence is designed to reconcile those representations into a traceable view of organizational state: what is happening, what changed, what may be off-track, which dependencies matter, and what requires management attention.

It is an **evidence and reconciliation layer**, not a replacement for ERP, finance, procurement, monitoring and evaluation (M&E), CRM, or banking systems.

## Why this exists

A dashboard can display submitted numbers without establishing whether they describe the same thing. A report can make a claim without proving it. A missed milestone can matter because another activity depends on it, even when the downstream activity has not yet failed.

The system is being developed to make these relationships explicit and help decision-makers distinguish:

- reported facts from verified conclusions;
- genuine contradictions from numbers that are not semantically comparable;
- an observed condition from an allegation about its cause;
- a current state from the historical events and evidence that produced it;
- an operational signal from the management action taken in response.

## Core model

```text
Organization
  └── Programmes
       ├── Entities
       ├── Relationships and dependencies
       ├── Facts and evidence
       ├── Events and audit history
       └── Organizational state
             └── Evidence-backed signals
                   └── Management actions
                         └── Outcomes
```

At the evidence level, the basic relationship is:

```text
ENTITY ── RELATIONSHIP ── ENTITY
  │
  └── FACT / CLAIM ── EVIDENCE
```

Facts should retain their subject, predicate, value, unit, relevant period or date, source, supporting evidence, confidence, and status. New evidence should add to the record rather than silently overwrite history.

## Current implementation

This repository contains an early working prototype, not a finished autonomous intelligence platform.

| Area | Current state |
| --- | --- |
| Backend runtime | FastAPI service backed by SQLite |
| Organizational data | Seeded fictional UDERP test programme and activity entities |
| Relationships | Explicit dependency relationships for selected activities |
| Signals | Deterministic signal recomputation and state retrieval |
| History | Event timeline and audit records in the runtime data model |
| Management actions | Action retrieval associated with programme signals |
| Frontend | Static UDERP Control Center prototype in `frontend/index.html` |
| Real-world reconstruction | A development objective; autonomous ingestion and reconstruction are not yet complete |

**Important data boundary:** the seeded UDERP programme is synthetic test data. It is not evidence about a real organization, programme, district, or beneficiary population. Do not present it as real-world findings.

The frontend is a prototype, and the backend and frontend are separate components. Do not assume that every screen is connected to the backend or that every workflow is production-ready.

## Architecture

```text
organizational-intelligence/
├── backend/
│   ├── app/
│   │   ├── api.py          # FastAPI routes
│   │   ├── db.py           # SQLite schema and connection helpers
│   │   ├── runtime.py      # Runtime initialization and synthetic seed data
│   │   └── signals.py      # Deterministic signal and state logic
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── index.html          # Control Center prototype
│   └── README.md
├── docs/
│   ├── DEVELOPMENT_STATUS.md
│   └── PRODUCT_PRINCIPLES.md
└── README.md
```

## Quick start

### Requirements

- Python 3.10 or newer is recommended.
- A terminal with permission to create a virtual environment and install Python packages.

### Run the backend

From the repository root:

```bash
cd backend
python -m venv .venv
```

Activate the environment:

**macOS / Linux**
```bash
source .venv/bin/activate
```

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies and run the tests:

```bash
python -m pip install -r requirements.txt
pytest -q
```

Start the API:

```bash
python -m app
```

The service runs at [http://127.0.0.1:8000](http://127.0.0.1:8000). Interactive API documentation is available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

The application initializes its SQLite database and seeds the fictional test programme at startup when the organizations table is empty. Database files are ignored by Git; keep local data and credentials out of version control.

### Open the frontend

Open `frontend/index.html` in a browser. See [frontend/README.md](frontend/README.md) for the prototype-specific notes.

## API surface

The current backend exposes these routes:

| Method | Route | Purpose |
| --- | --- | --- |
| `GET` | `/` | Runtime identity and version |
| `GET` | `/programmes/{pid}/state` | Recompute and return programme state and signals |
| `GET` | `/programmes/{pid}/timeline` | Return programme events in chronological order |
| `GET` | `/programmes/{pid}/actions` | Return management actions associated with programme signals |

Use the interactive documentation at `/docs` to inspect response schemas and exercise the running API. The seeded programme is created with a database-generated ID; inspect the database or API behavior rather than assuming IDs will remain stable across fresh databases.

## Product principles

1. **Evidence is not automatically truth.** A source establishes what was reported; validation and corroboration determine what can be concluded.
2. **Preserve history.** Keep prior facts, revisions, events, and decisions traceable.
3. **Compare like with like.** Before treating numeric differences as contradictions, establish comparability across metric definition, unit, period, and geography.
4. **Detection is not accusation.** Signals identify conditions requiring review; they do not independently establish misconduct or causality.
5. **Make conclusions traceable.** Important signals should be linked to their supporting records and evidence.
6. **Prefer precision to alert volume.** Optimize for management usefulness, not the number of notifications.
7. **Constrain AI with provenance.** AI may help extract and interpret evidence, while explicit logic, review, and source traceability constrain state changes.
8. **Test against reality.** Synthetic data is useful for controlled tests; it cannot establish real-world performance.

See [Product Principles](docs/PRODUCT_PRINCIPLES.md) and [Development Status](docs/DEVELOPMENT_STATUS.md).

## What remains to be built

The central unsolved problem is **autonomous reconstruction of organizational state from messy, fragmented source evidence**. Important development areas include:

- source-document ingestion and extraction;
- entity resolution across inconsistent names, identifiers, and systems;
- semantic matching of indicators, measures, units, periods, and geographies;
- cross-source reconciliation with explicit uncertainty and provenance;
- temporal and version reasoning that preserves historical truth;
- dependency propagation to identify downstream consequences;
- controlled review and evidence-driven state updates;
- evaluation on substantial real-world primary-source corpora.

These are development goals, not claims of current capability. A curated experiment or a dashboard populated with manually prepared data is not, by itself, proof of autonomous reconstruction.

## Development loop

The project follows an evidence-driven engineering loop:

```text
Real evidence
    → observed failure
    → missing capability identified
    → engineering change
    → re-test against the same evidence
```

Evaluation should measure extraction accuracy, entity and relationship resolution, reconciliation quality, signal precision, provenance completeness, and usefulness of resulting actions. The final state should not be hand-constructed if the experiment is intended to test autonomous reconstruction.

## Project status

This is an actively developed prototype. Expect incomplete workflows, evolving interfaces, and capabilities that have not yet been validated on substantial real-world evidence. The priority is a reliable organizational state engine whose important conclusions can be traced back to evidence—not a larger dashboard.

## License

No license is specified in this repository yet. Unless and until a license is added, do not assume the code is available for unrestricted reuse.
