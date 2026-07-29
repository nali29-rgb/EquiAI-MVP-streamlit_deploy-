import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import openai

app = FastAPI(
    title="EquiAudit Engine API",
    description="EEOC & Algorithmic Bias Compliance Audit Engine"
)

# Enable CORS for Next.js / Streamlit frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    """Health check endpoint for Render monitoring."""
    return {"status": "online", "service": "EquiAudit Compliance Engine"}


@app.post("/api/audit")
async def run_audit(
    file: UploadFile = File(...),
    target_ats: str = Form("Greenhouse")
):
    """
    Executes an algorithmic bias audit on the uploaded candidate dataset CSV
    for the specified ATS platform.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return {
            "success": False,
            "error": "OPENAI_API_KEY is missing from Render environment variables."
        }

    try:
        contents = await file.read()
        csv_text = contents.decode("utf-8", errors="ignore")

        # Python string check (.strip() handles whitespace correctly)
        if not csv_text.strip():
            return {"success": False, "error": "Uploaded CSV file is empty."}

        client = openai.OpenAI(api_key=api_key)

        # 🎯 High-Precision Actionable System Prompt
        system_prompt = f"""
You are an expert EEOC Title VII and NYC Local Law 144 compliance auditor specializing in automated employment decision tools (AEDTs) and applicant tracking system (ATS) architecture for **{target_ats}**.

Analyze the candidate CSV dataset and generate an actionable, audit-ready compliance report specifically tailored to the workflow and configuration settings of **{target_ats}**.

CRITICAL AUDIT MANDATES:
1. STRICTLY NO GENERIC BOILERPLATE: Do NOT output generic consulting advice like "conduct a review", "audit regularly", "implement bias protocols", or "introduce diverse datasets".
2. ATS PLATFORM NATIVE: Cite exact configuration menus, setting paths, stage rules, and screening modules native to **{target_ats}** (e.g., for Greenhouse: "Stage Rules & Auto-Rejection Knockout Questions", for Workday: "Candidate Match & Job Profile Weighting Filters", for Lever: "Fast-Track Rules", for SmartRecruiters: "Screening Scorecards").
3. HARD COMPUTATIONS: Perform actual numerical calculations from the CSV dataset (candidate totals, advancement counts, selection rates per demographic group, EEOC 4/5ths impact ratios).
4. DIRECT ACTIONABLE STEPS: Every fix must be a direct administrative command that an HR tech or recruiting operations admin can execute immediately inside **{target_ats}**.

REQUIRED OUTPUT FORMAT:

Start with:
Audit Protocol Note: [A 2-3 sentence executive summary evaluating Title VII and NYC Local Law 144 legal exposure, citing the exact computed adverse impact ratio for the affected demographic group on {target_ats}.]

Then provide exactly 4 structured sections using headers (`###`):

### 1. Funnel & Disparate Impact Analysis
- Calculate exact applicant headcounts, advancement numbers, and selection rates across demographic groups present in the CSV.
- Compute the EEOC Adverse Impact Ratio = (Selection Rate of Protected Group) / (Selection Rate of Benchmark Group).
- Explicitly state whether the calculated ratio breaches the 0.80 federal threshold under the EEOC 4/5ths rule.

### 2. Root Cause & Feature Weight Diagnosis
- Pinpoint specific candidate features, screening thresholds, or qualifications in the CSV causing the disparity.
- Detail how **{target_ats}**'s automated screening filters or scoring mechanisms amplify this bias against the protected demographic group.

### 3. Systemic Mitigation Playbook
- Provide 3-4 concrete, numbered administrative fixes directly executable within the **{target_ats}** platform interface.
- Format each as a direct step-by-step action (e.g., "1. In {target_ats} Admin -> Navigate to Requisition Screening Rules -> Modify or disable automated knockout logic on Feature X").

### 4. Legal Retention & Defense Strategy
- Outline exact record-keeping mandates, bias audit logging requirements, and NYC LL144 publication schedules required for **{target_ats}**.
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
            "error": f"An unexpected error occurred during execution: {str(e)}"
        }
