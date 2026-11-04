# Shatwik Sarthak

**Full-Stack, Distributed Systems & Applied AI Engineer**
Bengaluru, India • [LinkedIn](https://www.linkedin.com/in/shatwik-sarthak-b6121b2a6/) • [GitHub](https://github.com/shatwiks) • [Email](mailto:shatwik7@gmail.com)

> Focus: Scalable distributed web architectures (Node.js, TypeScript, PostgreSQL, Redis) coupled with production AI/ML systems (Advanced RAG, Model Serving, Agent Workflows) and low-latency data pipelines.

---

### About

B.Tech student in Computer Science and Engineering at **Manipal Institute of Technology (MIT) Bengaluru** (2024 to 2028). I build systems that stay correct under load: atomic inventory gates, real-time sync, streaming ingestion, and retrieval pipelines that are measured rather than guessed. Tech Solstice 48-Hour National Hackathon finalist (Top 5 of 120+ teams).

---

### Technical Capabilities

| Domain | Stack & Infrastructure |
| :--- | :--- |
| **Languages** | Python (Asyncio, Pydantic), TypeScript, JavaScript (ES6+), C++, C, SQL |
| **Backend & Distributed Systems** | Node.js, Express, FastAPI, Redis (Lua scripting, Redlock, Pub/Sub, Semantic Caching), WebSockets (Socket.io), SSE, REST APIs, Microservices, Saga pattern, idempotency keys |
| **Data Pipelines & Streaming** | WebSocket ingestion, deduplication and replay recovery, dead-letter handling, ClickHouse (materialized views, ASOF joins) |
| **Frontend Architecture** | React, Next.js (App Router, Server Actions), TanStack Query, Zustand, Redux Toolkit, Tailwind CSS, HTML5, CSS3 |
| **AI & Machine Learning** | PyTorch, Hugging Face Transformers, LangGraph, vLLM, Dense Vector Embeddings, Cohere Rerank, RAG, Agentic AI, Prompt Engineering, Pandas, Scikit-learn |
| **Databases & Vector Stores** | PostgreSQL, Prisma ORM, MySQL, MongoDB Atlas Vector Search, Pinecone, Redis |
| **Cloud & DevOps** | Docker (Multi-stage builds), AWS (ECS Fargate, EC2, S3, RDS, CloudFront), GitHub Actions (CI/CD), Linux/POSIX, NGINX |
| **Testing & Practices** | PyTest, Jest, Ragas, DeepEval, k6 load testing, Observability, Agile (Scrum, Kanban) |
| **AI-Assisted Development** | GitHub Copilot, Claude Code, Cline, Aider |

---

### Featured Systems & Production Repositories

#### 1. [Distributed Flash-Sale and Cloud Checkout Engine](https://github.com/shatwiks/distributed-flash-sale-engine) • [Live Demo](https://distributed-flash-sale-engine-bj7q.vercel.app/)
*A high-contention checkout engine built to sell limited stock under burst traffic without overbooking.*
* **Architecture:** O(1) atomic Redis Lua stock gate with Redlock distributed locking, PostgreSQL for durable orders, Dockerized services on AWS.
* **Impact & Metrics:** Sustained **10,000+ RPS** burst traffic with **0.00% overbooking**; cut **p95 latency by 93%** (271 ms to 18.5 ms) by replacing PostgreSQL row locks (`SELECT FOR UPDATE`), removing deadlocks and cascading timeouts.
* **Reliability:** Saga-style rollbacks (`INCRBY`) keep Redis and PostgreSQL consistent on write failures; two-tier idempotency keys block duplicate payment requests; TOCTOU race conditions eliminated.
* `TypeScript` `Node.js` `PostgreSQL` `Redis` `Docker` `AWS` `k6`

#### 2. PolyPulse: Cross-Venue Prediction-Market Orderbook & Markout Pipeline *(in progress)*
*Low-latency ingestion, orderbook and wallet-markout engine for Polymarket and Kalshi.*
* **Architecture:** Cache-aligned C++20 orderbook with AVX2 intrinsics normalizing Kalshi bid-only books (`YES Ask = 1.00 - NO Bid`); async ingestion with heartbeat watchdog, sequence-gap snapshot recovery and stable-key dedup; Polygon `OrderFilled` decoding; ClickHouse `AggregatingMergeTree` materialized views with `ASOF LEFT JOIN` for 5s/30s/60s post-trade markouts; React trading terminal with Web Worker parsing.
* **Status:** Benchmarks are being collected; results will be published in the repo README.
* `C++20` `ClickHouse` `Python` `TypeScript` `WebSockets`

#### 3. [Real-Time Commerce and Delivery Platform](https://github.com/shatwiks/Real-Time-Commerce-and-Web-Application-Platform) • [Live Demo](https://food-full-stack-kappa.vercel.app/)
*Food ordering and live delivery platform with a responsive React/TypeScript storefront.*
* **Architecture:** Event-driven pub/sub over Socket.io namespaces with room isolation; Express middleware; cloud PostgreSQL (Neon) via Prisma, deployed across Vercel and Render.
* **Impact & Metrics:** Order-lifecycle sync under **50 ms** across **1,500+** simulated sessions; **p95 catalog query latency cut by 64%** with compound indexes and connection pooling.
* **Security:** Email 2FA/OTP, signed HTTP-only JWT sessions and parameterized middleware eliminated authorization tampering in testing.
* `React` `TypeScript` `Node.js` `PostgreSQL` `Socket.io` `Prisma`

#### 4. [PayGuard AI: Agentic Payment Triage and RAG Engine](https://github.com/shatwiks/PayGuard-AI-Agentic-Payment-Triage-RAG-Engine)
*AI-powered triage and analytics assistant for payment operations, with Agile sprint reporting and KPI tracking.*
* **Architecture:** Agentic RAG engine orchestrating LLMs with few-shot and structured JSON prompts, context management and Text-to-SQL over PostgreSQL and MongoDB.
* **Impact & Metrics:** Cut payment-triage time by **65%** at **92% query accuracy**.
* **Safety:** PII token masking, regex-based redaction of emails and tokens, read-only SQL validation and sandboxing, and real-time observability before and after LLM inference.
* `Python` `FastAPI` `PostgreSQL` `MongoDB` `LLM APIs`

---

### Hackathons & Experience

**Team Lead & National Finalist, Tech Solstice 48-Hour Hackathon** • Bengaluru • March 2026 • *Top 5 of 120+ teams*
* Led the build of **DisasterSync**, an offline-first disaster coordination and operational reporting system, from concept to working product in 48 hours using an Agile (Kanban/Scrum) workflow.
* Built local mesh synchronization with WebSockets, WebRTC and IndexedDB that auto-syncs stored telemetry to cloud PostgreSQL once connectivity returns.
* Shipped real-time status dashboards and automated alert triage for field teams.

---

### Certifications & Achievements

* Supervised Machine Learning: Regression and Classification (DeepLearning.AI / Coursera)
* Generative AI, LLMs, RAG & Prompt Engineering Foundations
* 200+ DSA, OOP and SQL problems solved on LeetCode and HackerRank
* Active contributor to campus coding and AI/ML technical societies at MIT Bengaluru (GitHub workflows, code reviews, hackathon prototyping)

---

### Engineering Principles

* **Systems Over Wrappers:** Building resilient background task queues, distributed caches, and streaming protocols rather than relying on synchronous, brittle API calls.
* **Deterministic AI:** Guarding non-deterministic LLM behavior through strict schema validation (Pydantic/Zod), context-precision scoring, and automated CI/CD hallucination tests.
* **Clean Code & Git Hygiene:** Writing conventional, semantic commits (`feat:`, `fix:`, `refactor:`), maintaining comprehensive READMEs with architecture diagrams, and deploying reproducible Docker configurations.

---

### What I'm Focused On

* Low-latency data systems: streaming ingestion, orderbooks, and real-time analytics.
* Solving advanced algorithmic problems across Graphs, Dynamic Programming, and Low-Level Design.
* Contributing to open-source agentic frameworks and low-latency local model inference engines.
* Preparing for entry-level Software Development Engineer (SDE) and Full-Stack AI/ML roles.

---

### Contact

[LinkedIn](https://www.linkedin.com/in/shatwik-sarthak-b6121b2a6/) • [GitHub](https://github.com/shatwiks) • [shatwik7@gmail.com](mailto:shatwik7@gmail.com)
