<!-- Save this as README.md in a repo named exactly like your username: github.com/shatwiks/shatwiks -->

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=220&section=header&text=Shatwik%20Sarthak&fontSize=56&fontColor=ffffff&animation=fadeIn&fontAlignY=36&desc=Backend%20%E2%80%A2%20Distributed%20Systems%20%E2%80%A2%20Applied%20AI&descAlignY=58&descSize=20" width="100%" alt="Shatwik Sarthak banner" />

<a href="https://git.io/typing-svg">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&duration=3000&pause=1000&color=00F7FF&center=true&vCenter=true&width=720&lines=Full-Stack+%2B+Distributed+Systems+Engineer;Redis+Lua+%7C+10%2C000%2B+RPS+%7C+0.00%25+overbooking;Low-latency+C%2B%2B20+%2B+ClickHouse+pipelines;RAG+%2B+Agentic+AI+systems+that+are+measured;CS+%40+MIT+Bengaluru+%7C+Class+of+2028" alt="Typing animation" />
</a>

<br/>

<img src="https://komarev.com/ghpvc/?username=shatwiks&label=Profile+views&color=7c3aed&style=for-the-badge" alt="Profile views" />
<a href="https://www.linkedin.com/in/shatwik-sarthak-b6121b2a6/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
<a href="mailto:shatwik7@gmail.com"><img src="https://img.shields.io/badge/Email-FF2D95?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" /></a>
<a href="https://github.com/shatwiks"><img src="https://img.shields.io/badge/GitHub-00F7FF?style=for-the-badge&logo=github&logoColor=black" alt="GitHub" /></a>

</div>

---

## ⚡ About Me

B.Tech student in **Computer Science and Engineering at Manipal Institute of Technology (MIT) Bengaluru** (2024 to 2028).
I build systems that stay correct under load: atomic inventory gates, real-time sync, streaming ingestion, and retrieval pipelines that are measured rather than guessed.

- 🏆 **Tech Solstice 48-Hour National Hackathon** finalist, Top 5 of 120+ teams
- ⚙️ Focus: scalable distributed web architectures (Node.js, TypeScript, PostgreSQL, Redis) plus production AI/ML systems (Advanced RAG, model serving, agent workflows)
- 🚀 Building **PolyPulse**, a C++20 + ClickHouse prediction-market orderbook and markout pipeline
- 🎯 Preparing for entry-level SDE and Full-Stack AI/ML roles

---

## 🛠️ Tech Stack

<div align="center">

**Languages & Frontend**

<img src="https://skillicons.dev/icons?i=py,ts,js,cpp,c,react,nextjs,tailwind,redux&perline=9" alt="Languages and frontend" />

**Backend & Databases**

<img src="https://skillicons.dev/icons?i=nodejs,express,fastapi,postgres,mysql,mongodb,redis,prisma&perline=8" alt="Backend and databases" />

**Cloud, DevOps & AI**

<img src="https://skillicons.dev/icons?i=docker,aws,githubactions,linux,nginx,git,vercel,pytorch&perline=8" alt="Cloud DevOps and AI" />

<br/>

<img src="https://img.shields.io/badge/ClickHouse-FFCC01?style=for-the-badge&logo=clickhouse&logoColor=black" alt="ClickHouse" />
<img src="https://img.shields.io/badge/Hugging_Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black" alt="Hugging Face" />
<img src="https://img.shields.io/badge/LangGraph-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" alt="LangGraph" />
<img src="https://img.shields.io/badge/vLLM-7C3AED?style=for-the-badge" alt="vLLM" />
<img src="https://img.shields.io/badge/Pinecone-000000?style=for-the-badge" alt="Pinecone" />
<img src="https://img.shields.io/badge/Socket.io-010101?style=for-the-badge&logo=socketdotio&logoColor=white" alt="Socket.io" />
<img src="https://img.shields.io/badge/WebRTC-333333?style=for-the-badge&logo=webrtc&logoColor=white" alt="WebRTC" />
<img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas" />
<img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white" alt="scikit-learn" />
<img src="https://img.shields.io/badge/k6-7D64FF?style=for-the-badge&logo=k6&logoColor=white" alt="k6" />

</div>

| Domain | Details |
| :--- | :--- |
| **Distributed Systems** | Redis (Lua scripting, Redlock, Pub/Sub, semantic caching), Saga pattern, idempotency keys, TOCTOU race-condition elimination, eventual consistency, microservices |
| **Data Pipelines & Streaming** | WebSocket ingestion, deduplication and replay recovery, dead-letter handling, ClickHouse materialized views and ASOF joins, SSE |
| **AI & ML** | RAG, agentic AI, prompt engineering, dense embeddings, Cohere Rerank, Ragas, DeepEval |
| **Testing & Practices** | PyTest, Jest, k6 load testing, observability, Agile (Scrum, Kanban), conventional commits |
| **AI-Assisted Development** | GitHub Copilot, Claude Code, Cline, Aider |

---

## 🚀 Featured Projects

### 1. [Distributed Flash-Sale and Cloud Checkout Engine](https://github.com/shatwiks/distributed-flash-sale-engine) • [Live Demo](https://distributed-flash-sale-engine-bj7q.vercel.app/)
*A high-contention checkout engine built to sell limited stock under burst traffic without overbooking.*

- **Architecture:** O(1) atomic Redis Lua stock gate with Redlock distributed locking, PostgreSQL for durable orders, Dockerized services on AWS
- **Impact:** sustained **10,000+ RPS** with **0.00% overbooking**; cut **p95 latency by 93%** (271 ms to 18.5 ms) by replacing PostgreSQL row locks (`SELECT FOR UPDATE`)
- **Reliability:** Saga-style rollbacks (`INCRBY`) keep Redis and PostgreSQL consistent on write failures; two-tier idempotency keys block duplicate payments

![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=nodedotjs&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat-square&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazonwebservices&logoColor=white)

### 2. PolyPulse: Cross-Venue Prediction-Market Orderbook & Markout Pipeline 🚧 *(in progress)*
*Low-latency ingestion, orderbook and wallet-markout engine for Polymarket and Kalshi.*

- **Orderbook:** cache-aligned C++20 book with AVX2 intrinsics, normalizing Kalshi bid-only books (`YES Ask = 1.00 - NO Bid`)
- **Ingestion:** async pipeline with heartbeat watchdog, sequence-gap snapshot recovery, stable-key dedup, and Polygon `OrderFilled` decoding
- **Analytics:** ClickHouse `AggregatingMergeTree` materialized views with `ASOF LEFT JOIN` for 5s/30s/60s post-trade markouts; React terminal with Web Worker parsing
- **Status:** benchmarks being collected, results coming to the repo README

![C++20](https://img.shields.io/badge/C++20-00599C?style=flat-square&logo=cplusplus&logoColor=white)
![ClickHouse](https://img.shields.io/badge/ClickHouse-FFCC01?style=flat-square&logo=clickhouse&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)

### 3. [CogniSync: Enterprise Hybrid-Search RAG Platform](https://github.com/shatwiks)
*Distributed hybrid-search retrieval engine combining sparse lexical matching with dense vector indexing.*

- **Architecture:** Next.js 15 streaming interface, Node.js API gateway, containerized FastAPI inference microservice, MongoDB Atlas Vector Search
- **Impact:** context retrieval precision from 58% to 94% with Cohere cross-encoder re-ranking; sub-380ms time-to-first-token via SSE
- **Reliability:** Ragas and DeepEval regression benchmarks in GitHub Actions; 36% lower LLM API spend through Redis semantic caching

![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB_Atlas-47A248?style=flat-square&logo=mongodb&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat-square&logo=redis&logoColor=white)

### 4. [Synapse: Real-Time Collaborative Canvas & Agent Hub](https://github.com/shatwiks)
*Multiplayer workspace with state-synchronized canvas operations and streaming multimodal AI assistance.*

- **Architecture:** React canvas, Node.js WebSocket gateway, Redis Pub/Sub, CRDTs via Yjs, Gemini multimodal API
- **Impact:** sub-40ms sync latency across 50+ concurrent users per room with zero state divergence

![React](https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black)
![WebSockets](https://img.shields.io/badge/WebSockets-010101?style=flat-square)
![Yjs](https://img.shields.io/badge/Yjs-7C3AED?style=flat-square)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)

### 5. [OmniServe: High-Throughput Quantized LLM Inference Gateway](https://github.com/shatwiks)
*Reverse-proxy inference gateway with dynamic batching, sliding-window rate limiting and prompt-injection mitigation.*

- **Architecture:** FastAPI, vLLM with PagedAttention, INT4/INT8 quantization, Redis token-bucket rate limiter
- **Impact:** benchmarked at 2,400 req/sec; 65% lower GPU memory with zero loss in output quality

![vLLM](https://img.shields.io/badge/vLLM-7C3AED?style=flat-square)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=flat-square&logo=prometheus&logoColor=white)
![AWS ECS](https://img.shields.io/badge/AWS_ECS-FF9900?style=flat-square&logo=amazonecs&logoColor=white)

### 6. [Real-Time Commerce and Delivery Platform](https://github.com/shatwiks/Real-Time-Commerce-and-Web-Application-Platform) • [Live Demo](https://food-full-stack-kappa.vercel.app/)
*Food ordering and live delivery platform with a responsive React/TypeScript storefront.*

- **Architecture:** event-driven Socket.io (namespaces, room isolation), Express middleware, Neon PostgreSQL via Prisma, deployed on Vercel and Render
- **Impact:** order-lifecycle sync under **50 ms** across **1,500+** simulated sessions; **p95 catalog query latency down 64%** with compound indexes and pooling
- **Security:** email 2FA/OTP, signed HTTP-only JWT sessions, parameterized middleware

![React](https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black)
![Socket.io](https://img.shields.io/badge/Socket.io-010101?style=flat-square&logo=socketdotio&logoColor=white)
![Prisma](https://img.shields.io/badge/Prisma-2D3748?style=flat-square&logo=prisma&logoColor=white)

### 7. [PayGuard AI: Agentic Payment Triage and RAG Engine](https://github.com/shatwiks/PayGuard-AI-Agentic-Payment-Triage-RAG-Engine)
*AI assistant for payment operations with Agile sprint reporting and KPI tracking.*

- **Architecture:** agentic RAG engine orchestrating LLMs with few-shot and structured JSON prompts and Text-to-SQL over PostgreSQL and MongoDB
- **Impact:** cut payment-triage time by **65%** at **92% query accuracy**
- **Safety:** PII token masking, read-only SQL validation and sandboxing, real-time observability

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=flat-square&logo=mongodb&logoColor=white)

---

## 🏆 Hackathons & Achievements

**Team Lead & National Finalist, Tech Solstice 48-Hour Hackathon** • Bengaluru • March 2026 • *Top 5 of 120+ teams*

- Led the build of **DisasterSync**, an offline-first disaster coordination and reporting system, from concept to working product in 48 hours
- Local mesh synchronization with WebSockets, WebRTC and IndexedDB, auto-syncing stored telemetry to cloud PostgreSQL once connectivity returns
- Real-time status dashboards and automated alert triage for field teams

**Certifications & more**

- 🎓 Supervised Machine Learning: Regression and Classification (DeepLearning.AI / Coursera)
- 🎓 Generative AI, LLMs, RAG & Prompt Engineering Foundations
- 🧩 200+ DSA, OOP and SQL problems solved on LeetCode and HackerRank
- 🤝 Active contributor to campus coding and AI/ML societies at MIT Bengaluru

---

## 📊 GitHub Stats

<div align="center">

<img height="180" src="https://github-readme-stats.vercel.app/api?username=shatwiks&show_icons=true&theme=tokyonight&hide_border=true&bg_color=0D1117" alt="GitHub stats" />
<img height="180" src="https://github-readme-stats.vercel.app/api/top-langs/?username=shatwiks&layout=compact&theme=tokyonight&hide_border=true&bg_color=0D1117" alt="Top languages" />

<img src="https://streak-stats.demolab.com?user=shatwiks&theme=tokyonight&hide_border=true&background=0D1117" alt="GitHub streak" />

<img src="https://github-readme-activity-graph.vercel.app/graph?username=shatwiks&theme=tokyo-night&hide_border=true&bg_color=0D1117&area=true" alt="Contribution graph" width="100%" />

</div>

### 🐍 Contribution Snake

<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/shatwiks/shatwiks/output/github-contribution-grid-snake-dark.svg" />
    <img alt="Contribution snake" src="https://raw.githubusercontent.com/shatwiks/shatwiks/output/github-contribution-grid-snake.svg" />
  </picture>
</div>

---

## 🧠 Engineering Principles

- **Systems over wrappers:** resilient background queues, distributed caches and streaming protocols instead of brittle synchronous API calls
- **Deterministic AI:** guarding non-deterministic LLM behavior with strict schema validation (Pydantic/Zod), context-precision scoring and automated hallucination tests in CI
- **Clean code & Git hygiene:** semantic commits (`feat:`, `fix:`, `refactor:`), READMEs with architecture diagrams, reproducible Docker configs

## 🎯 Currently Focused On

- Low-latency data systems: streaming ingestion, orderbooks and real-time analytics
- Advanced algorithms across graphs, dynamic programming and low-level design
- Contributing to open-source agentic frameworks and local model inference engines

---

<div align="center">

### 📫 Let's connect

<a href="https://www.linkedin.com/in/shatwik-sarthak-b6121b2a6/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
<a href="mailto:shatwik7@gmail.com"><img src="https://img.shields.io/badge/Email-FF2D95?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" /></a>
<a href="https://github.com/shatwiks"><img src="https://img.shields.io/badge/GitHub-00F7FF?style=for-the-badge&logo=github&logoColor=black" alt="GitHub" /></a>

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=120&section=footer" width="100%" alt="footer" />

</div>
