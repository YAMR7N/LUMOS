## 📄 Specification (v 0.9)  
“A month-long sprint plan to ship a demo-ready, graph-savvy study-assistant”

---

### 1. Purpose & Scope  
Turn user-uploaded notes (handwritten pages, PDFs, photos) into a chat-first knowledge base that can:  

1. **Answer questions** with citations (RAG).  
2. **Re-draw figures/graphs** in a clean, branded style via Napkin.  
3. Let users **export** regenerated notes as DOCX/PDF.  

Target demo date: **T + 30 days** (four 1-week iterations).

---

### 2. System Architecture  

```
┌────────────────────────┐        ┌─────────────────────────┐
│     React SPA (Vite)   │◀──────▶│ FastAPI Gateway (ASGI)  │
└────────────────────────┘  WS/HTTP└────────────────▲────────┘
        ▲     ▲                                   │
        │     │                                   │
        │  PushNotif (Cloud Functions)            │
        │                                         │
┌───────┴────────┐        ┌────────────────────────┴─────────┐
│  Firebase Auth │        │   Task Queue (Redis + RQ)        │
└───────▲────────┘        └──────────────▲───────────────────┘
        │                                 │
        │ JWT                             │
        │                                 │
┌───────┴────────┐   gRPC/REST   ┌────────┴─────────┐
│ OCR Service    │──────────────▶│ChartOCR Service  │  (optional GPU)
│  (Paddle-Lite) │              └────────┬─────────┘
└───────▲────────┘                       │
        │ JSON(text,svg)                 │
        │                                 │
┌───────┴────────┐    REST/WS     ┌───────┴────────┐
│   R2R-Light    │───────────────▶│  Vector DB     │ (pgvector or Qdrant)
└───────▲────────┘                └───────▲────────┘
        │                                 │
        │            OpenAI / Ollama      │
        └──────────────┬──────────────────┘
                       ▼
                GPT-4o  |  Llama-3-8B
```

* **FastAPI** replaces Flask for native ASGI WebSockets.  
* **RQ + Redis** decouples heavy OCR & Napkin polling from chat.  
* **Napkin API** called asynchronously after ChartOCR returns data-tables.  
* **Observability**: OpenTelemetry side-car → Grafana Cloud; Sentry for FE/BE errors.  

---

### 3. Component Specs  

| Layer | Tech / Version | Key Responsibilities | Acceptance Criteria |
|-------|----------------|----------------------|---------------------|
| **Frontend** | React 19, Vite 5, Tailwind 3 | Chat UI, file-drop zone, live progress, “Regenerate Figure” modal. | Full keyboard nav; WCAG AA contrast; bundle < 250 kB gzip. |
| **Auth & State** | Firebase Auth + Firestore | User sessions, note metadata, job status. | CRUD latency ≤ 150 ms P90; security rules block cross-user reads. |
| **Gateway** | FastAPI 0.111 + Uvicorn | Auth guard, rate-limit, REST & WS endpoints, queues jobs. | > 1 k concurrent WS clients on M-t2.medium. |
| **OCR** | PaddleOCR ultra-lite CPU build | Extract text/diagrams; return SVG/JSON. | ≤ 8 s for 5-page PDF on MacBook M1; confidence metric exposed. |
| **ChartOCR** | chart-ocr 0.4 | Recover data tables from bar/line/pie charts. | ≥ 85 % recall on sample set; returns structured JSON. |
| **Retrieval** | R2R-Light 0.3.4 | Chunk, embed (OpenAI ada-3 or cohere), hybrid search. | BM25+vector top-k recall ≥ 0.8 vs. ground truth. |
| **Vector DB** | pgvector 0.6 **or** Qdrant 1.9 | Store embeddings. | 99-percentile search ≤ 300 ms for 1 M docs. |
| **LLM** | GPT-4o 2025-06 (hosted) **and** Llama-3-8B-Instruct via Ollama 0.2 | Generate chat answers, Napkin prompts. | Streaming TTFB < 1 s; cost guard blocks > 30 K tokens/user/day. |
| **Figure Render** | Napkin API 2025-Q2 | Turn prompt+table → SVG. | 95 % jobs < 10 s; SVG cached & accessible 30 days. |
| **Export** | python-docx 1.2 + pdfkit | Compose DOCX/PDF; upload to Firebase Storage. | DOCX gen < 4 s for 10 pages; links auto-expire. |
| **CI/CD** | GitHub Actions + Hatchling | Lint, test, build Docker images, deploy to Fly.io staging. | Pipeline < 10 min; zero-downtime blue/green. |

---

### 4. Non-functional Requirements  

* **Security**:  
  * HTTPS enforced; HSTS; OWASP top-10 tested via ZAP.  
  * Secrets in Fly.io secrets store; rotated weekly.  
  * “Delete my uploads” API + GDPR 30-day TTL.  

* **Observability & Cost Guardrails**:  
  * Prometheus metrics: `ocr_latency`, `llm_tokens`, `napkin_jobs`.  
  * Alerts: Firestore reads > 50 K/day, GPT spend > $25/day.  

* **Accessibility**: alt-text from LLM stored with every figure; roles & ARIA labels.  

* **Failover**: if Napkin or ChartOCR fails, raw PNG is embedded with warning banner.

---

### 5. Risk Register & Mitigations  

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Napkin rate-limit exceeded | Med | Figures don’t load | Cache by hash; queue retries; fallback to original image |
| PaddleOCR accuracy on messy handwriting | High | Wrong answers | Confidence threshold τ = 0.6 triggers human-select crop tool |
| Firestore cost blow-up | Med | $$ | Batched writes, indexed queries, daily spend alert |
| Vector DB > RAM | Low (30 days) | Latency | Use Qdrant cloud if embeddings > 2 M |

---

## 📆 30-Day Timeline (work-week cadence)

| Week | Milestones & Deliverables | Owner(s) |
|------|---------------------------|----------|
| **0 – Kick-off** (Fri) | - Finalise spec & repos<br>- Request Napkin token<br>- Install dev-containers | All |
| **1 – Foundations** | - FastAPI skeleton + Auth guard<br>- React scaffold, file-upload flow<br>- Docker Compose v1: FE, BE, Redis | FE, BE |
| **2 – Core AI Loop** | - PaddleOCR ultra-lite service<br>- R2R-Light running with pgvector<br>- Chat WS streaming answers via GPT-4o<br>- First green-to-red end-to-end demo | ML, BE |
| **3 – Figure Pipeline** | - ChartOCR container<br>- GPT prompt → Napkin API integration<br>- Regenerate Figure UI<br>- Celery/RQ workers & retries | ML, FE |
| **4 – Polish & Guardrails** | - Observability stack (Grafana, Sentry)<br>- Cost/budget alerts<br>- Docx/PDF export feature<br>- Accessibility QA, keyboard nav | Dev Ops, QA |
| **5 – Hardening** | - Load test: 1 k concurrent users<br>- Security scan + pen-test fixes<br>- Beta user feedback loop | Dev Ops |
| **6 – Launch Week** | - Bug triage & performance tweaks<br>- Demo script & slide deck<br>- Freeze by Thursday; dry-run Friday | All |

*Daily stand-ups at 10:00 AM (Africa/Cairo). Retro each Friday 4:00 PM.*

---

### 6. Success Criteria  

* **Demo judges** upload a 5-page scanned worksheet and receive:  
  1. Instant progress feedback (< 3 s).  
  2. Accurate answer to a content question with citations (< 10 s).  
  3. Click “Recreate Figure” → SVG appears, matches data, consistent branding.  
* System stays within **$50 cloud budget** for the month.  
* P95 end-to-end question latency **< 15 s**.  

---

*Print this, tape it above the coffee machine, and let the shipping commence. 🛠️*
