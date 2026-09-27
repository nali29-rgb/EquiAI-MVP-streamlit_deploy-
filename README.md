# ⚖️ EquiAudit AI
> **Algorithmic Bias & EEOC Legal Compliance Audit Engine for Enterprise Hiring Pipelines**

[![Award](https://img.shields.io/badge/Award-Best%20Responsible%20AI%20Solution-gold?style=for-the-badge)](https://davisinstituteai.colby.edu/)
[![Next.js](https://img.shields.io/badge/Frontend-Next.js-000000?style=for-the-badge&logo=nextdotjs)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/AI-GPT--4o-412991?style=for-the-badge&logo=openai)](https://openai.com/)
[![Vercel](https://img.shields.io/badge/Deploy-Vercel-000000?style=for-the-badge&logo=vercel)](https://vercel.com/)
[![Render](https://img.shields.io/badge/Deploy-Render-46E3B7?style=for-the-badge&logo=render)](https://render.com/)

---

## 🏆 Award & Background
Developed as part of the **Davis Institute for Artificial Intelligence Summer Bridges Program** at Colby College. 

EquiAudit AI was built following primary market research and interviews with HR managers to address algorithmic compliance risks in modern Applicant Tracking Systems (ATS). Our team pitched the technical platform and business strategy to an expert panel of judges and was awarded **"Best Responsible AI Solution."**

---

## 🎬 Product Demo Video

[![EquiAudit AI Demo Video](https://img.youtube.com/vi/YOUR_YOUTUBE_ID_HERE/maxresdefault.jpg)](https://www.loom.com/share/YOUR_LOOM_LINK_HERE)

> 📹 **[Click here to watch the full product walkthrough video on Loom / YouTube](https://www.loom.com/share/YOUR_LOOM_LINK_HERE)**

---

## 📌 Problem Statement & Overview
Modern companies rely heavily on automated candidate screening tools embedded inside Applicant Tracking Systems (e.g., Workday, Greenhouse, Lever). However, unmonitored algorithmic scoring, automated knockout filters, and experience thresholds often introduce illegal disparate impact against protected demographic groups.

**EquiAudit AI** solves this problem by allowing recruiting and legal teams to upload candidate progression CSV datasets. The engine automatically:
1. **Computes Exact Adverse Impact Ratios** under federal **EEOC Title VII (4/5ths Rule)** guidelines.
2. **Evaluates Compliance Risks** under state and municipal mandates such as **NYC Local Law 144**.
3. **Generates Platform-Native Remediation Steps** directly executable inside specific ATS settings (Workday, Greenhouse, Lever, SmartRecruiters).

---

## ✨ Key Features
* 📊 **EEOC 4/5ths Rule Calculation**: Dynamically computes demographic applicant totals, advancement rates, selection rates, and adverse impact ratios.
* 🛠️ **Platform-Native Remediation Playbooks**: Leverages OpenAI GPT-4o to generate step-by-step administrative fixes native to the UI workflows of Workday, Greenhouse, Lever, and SmartRecruiters.
* ⚖️ **Legal Exposure Summary**: Generates audit-ready executive protocol notices citing Title VII regulations and NYC Local Law 144 audit requirements.
* ⚡ **Decoupled Architecture**: High-performance FastAPI asynchronous backend paired with a responsive Next.js frontend.

---

## 🏗️ System Architecture

EquiAudit AI utilizes a decoupled client-server architecture designed for high-throughput candidate dataset processing and real-time LLM compliance auditing.

### 📐 High-Level Data Flow

```mermaid
graph TD
    %% User Interaction
    Client[User / Recruiting Admin] -->|1. Uploads Candidate CSV & Selects Target ATS| Frontend[Next.js Frontend / Vercel]
    
    %% API Request
    Frontend -->|2. Multipart Form POST /api/audit| Backend[FastAPI Backend Engine / Render]
    
    %% Backend Processing
    subgraph Backend Pipeline
        Backend -->|3. Read & Validate String Stream| Stream[CSV Ingestion & Normalization]
        Stream -->|4. Process Candidate Demographics| Math[EEOC 4/5ths Impact Ratio Calculator]
        Backend -->|5. Platform-Native System Prompt + CSV Data| LLM[OpenAI GPT-4o API]
    end
    
    %% Response Cycle
    LLM -->|6. Platform-Specific Remediation & Audit Report| Backend
    Backend -->|7. Structured JSON Payload| Frontend
    Frontend -->|8. Interactive Compliance Dashboard & Playbook| Client


---

## 🛠️ Tech Stack

* **Frontend**: Next.js, React, Tailwind CSS, TypeScript
* **Backend**: Python 3.11+, FastAPI, Uvicorn, Pandas / Data Processing
* **AI Model**: OpenAI GPT-4o API
* **Deployment & Infrastructure**: Vercel (Frontend), Render (Backend API), Git / GitHub Actions

---

## 🚀 Local Development Setup

### 1. Prerequisites
* Python 3.10+
* Node.js 18+
* OpenAI API Key

### 2. Backend Setup (FastAPI)
```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variable
export OPENAI_API_KEY="your-openai-api-key"

# Run FastAPI server
uvicorn main:app --reload --port 8000


## 👤 Author & Acknowledgments

### 👨‍💻 Author & Technical Lead
* **Technical Lead & Full-Stack Engineer**: [Your Name](https://github.com/nali29-rgb)
  * Architected full-stack compliance pipeline (Next.js, FastAPI, OpenAI GPT-4o).
  * Led product development, data pipeline design, and ATS remediation integration.

---

### 🏅 Award & Program Recognition
* **Awarded "Best Responsible AI Solution"** by an expert panel of industry judges during the project pitch showcase.
* Developed as part of the **[Davis Institute for Artificial Intelligence Summer Bridges Program](https://davisinstituteai.colby.edu/davisai-interdisciplinary-summer-bridges-program/)** at **Colby College**.

---

### 🙏 Special Thanks & Acknowledgments
* **Davis Institute for AI Faculty & Mentors**: For guidance on responsible AI frameworks, startup venture creation, and cross-disciplinary technical ethics.
* **HR & Talent Operations Managers**: To all HR professionals who participated in our customer discovery interviews and validated key pain points in automated hiring tools.
