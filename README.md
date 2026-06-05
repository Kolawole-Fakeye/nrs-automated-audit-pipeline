## 🦅 Nigeria Revenue Service (NRS) - Tax Integrity & Audit Intelligence System
### Decoupled Full-Stack Audit Compliance & Fraud Detection Engine

A secure, enterprise-grade tax auditing dashboard designed to ingest corporate financial telemetry, execute integrity validation models, andflag high-risk systemic anomalies. Built using a fully decoupled microservices architecture.

### 🚀 Live Production Interfaces

* **Auditor Interactive Interface:** [Live Streamlit Frontend Dashboard](https://share.streamlit.io/) * **Central Core API Gateway:** Hosted on Render Cloud Infrastructure
  * **API System Status Live Check:** [https://nrs-backend-api.onrender.com/](https://nrs-backend-api.onrender.com/) * **Tax Intelligence Metrics Endpoint:** [https://nrs-backend-api.onrender.com/api/v1/audit/metrics](https://nrs-backend-api.onrender.com/api/v1/audit/metrics)
  * **Interactive API Playground (Swagger UI):** [https://nrs-backend-api.onrender.com/docs](https://nrs-backend-api.onrender.com/docs)

### 🏗️ Systems Architecture & Flow
* **Frontend Layer:** Streamlit runtime processing dynamic web components based on incoming JSON telemetry vectors.
* **Backend Layer:** FastAPI production framework utilizing Pydantic schemas for data validation and isolated algorithmic audit routing.
* **Data Layer:** High-speed serialized data layers for fast processing and zero-cold-start container efficiency.
