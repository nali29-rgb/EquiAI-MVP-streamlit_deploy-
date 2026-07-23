from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io

from core.math_engine import calculate_funnel_bias
from core.llama_agent import generate_compliance_prose

app = FastAPI(title="EquiAudit AI Backend")

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Update with your Vercel URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "EquiAudit AI Engine"}

@app.post("/api/audit")
async def run_audit(
    file: UploadFile = File(...),
    target_ats: str = Form(...)
):
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        # Run math engine & Llama agent
        metrics = calculate_funnel_bias(df)
        report = generate_compliance_prose(metrics, target_ats)
        
        return {
            "success": True,
            "metrics": metrics,
            "report": report
        }
    except Exception as e:
        return {"success": False, "error": str(e)}