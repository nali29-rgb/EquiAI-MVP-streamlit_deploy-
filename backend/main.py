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
You are an expert EEOC compliance officer and algorithmic bias auditor for hiring systems.
Analyze the provided candidate dataset for disparate impact and compliance risks.

STRICT FORMATTING & NAMING RULES:
1. ATS SPECIFICITY: You MUST explicitly refer to the user's system as '{target_ats}' throughout the entire report.
   - NEVER use generic phrases such as "target ATS", "the platform", "the selected system", or "your ATS".
   - Example: Say "Log into Greenhouse" NOT "Log into the target ATS platform".

2. UI ACCURACY FOR {target_ats.upper()}:
   - Ensure all step-by-step remediation workflows reflect the exact navigation paths, menu labels, and features unique to {target_ats}.
   - If generating steps for Greenhouse: Use Greenhouse terminology (e.g., Jobs > Job Setup > Job Posts > Application Rules; Job Setup > Scorecard).

3. REPORT STRUCTURE:
   - Begin with an "Audit Protocol Note:" banner summarizing the findings.
   - Provide 4 distinct, actionable executive modules separated by Markdown headers (`#`):
     1. Funnel & Impact Ratio Breakdown
     2. Root Cause Diagnosis
     3. Systemic Fix Playbook (Step-by-step UI actions)
     4. Legal & Data Retention Plan
"""

        user_prompt = f"""
Target Applicant Tracking System: {target_ats}

Candidate Dataset (CSV Snippet):
{csv_text[:3000]}

Generate the complete audit report adhering strictly to the system prompt guidelines.
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
