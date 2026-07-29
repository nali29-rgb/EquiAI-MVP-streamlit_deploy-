import os
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import openai

app = FastAPI()

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Safely initialize OpenAI without crashing server startup if key is missing
api_key = os.environ.get("OPENAI_API_KEY", "")
client = openai.OpenAI(api_key=api_key) if api_key else None

@app.post("/api/audit")
async def execute_audit(
    file: UploadFile = File(...),
    target_ats: str = Form(...)
):
    try:
        # Read the uploaded CSV dataset
        csv_bytes = await file.read()
        csv_text = csv_bytes.decode("utf-8")

        # -------------------------------------------------------------
        # PROMPT FIX: Force explicit ATS naming & UI accuracy
        # -------------------------------------------------------------
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

        # Call OpenAI LLM (or your configured model)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2
        )

        report = response.choices[0].message.content

        return {
            "success": True,
            "report": report
        }

    except Exception as e:
        print(f"Error during audit execution: {e}")
        return {
            "success": False,
            "error": str(e)
        }
