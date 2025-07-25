 <context>
# Overview  
An agentic, Google‑first financial advisor app that lets users "talk to their money". It aggregates personal finance data (banks, credit cards, MF/stock portfolios, EPF, etc.) through an FI-MCP tool, mixes it with public market data, and uses a multi‑agent system (python-adk + FastAPI backend) to analyze, visualize, and plan. Target users are Indian retail investors, salaried professionals, and DIY finance geeks who want actionable insights, periodic reports, and proactive alerts—not static dashboards.

# Core Features

[x] **1. Unified Personal Finance View**

* **What:** Consolidate all user accounts, holdings, liabilities, cashflows, and net worth.
* **Why:** Single source of truth → reduces fragmentation and blind spots.
* **How:** Personal Finance Data Agent via FI-MCP; normalized into Firestore/BigQuery.

[x] **2. Market Context & Benchmarking**

* **What:** Compare user portfolio vs indices, sectors, inflation, and peers.
* **Why:** Users need to know if they’re outperforming or lagging.
* **How:** Public Data Agent pulls index/ETF data, macro indicators, news sentiment.

[x] **3. Goal-Based Financial Planning**

* **What:** Create/track goals (retirement, house, emergency fund) with Monte Carlo/what‑if analysis.
* **Why:** Moves from reactive look-back to proactive planning.
* **How:** Planner Agent decomposes user objectives; Python Analysis Agent runs simulations. 

[x] **4. Scheduled AI Reports & Alerts**

* **What:** Periodic summaries (weekly/monthly), anomaly alerts (bill spikes, MF underperformance), tax reminders.
* **Why:** Automation keeps users engaged without manual prompts.
* **How:** Cloud Scheduler → Pub/Sub → FastAPI job → Agents generate artifacts → Notify via FCM/email.

[x] **5. Visual Insight Delivery**

* **What:** Rich charts/plots (cashflow trends, asset allocation, drawdowns).
* **Why:** Visuals beat dense text for lay users.
* **How:** Visualization Agent (python code exec sandbox) returns images/HTML snippets stored in GCS.

[x] **6. Research on Active Investments**

* **What:** Deep dives on user’s holdings—fund fact sheets, stock fundamentals, earnings, risk metrics.
* **Why:** Contextual intel drives smarter decisions.
* **How:** Public Data + Python Analysis Agents generate briefs/on-demand dossiers.

[x] **7. Smart Recommendations & Next Actions**

* **What:** Actionable tips (rebalance 5% from debt to equity, prepay this loan tranche, harvest tax losses).
* **Why:** Insights must translate to action.
* **How:** Finalise Response Agent synthesizes agent outputs into concise guidance.

[x] **8. Natural-Language Chat Interface**

* **What:** Users ask anything—“How much did I spend on dining last month?” “What if NIFTY falls 10%?”
* **Why:** Removes UI friction; fits mobile.
* **How:** Primary Orchestrator Agent with tool-calling to sub-agents.

[?] **9. Compliance & Tax Helper** (deferred for future scope)

* **What:** GST/ITR prep hints (if business), capital gains summary, Section 80C/80D utilization.
* **Why:** High pain point; adds differentiated value.
* **How:** Tax Rules KB + Python Analysis Agent + periodic reminders.

[x] **10. Data Hygiene & Security Dashboard**

* **What:** Show connected sources, last sync times, revoke controls, encryption status.
* **Why:** Builds trust, helps with audits.
* **How:** Firebase Auth, IAM, Secret Manager; surface meta-data in UI.

(Add-ons: Shared family view, advisor export packs, webhook/API for power users.)

# User Experience

**Personas**

* **The Salaried Saver (25–40):** Wants clarity on spends, loans, emergency fund, ELSS allocation.
* **The DIY Investor (30–55):** Track portfolio vs benchmarks, sector weights, tax harvesting.
* **The Busy Professional (35–60):** Prefers scheduled briefs/alerts; low manual effort.

**Key Flows**

1. **Onboarding & Data Connect:** Sign in with Firebase → consent to FI-MCP → initial sync.
2. **Ask & Analyze:** User asks; Primary Agent plans → sub-agents fetch/analyze → visuals summarised.
3. **Goal Setup:** User defines goal → Planner Agent breaks tasks → periodic tracking.
4. **Scheduling Reports:** User schedules "Monthly Net Worth Brief" → system runs → push notification.
5. **Artifact Retrieval:** User has to consent to save the artifact → User taps a chart/report → loads from GCS via signed URL.

**UI/UX Considerations**

* Web/Mobile-first; light/dark modes, eye-comfort palettes.
* Chat-centric main screen with quick chips ("Spends", "Investments", "Taxes", "Goals").
* Recommend some prompt hints in the chat input area with animations. (like Google AI Studio) - create set of example prompts (various use case 10-15 per use case)
* Visuals inline (lazy-loaded) with ability to expand/share.
* Clear data source & timestamp labels for trust.
* Fail gracefully: show partial results + retry options if a tool fails.

 </context>

 <PRD>
# Technical Architecture  
**System Components**  
- **Client:** Flutter/React Native (mobile), optional web app.  
- **Auth & User Store:** Firebase Auth, Firestore (users, sessions, schedules).  
- **Backend:** FastAPI on Cloud Run (or GKE Autopilot) exposing python-adk agent endpoints.  
- **Agent Layer:** Single-entry Primary Orchestrator Agent (python-adk) that receives every user request and internally tool-calls all sub‑agents (Personal Finance, Public Data, Python Analysis, Visualization, Finalise Response, Planner). No direct HTTP invocation of sub‑agents.
- **LLM Runtime:** Vertex AI Gemini (tool-calling) or on-prem ADK models.  
- **Tools/MCPs:** FI-MCP (external), Web Search MCP, Market Data MCP, Code Exec Sandbox (Cloud Run job or Firecracker VM), Email/Notification MCP.  
- **Data Storage:** Firestore (users, chat/meta, consent flags), Cloud Storage (artifacts **only if** user consents), optional BigQuery for anonymous aggregated analytics. **No raw personal financial records are persisted**—they're fetched on-demand from FI-MCP and discarded unless explicitly retained in chat history.
- **Async & Scheduling:** Cloud Scheduler → Pub/Sub → Cloud Tasks/Workflows to trigger agent runs.  
- **Monitoring & Logging:** Cloud Logging, Error Reporting, OpenTelemetry traces from FastAPI/adk.

**Data Models (high level)**

```yaml
User:
  uid: string (Firebase)
  profile: {name, email, country, risk_profile}
  consents:
    store_financial_snippets: bool
    store_artifacts: bool
    retention_days: int
    granted_at: datetime

ChatSession:
  id: string
  user_id: ref(User)
  created_at: datetime
  title: string
  consent_snapshot: {store_financial_snippets, store_artifacts, retention_days}

Message:
  session_id: ref(ChatSession)
  role: ['user','assistant','system']
  text: string (redacted if contains financial PII and consent=false)
  artifacts: [ref(Artifact)]
  contains_financial_data: bool
  retention_expires_at: datetime | null
  agent_trace_id: string

Artifact:
  id: string
  type: ['image','csv','html','pdf','json']
  gcs_uri: string | null (null if not stored)
  created_by_agent: string
  description: string
  retention_expires_at: datetime | null

Schedule:
  id: string
  user_id: ref(User)
  cron/rrule: string
  task_type: ['report','alert','sync']
  config: {...}

DataAccessLog:
  id: string
  user_id: ref(User)
  source: 'fi-mcp' | 'public-data' | ...
  purpose: string
  accessed_at: datetime
  session_id: ref(ChatSession)
```

**APIs & Integrations (FastAPI)**
*All external calls hit the Primary Agent; sub-agents are never exposed as HTTP endpoints.*

* **POST /chat/sessions** – create a new chat session. User is derived from Firebase token; returns `session_id`.
* **GET /chat/sessions** – list user sessions (pagination, search by title/date).
* **GET /chat/sessions/{session\_id}** – fetch session metadata and optionally last N messages.
* **POST /chat/sessions/{session\_id}/messages** – send a user message; stream assistant output (SSE/WebSocket). Primary Agent orchestrates sub-agents internally and finally calls Finalise Response Agent.
* **GET /chat/sessions/{session\_id}/messages** – paginate messages (`before`/`after` cursors).
* **DELETE /chat/sessions/{session\_id}** – archive/soft delete a session.
* **GET /artifacts/{artifact\_id}/signed-url** – return a temporary signed GCS URL to view/download artifacts.
* **POST /schedules** / **PATCH /schedules/{id}** / **DELETE /schedules/{id}** – CRUD for periodic agent tasks (reports, alerts, syncs).
* **POST /sync/personal** – optional manual trigger to refresh FI-MCP data.
* **POST /hooks/pubsub/agent-run** – internal endpoint for Cloud Tasks/Workflows to kick off background agent runs.
* **/healthz**, **/readiness** – health probes for Cloud Run/GKE.

**Infrastructure Requirements**

* Cloud Run (FastAPI, code-exec microservice).
* Pub/Sub + Cloud Scheduler for async jobs.
* Firestore/BigQuery/GCS for data.
* Secret Manager for credentials.
* VPC + Serverless VPC Access for private services if needed.
* IAM roles per service; least privilege.

# Development Roadmap

**Phase 0 – Foundations**

* Repo setup (monorepo or polyrepo), CI/CD (Cloud Build/GitHub Actions).
* Firebase Auth integration, base FastAPI skeleton, Firestore schemas.
* python-adk orchestration skeleton with dummy tools.
* Infrastructure as code (Terraform) for GCP resources.

**Phase 1 – MVP (Usable Chat + Personal Data)**

* Integrate FI-MCP; Personal Finance Agent end-to-end (connect → fetch → store).
* Primary chat endpoint (text only) with simple summarization.
* Basic visualization (bar/pie charts) via Visualization Agent.
* Artifact storage + retrieval.
* Manual sync endpoint.

**Phase 2 – Public Data & Benchmarking**

* Public Data Agent (market indices, inflation, news).
* Portfolio benchmarking + simple recommendations.
* Goal definition + tracking UI.
* Basic scheduler: user-configurable weekly/monthly reports.

**Phase 3 – Advanced Analysis & Planning**

* Python Analysis Agent with sandboxed code execution + caching.
* Monte Carlo simulations, tax calculators.
* Finalise Response Agent polishing output formats (cards, charts, TL;DR).
* Alerting engine (thresholds, anomalies).

**Phase 4 – Hardening & Growth Features**

* Multi-language support.
* Family/shared views & export packs.
* Webhooks/API for power users.
* Performance optimizations (vector cache of chats, BigQuery ML for patterns).
* Security audits, SOC2 style logging, backup & DR plans.

# Logical Dependency Chain

1. **Identity & Data Store** → Firebase Auth, Firestore schemas.
2. **Backend Skeleton & Agent Orchestration** → FastAPI + python-adk core.
3. **Personal Data Integration** → FI-MCP sync & normalization.
4. **Chat UX + Simple Responses** → Get something user-visible ASAP.
5. **Artifacts/Visualization Pipeline** → Charts & signed URLs.
6. **Public Data + Benchmarking** → Broaden insight surface.
7. **Scheduler/Reports** → Automate value delivery.
8. **Advanced Analysis (MC, tax, optimizations)** → Deep value.
9. **Refine Finalise Agent & UX polish** → Trust & delight.

# Risks and Mitigations

* **Data Privacy/Compliance (Highest):** We handle sensitive finance data but do not store it. Mitigation: on-demand fetch, in-memory processing, redaction, explicit per-session consent, short-lived caches, GCS lifecycle rules.
* **Tool/Agent Latency & Cost:** Batch calls, cache non-sensitive public data, progressive disclosure of results.
* **Consent Drift/Mismatch:** Snapshot consent into each session; allow override prompts; audit via DataAccessLog.
* **MCP/Integration Fragility:** Versioned adapters, retries/backoff, health checks.
* **Visualization Sandbox Security:** Isolated runtime (Cloud Run jobs/Firecracker), resource/time limits, no outbound internet.
* **MVP Scope Creep:** Define MVP as chat + on-demand analysis without persistence; backlog extras.

# Appendix

* **Research Notes:** Indian finance APIs (Account Aggregator ecosystem), tax rule datasets, benchmark indices list.
* **Tech Specs:**

  * Streaming: Server-Sent Events (SSE) or WebSocket from FastAPI.
  * Code Exec: Restricted Python env, no internet, whitelisted libs (pandas, numpy, matplotlib, plotly).
  * Data Schemas: Prefer JSON schemas + pydantic models.
  * Observability: Trace each agent/tool call with IDs surfaced in UI for debugging.
* **Future Ideas:** RL-based personal finance coach, plugin marketplace for external advisors, on-device inference for privacy.

  </PRD>
