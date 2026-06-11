# 🦅 Nigeria Revenue Service (NRS) - Tax Integrity & Audit Intelligence System
### Full-Stack Enterprise Audit Engine, REST API, & Columnar Data Pipeline

An automated, data-driven compliance and risk-scoring platform engineered to ingest corporate tax filings, execute high-speed text normalization, detect systemic tax irregularities, and maintain a high-performance Apache Parquet data layer.

---

## 🚀 Live Production System
* **Interactive UI Dashboard:** [https://nrs-automated-audit-pipeline-c7xrbfwfk4agwin8h54dv5.streamlit.app/]
* **API Documentation Gateway:** `http://localhost:8000/docs` (Local Development)

---

## 🛠️ Core System Architecture & Engineering Features

* **High-Performance Columnar Storage Architecture:** Reengineered the underlying data persistence layer from legacy flat CSV files into optimized, binary **Apache Parquet** (`nrs_audited_results.parquet`) powered by the `pyarrow` engine, resulting in sub-millisecond data I/O performance.
* **Automated Data Migration & Anti-Crash Pipeline:** Built a defensive data initialization layer that detects legacy assets on system startup, dynamically normalizes column headers (`strip()`, `lower()`, and `replace(" ", "_")`), and auto-generates a baseline fallback matrix if a cold boot occurs.
* **Dynamic Risk-Coefficient Matrix:** Features a programmatic audit heuristic that flags corporate entities under review (`risk_score > 0.65`), isolating accounts showing severe deviation from effective corporate tax rates.
* **Decoupled REST API Architecture:** Structured a robust **FastAPI Gateway** serving cross-origin secure data streaming endpoints (`/api/v1/audit-data`), entirely separating raw business logic processing from presentation states.
* **Interactive Executive Intelligence Visualizations:** Leveraged the `plotly.express` engine to render interactive real-time multi-variable graphs, including corporate risk profile curves and revenue vs. tax paid distribution benchmarks.

---

## 🏗️ Technical Stack & Dependencies

* **Core Backend Engine:** FastAPI (0.110.0), Uvicorn (0.28.0), Pydantic (2.6.4)
* **Data Engineering & Serialization:** Pandas (2.2.1), PyArrow (15.0.0)
* **Frontend Presentation Layer:** Streamlit (1.32.0), Plotly (5.19.0), Requests (2.31.0)
* **Target Container Environment:** Python 3.11 Standard Linux Container Architecture

---

---

## 🖥️ Local Installation & Deployment Guide

Follow these steps to run the decoupled full-stack architecture inside your local workspace environment:

### 1. Environment Setup & Dependency Installation
Clone this repository to your machine, open your terminal workspace, and install the compiled requirements file:
pip install -r requirements.txt

### 2. Launch the FastAPI Backend Service
Boot up the high-speed data stream API layer using the Uvicorn ASGI server interface:
uvicorn main:app --reload --port 8000

*The backend will automatically check, clean, and initialize the Apache Parquet storage cache instantly upon activation.*

### 3. Launch the Streamlit Analytics Interface
In a separate terminal or split panel window, spin up the browser-based visualization dashboard:
streamlit run ui.py

---

## 📋 Standardized Data Schema (Lower Snake Case)

| Column Variable Name | Data Type | Engineering Description |
| :--- | :--- | :--- |
| taxpayer_id | String | Unique statutory alphanumeric tax identifier |
| taxpayer_name | String | Corporate registered trade name / corporate entity |
| reported_revenue | Float | Declared gross institutional revenue earnings (₦) |
| tax_paid | Float | Verified corporate tax remittances processed (₦) |
| risk_score | Float | Algorithmic compliance risk index range (0.00 to 1.00) |
| audit_status | String | System classification vector (Compliant / Under Review) |
