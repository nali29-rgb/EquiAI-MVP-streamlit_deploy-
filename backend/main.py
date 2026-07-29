import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import openai

app = FastAPI(
    title="EquiAudit Engine API",
    description="EEOC & Algorithmic Bias Compliance Audit Engine"
)

# Enable CORS so your Next.js frontend can make requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust to specific domain in production if needed
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
    # 1. Dynamically retrieve the API key per request
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return {
            "success": False,
            "error": "OPENAI_API_KEY is missing from Render environment variables."
        }

    try:
        # 2. Read and decode the CSV dataset
        contents = await file.read()
        csv_text = contents.decode("utf-8", errors="ignore")

        if not csv_text.trim():
            return {"success": False, "error": "Uploaded CSV file is empty."}

        # 3. Initialize OpenAI client safely
        client = openai.OpenAI(api_key=api_key)

        # 4. Craft executive compliance prompt
        system_prompt = f"""
You are an expert EEOC & Algorithmic Bias Compliance Auditor specializing in Title VII regulations, NYC Local Law 144, and automated screening rule evaluations for the {target_ats} platform.

Analyze the provided candidate dataset CSV and construct a structured compliance audit report.

Formatting Requirements:
1. Start with an "Audit Protocol Note:" paragraph summarizing the overall compliance state and legal exposure level.
2. Provide exactly 4 structured sections starting with headers (`###`):
   - ### 1. Funnel & Disparate Impact Analysis
   - ### 2. Root Cause & Feature Weight Diagnosis
   - ### 3. Systemic Mitigation Playbook
   - ### 4. Legal Retention & Defense Strategy
3. Calculate/evaluate the EEOC 4/5ths rule (0.80 adverse impact ratio threshold) across candidate demographic groups.
4. Call out specific screening triggers or auto-rejection mechanisms within the {target_ats} workflow.
"""

        # Truncate text if extremely large to fit standard token limits
        sample_csv = csv_text[:20000]

        response = client.chat.completions.create(
            model="gpt-4o",  # You can switch to "gpt-4o-mini" if preferred
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"Target ATS: {target_ats}\n\nCandidate CSV Dataset:\n{sample_csv}"
                }
            ],
            temperature=0.2
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
            "error": "OpenAI API quota exceeded or insufficient account balance. Please check your OpenAI billing."
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"An unexpected error occurred during execution: {str(e)}"
        }
