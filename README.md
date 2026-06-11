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

