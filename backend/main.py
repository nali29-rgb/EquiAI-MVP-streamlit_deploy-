import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import openai

app = FastAPI(
    title="EquiAudit Engine API",
    description="EEOC & Algorithmic Bias Compliance Audit Engine"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {"status": "online", "service": "EquiAudit Compliance Engine"}


@app.post("/api/audit")
async def run_audit(
    file: UploadFile = File(...),
    target_ats: str = Form("Greenhouse")
):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return {
            "success": False,
            "error": "OPENAI_API_KEY is missing from Render environment variables."
        }

    try:
        contents = await file.read()
        csv_text = contents.decode("utf-8", errors="ignore")

        if not csv_text.strip():
            return {"success": False, "error": "Uploaded CSV file is empty."}

        client = openai.OpenAI(api_key=api_key)

        # 🎯 Rigorous, Platform-Native & Actionable Audit Prompt
        system_prompt = f"""
You are an elite EEOC Title VII and NYC Local Law 144 Algorithmic Compliance Auditor. 
Your task is to perform an audit-grade evaluation of the provided candidate dataset CSV for the **{target_ats}** platform.

STRICT AUDIT RULES:
- DO NOT use generic boilerplate advice (e.g., "conduct a review", "implement bias detection", "introduce diverse datasets").
- DO provide exact, step-by-step administrative actions native to **{target_ats}** UI workflows, stage settings, and knockout rules.
- DO perform exact numerical calculations based on the dataset (pass rates, EEOC 4/5ths Impact Ratios).

OUTPUT FORMATTING REQUIREMENTS:

1. Start immediately with:
Audit Protocol Note: [Provide a 2-3 sentence legal exposure summary citing Title VII, NYC Local Law 144, calculated impact ratios, and platform-specific risk for {target_ats}.]

2. Follow with EXACTLY 4 structured sections using markdown headers (`###`):

### 1. Funnel & Disparate Impact Analysis
- Calculate exact candidate counts, advancement counts, and selection rates across demographic groups from the CSV.
- Display the computed EEOC Impact Ratio (Protected Rate / Benchmark Rate). State whether it breaches the federal 0.80 (4/5ths rule) threshold.

### 2. Root Cause & Feature Weight Diagnosis
- Identify the exact feature weighting or screening rule inside **{target_ats}** triggering the disparity (e.g., automated knockout questions, hard-coded experience filters, candidate match scoring thresholds).
- Explain precisely how this feature disproportionately penalizes protected candidate groups.

### 3. Systemic Mitigation Playbook
- Provide 3-4 concrete, step-by-step configuration fixes directly inside **{target_ats}** settings.
- Format as direct actionable commands (e.g., "1. In {target_ats} Admin -> Navigate to Screening Rules -> Disable automatic rejection on Question X").

### 4. Legal Retention & Defense Strategy
- Outline specific audit logging, candidate data retention schedules, and NYC LL144 compliance reporting requirements for **{target_ats}**.
"""

        sample_csv = csv_text[:25000]

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"Target ATS Platform: {target_ats}\n\nCandidate CSV Dataset:\n{sample_csv}"
                }
            ],
            temperature=0.1
        )

        report_content = response.choices[0].message.content
        return {"success": True, "report": report_content}

    except openai.AuthenticationError:
        return {
            "success": False,
            "error": "Invalid OpenAI API key. Check your OPENAI_API_KEY variable in Render."
        }
    except openai.RateLimitError:
        return {
            "success": False,
            "error": "OpenAI API quota exceeded or insufficient account balance. Check your OpenAI billing."
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"An unexpected error occurred: {str(e)}"
        }
