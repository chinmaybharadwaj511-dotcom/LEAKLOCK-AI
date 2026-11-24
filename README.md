# LEAKLOCK — AI Data Protection Gateway

**IBM Z Datathon 2026 · AI Secured: Innovation Without Exposure**

LEAKLOCK is an enterprise-oriented AI prompt inspection gateway that detects, classifies, and governs sensitive data before prompts are sent to external Large Language Models (LLMs). It runs entirely locally — no prompt text or matched secrets ever leave the machine.

---

## Table of Contents

1. [Features](#features)
2. [Architecture](#architecture)
3. [Quick Start](#quick-start)
4. [Windows 11 Setup](#windows-11-setup)
5. [Rocky Linux 10.x Setup](#rocky-linux-10x-setup)
6. [Running Tests](#running-tests)
7. [Configuration](#configuration)
8. [Project Structure](#project-structure)
9. [Detection Categories](#detection-categories)
10. [Agent Roles & Policy Enforcement](#agent-roles--policy-enforcement)
11. [Security Audit Notes](#security-audit-notes)
12. [Known Limitations](#known-limitations)
13. [Development Roadmap](#development-roadmap)

---

## Features

| Capability | Status |
|---|---|
| 12-category sensitive-data detection (regex + Luhn + secondary validation) | ✅ Active |
| Explainable 0–100 contextual risk scoring with factor breakdown | ✅ Active |
| 2-bit hardware-compatible risk encoding (for future Verilog controller) | ✅ Active |
| Prompt injection & data exfiltration threat detection | ✅ Active |
| Optional hybrid AI contextual analysis (on pre-redacted text only) | ✅ Active |
| Role-based ALLOW / REDACT / BLOCK policy engine (4 agent profiles) | ✅ Active |
| Automatic span-level redaction (`[REDACTED_<CATEGORY>]`) | ✅ Active |
| Privacy-conscious audit logger (SHA-256 fingerprint + metadata only) | ✅ Active |
| Interactive Streamlit multi-page UI | ✅ Active |
| 71-test automated pytest suite | ✅ Active |
| Verilog hardware controller (RTL stub, future Phase 3) | ⏳ Planned |

---

## Architecture

```
Streamlit UI  (app.py + pages/)
       │
       ▼
core/detector.py      ← Regex engine: finds sensitive spans + validates
core/threat_detector.py  ← Prompt injection / exfiltration rules
core/risk_scorer.py      ← Explainable 0–100 contextual score
core/policy_engine.py    ← ALLOW / REDACT / BLOCK per agent role
core/audit_logger.py     ← Privacy-preserving SHA-256 metadata log
       │
       ▼
hardware/interface/   ← Future Python ↔ Verilog bridge (Phase 3)
```

All detection, scoring, and policy decisions run in-process. No network calls are made for prompt analysis. Prompts are **never written to disk** by default.

---

## Quick Start

### Prerequisites

- Python **3.10 or later** (3.12 recommended)
- `pip` (bundled with Python)
- No database, no external services, no API keys required

### Minimal install

```bash
# 1. Clone / download the project
cd /path/to/LEAKLOCK

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate          # Linux / macOS
# OR
.venv\Scripts\Activate.ps1         # Windows PowerShell

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

Open your browser at **http://127.0.0.1:8501**

---

## Windows 11 Setup

### Option A — Startup script (recommended)

```powershell
# From the project root, in PowerShell:
powershell -ExecutionPolicy Bypass -File scripts\run_windows.ps1
```

The script:
- Checks for Python 3.10+
- Creates `.venv` if it does not exist
- Installs all requirements
- Runs the test suite
- Starts Streamlit on `127.0.0.1:8501`

To skip tests on subsequent runs:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_windows.ps1 -SkipTests
```

### Option B — Manual steps

```powershell
# 1. Create venv
python -m venv .venv
.venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Run tests
python -m pytest tests/ -v

# 4. Start the application
streamlit run app.py
```

### Windows troubleshooting

| Problem | Fix |
|---|---|
| `python` not found | Install Python from https://python.org and check "Add to PATH" |
| PowerShell execution policy error | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| Port 8501 in use | Set `LEAKLOCK_PORT=8502` in `.env` or use `streamlit run app.py --server.port 8502` |
| `streamlit` not found after install | Ensure the venv is activated: `.venv\Scripts\Activate.ps1` |

---

## Rocky Linux 10.x Setup

### Option A — Startup script (recommended)

```bash
# Make the script executable (first time only)
chmod +x scripts/run_linux.sh

# Run
./scripts/run_linux.sh
```

To skip tests:

```bash
./scripts/run_linux.sh --skip-tests
```

### Option B — Manual steps

```bash
# 1. Install system Python if needed
sudo dnf install python3 python3-pip    # Rocky Linux 10 / RHEL
# or
sudo apt install python3 python3-pip    # Ubuntu/Debian

# 2. Create and activate venv
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Run tests
python -m pytest tests/ -v

# 5. Start the application
streamlit run app.py
```

Open your browser at **http://127.0.0.1:8501**

### Rocky Linux troubleshooting

| Problem | Fix |
|---|---|
| Python 3.10 not available | `sudo dnf install python3.12` (EPEL may be needed) |
| `streamlit` browser doesn't open automatically | Navigate manually to `http://127.0.0.1:8501` |
| Port blocked by firewall | `sudo firewall-cmd --add-port=8501/tcp --zone=public` (only if needed for remote access) |
| Permission denied on `.sh` | `chmod +x scripts/run_linux.sh` |

### IBM LinuxONE / z/Architecture

LEAKLOCK uses only pure-Python packages with no compiled C extensions beyond numpy/pandas (which Streamlit bundles). Pre-built wheels for s390x are available for Python 3.10+ via `pip`. If wheels are unavailable:

```bash
pip install --no-binary :all: -r requirements.txt
```

This requires a C compiler (`gcc`) and build tools (`python3-devel`).

---

## Running Tests

```bash
# Full suite (71 tests)
python -m pytest tests/ -v

# Quick run (no verbose output)
python -m pytest tests/ -q

# Specific test file
python -m pytest tests/test_security_workflow.py -v

# With coverage (if pytest-cov is installed)
python -m pytest tests/ --cov=core --cov-report=term-missing
```

### Test files

| File | What it tests |
|---|---|
| `tests/test_detector.py` | Regex detection accuracy, offsets, overlap resolution, edge cases |
| `tests/test_app_structure.py` | File layout, imports, JSON schema, settings |
| `tests/test_security_workflow.py` | End-to-end security pipeline: detection → policy → redaction → audit |

---

## Configuration

Copy `.env.example` to `.env` and edit as needed:

```bash
cp .env.example .env
```

| Variable | Default | Description |
|---|---|---|
| `LEAKLOCK_ENV` | `development` | Environment label |
| `LEAKLOCK_PHASE` | `Phase 2 Enhanced: Detection, Policy & Audit` | Phase label shown in UI |
| `LEAKLOCK_DECISION_BACKEND` | `software_fallback` | `software_fallback` or `verilog_controller` |
| `LEAKLOCK_LOG_PROMPTS` | `false` | Set to `true` only for debugging (logs prompt text!) |
| `LEAKLOCK_HOST` | `127.0.0.1` | Bind address for Streamlit server |
| `LEAKLOCK_PORT` | `8501` | Bind port for Streamlit server |

> **Security:** Never change `LEAKLOCK_HOST` to `0.0.0.0` unless the port is protected by a firewall or reverse proxy. Never commit `.env` to version control.

---

## Project Structure

```
LEAKLOCK/
├── app.py                        # Main Streamlit entry point (home page)
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variable template
├── .gitignore
├── README.md
│
├── pages/
│   ├── 1_Security_Scanner.py    # Interactive prompt scanner
│   ├── 2_Policy_Manager.py      # Agent role & policy reference
│   ├── 3_Audit_Dashboard.py     # Live audit telemetry
│   └── 4_About.py               # Project info & roadmap
│
├── core/
│   ├── detector.py              # Regex detection engine (12 categories)
│   ├── threat_detector.py       # Prompt injection & exfiltration rules
│   ├── risk_scorer.py           # Explainable 0–100 risk scoring
│   ├── policy_engine.py         # RBAC policy evaluation & redaction
│   └── audit_logger.py          # Privacy-preserving audit logger
│
├── config/
│   └── settings.py              # Centralized application settings
│
├── data/
│   └── sample_prompts.json      # Synthetic demonstration prompts
│
├── services/
│   └── __init__.py              # Services package (Phase 3+ expansion)
│
├── scripts/
│   ├── run_linux.sh             # Linux/Rocky Linux startup script
│   └── run_windows.ps1          # Windows 11 startup script (PowerShell)
│
├── tests/
│   ├── test_detector.py         # Detection engine unit tests
│   ├── test_app_structure.py    # Structural & import tests
│   └── test_security_workflow.py # Security pipeline integration tests
│
├── hardware/                    # Phase 3 Verilog stubs (empty placeholders)
│   ├── rtl/                     # Future: leaklock_controller.v
│   ├── tb/                      # Future: testbench
│   ├── sim/                     # Future: iverilog simulation
│   ├── synthesis/               # Future: Yosys synthesis
│   ├── physical/                # Future: FPGA constraints
│   └── interface/               # Future: Python ↔ simulator bridge
│
└── docs/
    └── architecture.md          # Architecture specification
```

---

## Detection Categories

All detection runs locally in-memory using Python's `re` module. No prompt text leaves the process.

| Category | Example Pattern | Default Risk | Secondary Validation |
|---|---|---|---|
| `EMAIL` | `sujan@example.com` | MEDIUM | Regex boundary checks |
| `PHONE` | `+91 98765 43210`, `+1-415-555-0199` | MEDIUM | Digit count 10–15 |
| `API_KEY` | `sk-demo-123456789abcdef`, `api_key=SECRET` | HIGH | — |
| `JWT_TOKEN` | `eyJ…header.payload.signature` | HIGH | 3-part dot format |
| `PRIVATE_KEY_HEADER` | `-----BEGIN RSA PRIVATE KEY-----` | CRITICAL | — |
| `CREDIT_CARD` | `4532-0151-1283-0366` | CRITICAL | Luhn checksum |
| `AADHAAR_ID` | `2345 6789 0123` | HIGH | Start digit 2–9 |
| `PAN_ID` | `ABCDE1234F` | HIGH | 5 alpha + 4 digit + 1 alpha |
| `EMPLOYEE_ID` | `EMP-12345` | HIGH | — |
| `CUSTOMER_ID` | `CUST-98765` | HIGH | — |
| `CONFIDENTIAL_IDENTIFIER` | `PROJECT-ALPHA-CONFIDENTIAL` | HIGH | — |
| `IPV4_ADDRESS` | `10.24.16.88`, `192.168.1.1` | MEDIUM | Octet range 0–255 |

---

## Agent Roles & Policy Enforcement

| Role | Max Risk | Redactable | Blocked |
|---|---|---|---|
| `PUBLIC_ASSISTANT` | LOW | EMAIL, PHONE, IPV4 | All credential & enterprise categories |
| `INTERNAL_ANALYST` | MEDIUM | EMAIL, PHONE, IPV4, EMP_ID, CUST_ID, AADHAAR, PAN | API keys, cards, private keys, JWT, confidential IDs |
| `PRIVILEGED_DEBUGGER` | HIGH | Most categories incl. API keys, JWT | CREDIT_CARD, PRIVATE_KEY_HEADER |
| `AUTOMATED_PIPELINE` | LOW | _(none — zero-trust)_ | All sensitive categories |

Any prompt injection / exfiltration threat triggers an immediate **BLOCK** regardless of role.

---

## Security Audit Notes

### Verified safeguards

- **Fail-closed by default:** Categories not in a role's redactable or blocked list default to BLOCK (not silently allowed).
- **Zero secret leakage in audit log:** Audit records store SHA-256 fingerprints, category counts, and span lengths — never raw prompt text or matched values. Verified by automated tests (`TestAuditLogging`).
- **Pre-redacted AI analysis:** When hybrid AI analysis is enabled, secrets are masked with `[REDACTED_<CATEGORY>]` before the text is passed to the AI layer.
- **No subprocess execution:** Detection is pure Python regex; no shell commands are invoked.
- **No path traversal risk:** Sample prompts are loaded from a fixed resolved path; filenames are not user-supplied.
- **Prompt treated as untrusted:** Text inside prompts is never executed, interpreted, or used to construct system commands.
- **No credentials in code:** No API keys, passwords, or secrets are hard-coded. The `.env.example` contains only placeholder values.
- **Localhost-only by default:** Streamlit binds to `127.0.0.1` unless explicitly overridden.

### Known limitations / unverified protections

- **Regex coverage only:** Unstructured secrets, obfuscated text, custom credential formats, or paraphrased confidential information are **not detected**.
- **No authentication or authorization:** The Streamlit UI has no login mechanism. It is suitable for local/trusted-network use only.
- **CORS:** Streamlit's built-in CORS handling is used; no custom CORS policy is enforced.
- **Input size:** No hard limit on prompt length in the UI. Very large inputs may cause slow UI response.
- **Prompt injection to the application itself:** The application does not forward prompts to an LLM; there is no risk of prompt injection affecting the application's own behavior.
- **Windows 11 compatibility:** Statically verified — all imports use Python stdlib and `re` module patterns that are cross-platform. Paths use `pathlib.Path` throughout. **Manual end-to-end test on Windows 11 was performed** in this session using Python 3.12.10 on Windows.
- **Rocky Linux 10.x compatibility:** Statically verified. All code is pure Python with no Linux-specific syscalls. The startup script uses POSIX-compatible bash. **A manual end-to-end run on Rocky Linux 10 has not been performed** in this session but no platform-specific code barriers exist.

---

## Development Roadmap

| Phase | Description | Status |
|---|---|---|
| Phase 1 | Project foundation, modular layout, Streamlit UI shell | ✅ Complete |
| Phase 2 | Detection engine, risk scoring, policy engine, audit logger | ✅ Complete |
| Phase 3 | Custom Verilog RTL controller (`leaklock_controller.v`) | ⏳ Planned |
| Phase 4 | Advanced threat intelligence, ML anomaly detection | ⏳ Planned |
| Phase 5 | End-to-end integration, IBM LinuxONE deployment readiness | ⏳ Planned |


---

## Phase 4: Security Validation, Limitations & Reliability

### 1. Validated Test Categories
- **Sensitive-Data Detection (`tests/test_detector.py`)**: Positive and negative synthetic test coverage across emails, phone numbers, API keys/tokens, employee/customer IDs, confidential project IDs, Luhn-validated credit-card numbers, PEM private keys, JWT tokens, government ID placeholders (`[Aadhaar Redacted]`), synthetic PAN identifiers (`ABCDE1234F`), and private IPv4 ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`).
- **Overlap-Safe Redaction**: Verified via `redact_spans_safely()`, which sorts character spans by `(start ASC, end DESC)`, merges overlapping intervals while preserving all detected category names (`[REDACTED:CAT1+CAT2]`), and replaces spans right-to-left so character offsets and surrounding Unicode characters never drift.
- **Threat Detection & False-Positive Resistance (`tests/test_security_workflow.py`)**: Covers instruction overrides, system-prompt extraction, data exfiltration, jailbreak framing, and Base64/encoding bypass cues alongside benign programming lookalikes.
- **Fail-Closed Resilience**: Simulated exceptions across detection, threat scanning, risk scoring, and policy evaluation verify that failures always produce `BLOCK`, suppress `sanitized_prompt` (`None`), and never leak raw secrets or file paths in error messages.
- **Audit Privacy & Concurrency**: Verified that audit events and JSONL exports strip all raw prompt and secret fields, record deterministic SHA-256 prompt fingerprints (`sha256:<16-hex-chars>`), and synchronize concurrent access via `threading.RLock`.

### 2. Documented Input Limits
- **Maximum Prompt Size**: `10,000` characters (`MAX_PROMPT_LENGTH` in `config/settings.py`). Requests exceeding `10,000` characters or containing null bytes (`\x00`) are rejected before regex evaluation with a `BLOCK` decision and an `INPUT_LIMIT_EXCEEDED` / `MALFORMED_INPUT_NULL_BYTE` audit event.

### 3. Known Detection Limitations
- **Pattern & Heuristic Scope**: Regex and heuristic detectors provide fast, deterministic defense-in-depth for structured secrets and known adversarial phrases, but cannot guarantee detection of novel semantic prompt injections, custom cipher/steganographic encodings, or unstructured confidential business logic.
- **Pattern Match != Verified Live Identity**: A regex or Luhn match indicates structural similarity to a credential or identifier, not proof that an active credential or real identity exists.

### 4. Audit Retention Behavior
- **In-Memory Default**: By default, audit events are stored in memory for the lifetime of the running Python process and reset upon application restart. Operators should use the **Export Audit Log (JSONL)** control in the Audit Dashboard for external retention.

### 5. Running the Validation Suite
```bash
# Run full test suite with verbose output
pytest -v

# Run detector and redaction span tests only
pytest tests/test_detector.py -v

# Run security workflow, fail-safe, concurrency, and latency harness tests
pytest tests/test_security_workflow.py -v
```