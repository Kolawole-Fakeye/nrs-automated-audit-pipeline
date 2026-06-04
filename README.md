# NRS Automated Audit Pipeline

An enterprise-grade, cloud-deployed data processing and visualization pipeline built to automate the auditing processes of the **Federal Inland Revenue Service (FIRS) / Nigeria Revenue Service (NRS)**. 

The system leverages a decoupled architecture: an optimized **FastAPI backend** handles heavy data ingestion, validation, and normalization, while a reactive **Streamlit frontend** serves as an interactive compliance dashboard for senior leadership.

### 🔗 Live Deployments & Previews
* 🚀 **Production Interactive Dashboard:** [https://nrs-automated-audit-pipeline-zjz3bim9bunmg4ncwv5zhn.streamlit.app/](https://nrs-automated-audit-pipeline-zjz3bim9bunmg4ncwv5zhn.streamlit.app/)
* ⚙️ **Production Backend API:** `https://nrs-backend-api.onrender.com/docs`
* 💻 **Active Codespaces Preview:** [Launch Live NRS Audit Dashboard](https://humble-invention-7vgx9gw9g6xwcwqj4-8501.app.github.dev/)

---

## 🏗️ Architecture Overview

The pipeline is split into independent cloud-hosted layers to ensure scalability, high performance, and high availability:

1. **Frontend Dashboard (Streamlit Cloud):** Consumes normalized JSON payloads from the API and translates them into actionable financial metrics, compliance tracking tables, and data visualizations. Includes built-in CSV fallback handling.
2. **Data Storage & Cache Optimization (Apache Parquet):** Automatically migrates legacy tax CSV files into a high-performance, binary columnar Parquet layer upon initialization, dramatically reducing read latency and protecting memory overhead during heavy audit parsing.
3. **Backend API (Render - Dockerized):** Built with FastAPI and containerized via Docker. Manages schema validation, sanitizes column drift from incoming tax records, and exposes structured REST endpoints.

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit, Pandas, Plotly
* **Data Layer:** Apache Parquet, PyArrow
* **Backend:** Python, FastAPI, Uvicorn, Docker
* **Deployment & DevOps:** GitHub, Render (Docker Runtime), Streamlit Community Cloud

---

## 🚀 Local Setup & Installation

To run this project locally, clone the repository and set up both components:

### 1. Prerequisites
Ensure you have Python 3.10+ installed.

### 2. Run the Backend API Engine
Open your terminal and boot up the FastAPI core using Uvicorn. Upon launch, the system automatically checks and builds the optimized Parquet data cache:
```bash
uvicorn main:app --reload --port 8000

3. Run the Frontend Dashboard
Open a second (or split) terminal tab and launch the Streamlit interface:

streamlit run ui.py --server.enableCORS false --server.enableXsrfProtection false

🔒 Environment & Configuration
For production deployment, configure your Streamlit Cloud provider environment variables or secrets with the following key:

NRS_BACKEND_URL = "https://nrs-backend-api.onrender.com/data"

📈 Core Capabilities Demonstrated
High-Performance Data Ingestion: Integrated Apache Parquet to process multi-million row taxpayer ledgers natively with optimized columnar compression.

Containerization: Production deployment utilizing optimized Docker configurations for seamless cloud execution.

Schema Drift Resilience: Ingestion algorithms capable of sanitizing and normalizing unstructured file schemas on the fly (strip(), lower(), replace(" ", "_")).

Decoupled Architecture: Clean separation of concerns between raw analytical processing (API) and presentation layers (UI).

Fault Tolerance: Robust exception mapping to guarantee uninterrupted dashboard operation even during network latency.
