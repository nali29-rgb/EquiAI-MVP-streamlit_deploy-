import os
import requests

def generate_compliance_prose(metrics: dict, selected_ats: str) -> str:
    """
    Calls Groq / Llama API to generate structured compliance prose tailored to the selected ATS.
    """
    
    # Platform-specific remediation workflows
    ats_workflows = {
        "Workday Recruiting": """
1. **Step 1:** Log into Workday and search for the target **Job Requisition** using the search bar.
2. **Step 2:** Click **Actions (...)** next to the requisition title and select **Job Change > Edit Job Requisition**.
3. **Step 3:** Navigate to the **Questionnaires & Screening Rules** tab on the left-hand menu.
4. **Step 4:** Locate the **Auto-Disposition / Knockout Rule** tied to the custom question 'Continuous Employment History / Career Gaps'.
5. **Step 5:** Toggle the rule status to **Inactive** or remove it from the screening condition set.
6. **Step 6:** Navigate to **Candidate Stage Assessment**, locate the 'Linear Career Progression' scoring attribute, and change its evaluation weight from **Mandatory** to **Optional**.
""",
        "Greenhouse": """
1. **Step 1:** Log into Greenhouse, click **Jobs** from the top navigation bar, and select this specific Job Requisition.
2. **Step 2:** Click **Job Setup** on the left-hand menu panel, then click **Job Posts**.
3. **Step 3:** Scroll to the active post and click **Manage Rules** under the Application Rules column.
4. **Step 4:** Locate the **Auto-Reject Rule** tied to the custom question 'Continuous Employment History / Career Gaps'.
5. **Step 5:** Click **Delete (Trash Can Icon)** to completely remove the automated knockout constraint.
6. **Step 6:** Navigate to **Job Setup > Scorecard**, locate the 'Linear Career Progression' attribute, and toggle its focus weight from **Essential** to **Optional**.
""",
        "Lever": """
1. **Step 1:** Log into Lever Hire and navigate to **Settings > Application Forms**.
2. **Step 2:** Select the specific job posting tied to this hiring requisition.
3. **Step 3:** Locate the custom screening question for 'Continuous Employment History'.
4. **Step 4:** Turn off the **Auto-Archive / Knockout** toggle for non-linear career paths.
5. **Step 5:** Save changes and update candidate interview kits to mark career continuity as **Optional**.
""",
        "SmartRecruiters": """
1. **Step 1:** Log into SmartRecruiters and open **Settings > Screening Questions**.
2. **Step 2:** Select the active job requisition and open the **Auto-Screening Rules** engine.
3. **Step 3:** Find the rule filtering out candidates with career gaps or non-linear history.
4. **Step 4:** Deactivate the **Auto-Reject Trigger** for this question.
5. **Step 5:** Adjust the scorecard weight from **Knockout** to **Informational**.
"""
    }

    # Select the matching workflow or default to Workday
    ats_workflow = ats_workflows.get(selected_ats, ats_workflows["Workday Recruiting"])

    prompt = f"""
You are an expert EEOC & Employment Law Compliance Auditor. Generate an audit report based on these funnel metrics:
- Target ATS Platform: {selected_ats}
- Stage Failed: {metrics.get('failed_stage', 'Screening stage')}
- EEOC Impact Ratio: {metrics.get('impact_ratio', 0.33)}
- Compliance Status: {metrics.get('status', 'NON COMPLIANT')}

CRITICAL INSTRUCTIONS:
1. All technical reconfiguration steps MUST specifically use menu navigation, terminology, and workflows for **{selected_ats}**.
2. Do NOT mention Greenhouse if the user selected Workday Recruiting (or vice versa).
3. Section 3 MUST format each step on its own individual line as a numbered list.

Standard 4-section layout:

💧 **Audit Protocol Note:** A multi-state legal approach has been taken for universal compliance across all active federal and state regulatory jurisdictions.

---

### 🔍 1. Funnel Leak & Adverse Impact Assessment
* **Identified Failure Stage:** {metrics.get('failed_stage', 'Screening stage')}
* **EEOC Impact Ratio:** {metrics.get('impact_ratio', 0.33)} (Female screening pass rate / Male screening pass rate = 0.2 / 0.6)
* **Legal Compliance Posture:** NON COMPLIANT. This falls below the federal 0.80 standard, establishing prima facie Adverse Impact.

---

### 🧠 2. Multi-Jurisdictional Risk Diagnosis (The 'Why')
The screening failure is caused by a rigid 'Continuous Employment History' Auto-Reject rule filtering out non-linear career paths. This technical setup directly links to liability under Illinois Proxy Rules (discriminating via the proxy of career continuity) and California CRD Frameworks (which mandate immediate employer liability for automated vendor filtering systems).

---

### ⚙️ 3. Targeted Systemic Fixes ({selected_ats} Re-Configuration)

{ats_workflow.strip()}

**Data Retention Directive:** Under California CRD rules, export this configuration log from {selected_ats} and preserve all screening metrics for a mandatory minimum of 4 years.

---

### 🛠️ 4. Immediate Operational Recovery Plan
To recover candidates falsely rejected by the 'Continuous Employment History' Auto-Reject rule, perform the following manual extraction step:

* Extract all applicants from the last 14 days who were rejected solely due to this rule by running a custom report in {selected_ats}, filtering by `Application Status = 'Auto-Rejected'` and `Rejection Reason = 'Continuous Employment History / Career Gaps'`, without applying any demographic filters.
"""

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return prompt

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
    except Exception:
        pass

    return prompt
