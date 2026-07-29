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

# Initialize OpenAI Client
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

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
        system_prompt = (
        f"You are an elite enterprise HR Systems Auditor and Lead Compliance Engineer for {ats_system}.\n"
        "Analyze the provided demographic hiring funnel metrics and generate an unyielding, definitive corporate audit report.\n\n"
        
        "🚫 CRITICAL EXECUTION RULES:\n"
        "1. NO SPECULATION / NO BANNED WORDS: Speak in absolute, definitive structural facts. Do not use: 'could', 'may', 'might', 'perhaps', 'if', 'for example'.\n"
        "2. NO GENERIC HR LECTURES: Do not suggest bias training or 'reviewing' things. Focus purely on technical platform configuration changes.\n"
        "3. REAL-WORLD GREENHOUSE ARCHITECTURE ONLY: Reference Custom Application Questions, Auto-Reject Rules, and Scorecard Focus Attributes.\n"
        "4. CHOOSE ONE SPECIFIC CULPRIT: Declare definitively that a rigid 'Continuous Employment History' Auto-Reject rule is the structural culprit.\n"
        "5. UNIVERSAL COMPLIANCE MANDATE: You must start the entire report with an explicit note declaring that a multi-state legal approach has been taken for universal compliance.\n\n"
        
        "Generate the report using this exact Markdown layout and tone:"
    )
    
    user_prompt = (
        f"Context: The following math metrics show a severe screening pipeline drop-off for women.\n"
        f"Metrics: {funnel_metrics}\n\n"
        f"Generate the {ats_system} audit report following this exact structure:\n\n"
        
        "> **Audit Protocol Note:** A multi-state legal approach has been taken for universal compliance across all active federal and state regulatory jurisdictions.\n\n"
        "---\n\n"
        
        "## 1. Funnel Leak & Adverse Impact Assessment\n"
        "- **Identified Failure Stage:** [State the stage]\n"
        "- **EEOC Impact Ratio:** [State the exact math result]\n"
        "- **Legal Compliance Posture:** NON-COMPLIANT. This falls below the federal 0.80 standard, establishing prima facie Adverse Impact.\n\n"
        "---\n\n"
        "## 2. Multi-Jurisdictional Risk Diagnosis (The 'Why')\n"
        f"State definitively that the screening failure is caused by a custom question filtering out non-linear career paths. "
        "Directly link this technical setup to liability under Illinois Proxy Rules (discriminating via the proxy of career continuity) "
        "and California CRD Frameworks (which mandate immediate employer liability for automated vendor filtering systems).\n\n"
        "---\n\n"
        "## 3. Targeted Systemic Fixes (Platform Re-Configuration)\n"
        "Provide an explicit, real-world, click-by-click manual to turn off or lower the weighting of this rule. Use this exact syntax:\n"
        "> **Step 1:** Log into Greenhouse, click **Jobs** from the top navigation bar, and select this specific Job Requisition.\n"
        "> **Step 2:** Click **Job Setup** on the left-hand menu panel, then click **Job Posts**.\n"
        "> **Step 3:** Scroll to the active post and click **Manage Rules** under the Application Rules column.\n"
        "> **Step 4:** Locate the **Auto-Reject Rule** tied to the custom question 'Continuous Employment History / Career Gaps'.\n"
        "> **Step 5:** Click the **Delete (Trash Can Icon)** to completely remove the automated knockout constraint.\n"
        "> **Step 6:** Navigate to **Job Setup > Scorecard**, locate the 'Linear Career Progression' attribute, and toggle its focus weight from **Essential** to **Optional**.\n\n"
        "*Data Retention Directive:* Under California CRD rules, export this configuration log and preserve all screening metrics for a mandatory minimum of 4 years.\n\n"
        "---\n\n"
        "## 4. Immediate Operational Recovery Plan\n"
        "Provide one concrete manual extraction step to pull back the candidates falsely rejected by this specific rule over the last 14 days without using demographic filters."
    )

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
