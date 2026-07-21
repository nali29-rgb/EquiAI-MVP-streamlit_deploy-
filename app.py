import streamlit as st
import pandas as pd

# Import your backend engines from the core folder
from core.math_engine import calculate_funnel_bias
from core.llama_agent import generate_compliance_prose
from datetime import datetime


st.set_page_config(page_title="EquiAudit AI", page_icon="⚖️", layout="wide")

PRIMARY = "#748bc5"
SECONDARY = "#f18d7a"
TEXT = "#171717"
BORDER = "rgba(148, 163, 184, 0.18)"
SURFACE = "#f4f6ff"
BACKGROUND = "#fff1f9"

PAGE_OPTIONS = [
    "Dashboard",
    "Upload Analysis",
    "Analysis Progress",
    "Results Dashboard",
    "Detailed Finding",
    "Report Preview",
    "Legal Library",
    "Settings",
]

RECENT_ANALYSES = [
    {"name": "Q3 Hiring Bias Audit", "date": "2026-07-05", "score": "82", "status": "Complete", "badge": "Low"},
    {"name": "Campus Summer Round", "date": "2026-06-28", "score": "74", "status": "Review", "badge": "Medium"},
    {"name": "DEI Compliance Snapshot", "date": "2026-06-18", "score": "91", "status": "Complete", "badge": "Low"},
]

UPLOAD_EXAMPLES = [
    {"file": "Engineering_Spring_Applicants.csv", "size": "2.4 MB", "status": "Ready"},
    {"file": "Sales_Hires_Q2.xlsx", "size": "1.1 MB", "status": "Ready"},
]

RISK_TREND = pd.DataFrame({
    "Week": ["Apr 1", "Apr 8", "Apr 15", "Apr 22", "Apr 29", "May 6", "May 13"],
    "Risk Score": [72, 68, 74, 77, 75, 79, 82],
    "Compliance": [86, 88, 85, 84, 86, 82, 80],
}).set_index("Week")

PROTECTED_CLASS_DATA = pd.DataFrame([
    {"Group": "Gender", "Accepted %": 55, "Rejected %": 45, "Delta": "+10"},
    {"Group": "Race/Ethnicity", "Accepted %": 48, "Rejected %": 52, "Delta": "-4"},
    {"Group": "Age", "Accepted %": 61, "Rejected %": 39, "Delta": "+22"},
])

DETAILED_FINDINGS = [
    {
        "keyword": "On-site availability",
        "frequency": "26",
        "accepted": "82%",
        "rejected": "18%",
        "confidence": "92%",
        "category": "Scheduling proxy",
        "explanation": "Candidates indicating flexible remote work windows are more likely to progress, which may penalize applicants with caregiving obligations.",
        "legal_refs": ["Title VII", "EEOC Guidance on Employment Discrimination"],
        "suggestion": "Replace with a neutral availability question that focuses on core role hours rather than personal obligations.",
    },
    {
        "keyword": "College prestige",
        "frequency": "18",
        "accepted": "76%",
        "rejected": "24%",
        "confidence": "88%",
        "category": "Educational proxy",
        "explanation": "A strong signal is being placed on university ranking, which can indirectly exclude first-generation applicants.",
        "legal_refs": ["EEOC Enforcement Guidance", "NIST AI Risk Management Framework"],
        "suggestion": "Prioritize skills-based assessment language and remove prestige-based scoring from the job rubric.",
    },
    {
        "keyword": "Parenting gap",
        "frequency": "12",
        "accepted": "69%",
        "rejected": "31%",
        "confidence": "90%",
        "category": "Family status proxy",
        "explanation": "Candidates reporting career breaks are less likely to progress, which can disadvantage primary caregivers.",
        "legal_refs": ["Title VII", "State Family Leave Regulations"],
        "suggestion": "Frame career interruptions as experience diversity rather than risk factors.",
    },
]

LEGAL_LIBRARY = [
    {"title": "Title VII of the Civil Rights Act", "category": "Federal", "summary": "Prohibits employment discrimination based on race, color, religion, sex and national origin.", "details": "Title VII requires employers to treat applicants and employees fairly across protected traits and to avoid policies with disparate impact."},
    {"title": "EEOC Guidance on AI Hiring", "category": "EEOC", "summary": "Best practices for using algorithms in hiring without discriminating.", "details": "The EEOC recommends audits, bias testing, and transparency when automated tools influence hiring decisions."},
    {"title": "NIST AI Risk Management Framework", "category": "NIST", "summary": "A technical framework for trustworthy AI deployment.", "details": "Use risk-based controls, documentation, and monitoring to reduce AI-driven bias in decision systems."},
    {"title": "California Fair Employment & Housing Act", "category": "State", "summary": "Protects employees and applicants from discrimination in California.", "details": "Employer practices should be evaluated for both intentional discrimination and disparate impact statewide."},
]

SETTINGS = {
    "workspace_name": "EquiAudit AI - Acme Legal Ops",
    "email": "compliance@acme-legal.com",
    "notifications": {
        "weekly_summary": True,
        "report_ready": True,
        "policy_alerts": False,
    },
    "branding": {
        "accent_color": "#748bc5",
        "logo_text": "EquiAudit AI",
        "report_header": "Acme Hiring Bias Review",
    },
    "analysis_defaults": {
        "include_legal_references": True,
        "confidence_threshold": "85%",
        "review_scope": "All departments",
    },
}


# -----------------------------------------------------------------------------
# Utility components
# -----------------------------------------------------------------------------

def render_css():
    st.markdown(
        f"""
        <style>
            :root {{
                color-scheme: light;
                font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            }}
            .stApp {{ background: {BACKGROUND}; color: {TEXT}; }}
            .block-container {{ padding-top: 1rem; padding-bottom: 1.5rem; padding-left: 2rem; padding-right: 2rem; max-width: 1680px; }}
            .stSidebar {{ background: #ffffff; border-right: 1px solid {BORDER}; }}
            .sidebar .css-1d391kg {{ background: #ffffff; }}
            .main .css-18e3th9 {{ gap: 1rem; }}
            .stButton>button {{ background: {PRIMARY}; color: white; border: none; border-radius: 14px; padding: 0.85rem 1rem; box-shadow: none; }}
            .stButton>button:hover {{ background: {SECONDARY}; color: white; }}
            .st-buzzer {{ box-shadow: 0 24px 60px rgba(15, 23, 42, 0.08); }}
            .card {{ background: {SURFACE}; border: 1px solid {BORDER}; border-radius: 24px; padding: 1.2rem; box-shadow: 0 20px 50px rgba(15, 23, 42, 0.04); }}
            .card-compact {{ background: {SURFACE}; border: 1px solid {BORDER}; border-radius: 20px; padding: 1rem; }}
            .card-hero {{ background: {SURFACE}; border: 1px solid {PRIMARY}; border-radius: 28px; padding: 1.4rem; }}
            .section-title {{ font-size: 1.1rem; font-weight: 700; color: {PRIMARY}; margin-bottom: 0.65rem; }}
            .small-muted {{ color: #6b7280; font-size: 0.95rem; }}
            .risk-badge {{ display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.55rem 0.9rem; border-radius: 999px; font-size: 0.85rem; font-weight: 700; }}
            .badge-low {{ background: #eef2ff; color: #3730a3; }}
            .badge-medium {{ background: #fef3c7; color: #92400e; }}
            .badge-high {{ background: #fff1f2; color: #b91c1c; }}
            .badge-critical {{ background: #fee2e2; color: #991b1b; }}
            .metric-title {{ color: {TEXT}; font-size: 0.95rem; margin-bottom: 0.35rem; }}
            .metric-value {{ font-size: 2.2rem; font-weight: 700; margin-bottom: 0.35rem; }}
            .metric-note {{ font-size: 0.95rem; color: #64748b; }}
            .table-card th {{ text-align: left; padding: 0.95rem 0.75rem; color: {TEXT}; font-weight: 700; border-bottom: 1px solid rgba(148, 163, 184, 0.20); }}
            .table-card td {{ padding: 0.82rem 0.75rem; border-bottom: 1px solid rgba(148, 163, 184, 0.10); }}
            .table-card tbody tr:hover {{ background: #f8fafc; }}
            .top-nav {{ margin-bottom: 1.5rem; }}
            .top-nav__item {{ display: inline-flex; align-items: center; gap: 0.6rem; color: {TEXT}; font-size: 0.95rem; }}
            .top-nav__pill {{ background: {SECONDARY}; color: white; padding: 0.55rem 0.9rem; border-radius: 999px; font-weight: 700; }}
            .focus-visible:focus {{ outline: 3px solid rgba(75, 108, 250, 0.35); outline-offset: 2px; }}
            .streamlit-expanderHeader {{ outline-offset: 2px; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_top_navigation(page_name: str):
    left, middle, right = st.columns([3, 3, 2], gap="large")
    with left:
        st.markdown(f"<div class='top-nav'><span class='top-nav__item'><strong>{SETTINGS['workspace_name']}</strong></span></div>", unsafe_allow_html=True)
    with middle:
        query = st.text_input("Search the workspace", placeholder="Search reports, keywords, laws...", key="top_search")
        if query:
            st.info(f"Search placeholder: {query}")
    with right:
        st.markdown(
            "<div style='display:flex; gap:0.5rem; justify-content:flex-end;'>"
            "<span class='top-nav__pill'>Notifications</span>"
            "<span class='top-nav__pill'>Profile</span>"
            "</div>",
            unsafe_allow_html=True,
        )
    st.markdown("---")


def render_sidebar():
    st.sidebar.markdown("## Navigation")
    page = st.sidebar.radio("", PAGE_OPTIONS, index=0)
    st.sidebar.markdown("---")
    st.sidebar.markdown("## Quick actions")
    st.sidebar.button("Start new compliance review")
    st.sidebar.button("Open latest report")
    st.sidebar.markdown("---")
    st.sidebar.markdown("## Account")
    st.sidebar.write("**Lina Hart**")
    st.sidebar.write("Compliance Lead")
    st.sidebar.write("lina.hart@acme-legal.com")
    return page


def risk_badge(level: str) -> str:
    classes = {
        "Low": "risk-badge badge-low",
        "Medium": "risk-badge badge-medium",
        "High": "risk-badge badge-high",
        "Critical": "risk-badge badge-critical",
    }
    color = classes.get(level, classes["Low"])
    return f"<span class='{color}'>{level}</span>"


def render_summary_card(title: str, value: str, note: str):
    st.markdown(
        f"""
        <div class='card-compact'>
            <div class='metric-title'>{title}</div>
            <div class='metric-value'>{value}</div>
            <div class='metric-note'>{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section(title: str, subtitle: str = ""):
    st.markdown(f"<div class='section-title'>{title}</div><div class='small-muted'>{subtitle}</div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Page renderers
# -----------------------------------------------------------------------------

def dashboard_page():
    render_top_navigation("Dashboard")
    row1 = st.columns(3, gap="large")
    with row1[0]:
        render_summary_card("Average compliance score", "84%", "Up 4 points from last quarter")
    with row1[1]:
        render_summary_card("Open risk profiles", "12", "Pending review across three regions")
    with row1[2]:
        render_summary_card("Active datasets", "5", "Uploaded in the last 30 days")

    st.markdown("<div class='card'> <div class='section-title'>Risk trend</div>", unsafe_allow_html=True)
    st.line_chart(RISK_TREND)
    st.markdown("</div>", unsafe_allow_html=True)

    st.write(" ")
    left, right = st.columns([2, 1], gap="large")
    with left:
        render_section("Recent analyses", "Latest compliance and bias reports")
        table_rows = ""
        for item in RECENT_ANALYSES:
            table_rows += (
                f"<tr><td>{item['name']}</td><td>{item['date']}</td>"
                f"<td><strong>{item['score']}%</strong></td><td>{item['status']}</td>"
                f"<td>{risk_badge(item['badge'])}</td></tr>"
            )
        st.markdown(
            """
            <div class='card'>
            <table class='table-card' style='width:100%; border-collapse:collapse;'>
                <thead><tr><th>Analysis</th><th>Date</th><th>Score</th><th>Status</th><th>Risk</th></tr></thead>
                <tbody>
            """
            + table_rows +
            "</tbody></table></div>",
            unsafe_allow_html=True,
        )
    with right:
        render_section("Quick actions", "Launch a new dataset, review a report, or share findings")
        st.markdown(
            "<div class='card'>"
            "<div style='display:grid; gap:1rem'>"
            "<button class='stButton'>Upload new hiring file</button>"
            "<button class='stButton'>Review latest bias finding</button>"
            "<button class='stButton'>Create report preview</button>"
            "</div></div>",
            unsafe_allow_html=True,
        )

    st.write(" ")
    render_section("Recent uploads", "Files ready for analysis with source and type details")
    upload_rows = ""
    for item in UPLOAD_EXAMPLES:
        upload_rows += f"<tr><td>{item['file']}</td><td>{item['size']}</td><td>{item['status']}</td></tr>"
    st.markdown(
        """
        <div class='card'>
            <table class='table-card' style='width:100%; border-collapse:collapse;'>
                <thead><tr><th>File</th><th>Size</th><th>Status</th></tr></thead>
                <tbody>
        """
        + upload_rows +
        """
                </tbody></table>
        </div>
        """,
        unsafe_allow_html=True,
    )


def upload_analysis_page():
    render_top_navigation("Upload Analysis")
    st.markdown("<div class='card-hero'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Upload hiring datasets</div>")
    st.write("Drag CSV, Excel, or JSON applicant upload files into the area below. We will stage them for your next compliance review.")
    
    # 1. Target ATS Dropdown Selection
    selected_ats = st.selectbox(
        "Target ATS Platform:", 
        ["Greenhouse", "Workday Recruiting"]
    )
    
    uploaded_files = st.file_uploader("Upload your analysis files", type=["csv", "xlsx", "json"], accept_multiple_files=True)
    
    if uploaded_files:
        st.success(f"{len(uploaded_files)} file(s) uploaded and staged for analysis.")
        for f in uploaded_files:
            st.markdown(f"- **{f.name}** · *{round(f.size / 1024, 1)} KB*")
        
        # 2. Trigger Audit Execution
        if st.button("Analyze dataset", key="start_analysis"):
            with st.spinner("Executing Math Engine & querying Llama Compliance Engine..."):
                target_file = uploaded_files[0]
                df = pd.read_csv(target_file)
                
                # Run backend math and LLM engine
                metrics = calculate_funnel_bias(df)
                report = generate_compliance_prose(metrics, selected_ats)
                
                st.divider()
                st.markdown(report)
    else:
        st.info("Drop a supported dataset or click to browse your files.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.write(" ")
    settings_card = st.columns([2, 1], gap="large")
    with settings_card[0]:
        render_section("Analysis settings", "Customize the audit before you run it")
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.selectbox("Review scope", ["All departments", "Customer support", "Engineering", "Sales"], index=0)
        st.selectbox("Compliance profile", ["Standard bias audit", "AI regulation deep scan", "EEOC readiness check"], index=0)
        st.checkbox("Include legal references in the report", value=True)
        st.select_slider("Confidence threshold", options=["70%", "75%", "80%", "85%", "90%", "95%"], value="85%")
        st.markdown("</div>", unsafe_allow_html=True)
    with settings_card[1]:
        render_section("Upload guide", "What this page supports")
        st.markdown(
            "<div class='card'>"
            "<ul style='padding-left:1.15rem; color:#475569;'>"
            "<li>CSV, Excel, JSON files</li>"
            "<li>Candidate outcome datasets</li>"
            "<li>Structured applicant metadata</li>"
            "<li>Ready for batch review</li>"
            "</ul>"
            "</div>",
            unsafe_allow_html=True,
        )


def analysis_progress_page():
    render_top_navigation("Analysis Progress")
    render_section("Analysis in progress", "Simulated workflow for dataset ingestion and compliance review")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.progress(0.76)
    st.write("**76% complete — estimated 90 seconds remaining**")
    steps = [
        ("Reading files", True),
        ("Cleaning data", True),
        ("Finding keywords", True),
        ("Running statistics", True),
        ("Consulting legal database", False),
        ("Generating recommendations", False),
        ("Building PDF", False),
    ]
    for label, done in steps:
        icon = "✅" if done else "⏳"
        st.markdown(f"- {icon} **{label}**")
    st.markdown("</div>", unsafe_allow_html=True)
    st.write(" ")
    with st.expander("Analysis summary", expanded=True):
        st.write("This animation represents a staged data pipeline where each step has been verified against compliance controls and bias assertions.")
        st.write("The final results dashboard will include the complete risk score, protected class proxies, keyword issues, and recommendations.")


def results_dashboard_page():
    render_top_navigation("Results Dashboard")
    top_metrics = st.columns(4, gap="large")
    stats = [
        ("Overall risk score", "78/100", "Bias exposure suggests moderate review priority."),
        ("Compliance score", "84%", "Aligned with current EEOC benchmarks."),
        ("Critical findings", "3", "Items needing immediate policy review."),
        ("Legal references", "12", "Guidance selected for this analysis."),
    ]
    for index, info in enumerate(stats):
        with top_metrics[index]:
            render_summary_card(info[0], info[1], info[2])

    st.write(" ")
    left, right = st.columns([2, 1], gap="large")
    with left:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Overall risk gauge</div>")
        st.markdown("<div style='height: 260px; display:flex; align-items:center; justify-content:center;'>"
                    "<div style='width: 80%; height: 16px; background: #e2e8f0; border-radius: 999px; overflow:hidden;'>"
                    "<div style='width: 78%; height: 100%; background: linear-gradient(90deg, #4b6cfa, #3c59d2);'></div>"
                    "</div></div>")
        st.markdown("<div style='display:flex; justify-content:space-between; color:#475569; font-size:0.95rem;'>"
                    "<span>Low risk</span><span>Critical risk</span></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Key summary</div>")
        st.write("- Hiring funnel leakage is concentrated in early screening and scheduling requirements.")
        st.write("- Legal risk is strongest for proxy language in interview availability and education filters.")
        st.write("- Recommend immediate review of automated screening rules and scorecard requirements.")
        st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("Potential biases", expanded=True):
        bias_tabs = st.columns(3, gap="large")
        bias_scores = [
            ("Gender bias", "High", "Review hiring criteria for gendered language."),
            ("Age bias", "Medium", "Assess job requirements that penalize older applicants."),
            ("Education bias", "Low", "Replace prestige cues with skills-based criteria."),
        ]
        for index, item in enumerate(bias_scores):
            with bias_tabs[index]:
                st.markdown(f"<div class='card-compact'><div class='metric-title'>{item[0]}</div><div class='metric-value'>{item[1]}</div><div class='metric-note'>{item[2]}</div></div>", unsafe_allow_html=True)
    with st.expander("Detected keywords", expanded=False):
        keywords = pd.DataFrame([
            {"Keyword": "On-site availability", "Count": 26, "Severity": "High"},
            {"Keyword": "College prestige", "Count": 18, "Severity": "Medium"},
            {"Keyword": "Parenting gap", "Count": 12, "Severity": "High"},
        ])
        st.table(keywords)
    with st.expander("Statistical findings", expanded=False):
        st.table(PROTECTED_CLASS_DATA)
    with st.expander("Legal references", expanded=False):
        for law in LEGAL_LIBRARY:
            st.markdown(f"**{law['title']}** — {law['category']}<br><span style='color:#475569'>{law['summary']}</span><br><br>", unsafe_allow_html=True)
    with st.expander("Recommendations", expanded=False):
        st.markdown(
            "- Remove operational language that evaluates candidate availability as a proxy for reliability.\n"
            "- Replace prestige-based bias with objective performance criteria.\n"
            "- Add audit triggers for protected-class distribution changes after each hiring batch."
        )


def detailed_finding_page():
    render_top_navigation("Detailed Finding")
    title = st.selectbox("Choose flagged issue", [item["keyword"] for item in DETAILED_FINDINGS])
    issue = next(item for item in DETAILED_FINDINGS if item["keyword"] == title)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>{issue['keyword']}</div>")
    left, right = st.columns(2, gap="large")
    with left:
        st.markdown(f"<div class='metric-title'>Frequency</div><div class='metric-value'>{issue['frequency']}</div>")
        st.markdown(f"<div class='metric-title'>Accepted %</div><div class='metric-value'>{issue['accepted']}</div>")
        st.markdown(f"<div class='metric-title'>Rejected %</div><div class='metric-value'>{issue['rejected']}</div>")
    with right:
        st.markdown(f"<div class='metric-title'>Confidence</div><div class='metric-value'>{issue['confidence']}</div>")
        st.markdown(f"<div class='metric-title'>Category</div><div class='metric-value'>{issue['category']}</div>")
    st.markdown("<hr style='border:none; border-top:1px solid rgba(148,163,184,0.18); margin:1rem 0;' />")
    st.markdown(f"<div class='metric-title'>Explanation</div><div style='color:#475569'>{issue['explanation']}</div>")
    st.markdown(f"<div class='metric-title' style='margin-top:1rem;'>Legal references</div>")
    for ref in issue["legal_refs"]:
        st.markdown(f"- {ref}")
    st.markdown(f"<div class='metric-title' style='margin-top:1rem;'>Suggested replacement</div><div style='color:#475569'>{issue['suggestion']}</div>")
    st.markdown("</div>", unsafe_allow_html=True)


def report_preview_page():
    render_top_navigation("Report Preview")
    top = st.columns([3, 1], gap="large")
    with top[0]:
        render_section("Report preview", "Professional PDF layout with export controls")
    with top[1]:
        st.button("Export PDF")
        st.button("Email report")
        st.button("Download")

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Table of contents</div>")
    st.write("1. Executive summary")
    st.write("2. Risk and compliance scores")
    st.write("3. Key findings")
    st.write("4. Legal references")
    st.write("5. Recommendations")
    st.markdown("</div>", unsafe_allow_html=True)
    st.write(" ")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Preview page: executive summary</div>")
    st.write("**Overall risk score:** 78/100")
    st.write("**Compliance score:** 84%")
    st.write("EquiAudit AI identified priority bias signals in candidate screening and keyword-based filtering.")
    st.markdown("</div>", unsafe_allow_html=True)


def legal_library_page():
    render_top_navigation("Legal Library")
    search_term = st.text_input("Search legal references", placeholder="Search federal, state, EEOC, NIST, AI regulations")
    selected_filters = st.multiselect("Filter by category", ["Federal", "State", "EEOC", "NIST", "AI Regulations"], default=["Federal", "EEOC", "NIST"])
    filtered = [law for law in LEGAL_LIBRARY if (not search_term or search_term.lower() in law["title"].lower()) and (not selected_filters or law["category"] in selected_filters)]
    if not filtered:
        st.warning("No legal references match that search. Try a broader keyword.")
        return
    first = filtered[0]
    left, right = st.columns([1, 2], gap="large")
    with left:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        for law in filtered:
            st.markdown(f"### {law['title']}<br><span style='color:#64748b'>{law['summary']}</span><br><br>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='section-title'>{first['title']}</div>")
        st.write(first["details"])
        st.markdown("</div>", unsafe_allow_html=True)


def settings_page():
    render_top_navigation("Settings")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Workspace settings</div>")
    st.text_input("Workspace name", value=SETTINGS["workspace_name"])
    st.text_input("Primary notification email", value=SETTINGS["email"])
    st.markdown("<div style='display:grid; gap: 1rem; margin-top: 1rem;'>", unsafe_allow_html=True)
    st.checkbox("Weekly summary emails", value=SETTINGS["notifications"]["weekly_summary"])
    st.checkbox("Report ready alerts", value=SETTINGS["notifications"]["report_ready"])
    st.checkbox("Policy alert notifications", value=SETTINGS["notifications"]["policy_alerts"])
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.write(" ")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Report branding</div>")
    st.text_input("Brand accent color", value=SETTINGS["branding"]["accent_color"])
    st.text_input("Report header text", value=SETTINGS["branding"]["report_header"])
    st.markdown("</div>", unsafe_allow_html=True)

    st.write(" ")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Default analysis settings</div>")
    st.selectbox("Review scope", ["All departments", "Customer support", "Engineering", "Sales"], index=0)
    st.select_slider("Confidence threshold", options=["70%", "75%", "80%", "85%", "90%", "95%"], value=SETTINGS["analysis_defaults"]["confidence_threshold"])
    st.checkbox("Include legal references by default", value=SETTINGS["analysis_defaults"]["include_legal_references"])
    st.markdown("</div>", unsafe_allow_html=True)


def main():
    render_css()
    page = render_sidebar()
    if page == "Dashboard":
        dashboard_page()
    elif page == "Upload Analysis":
        upload_analysis_page()
    elif page == "Analysis Progress":
        analysis_progress_page()
    elif page == "Results Dashboard":
        results_dashboard_page()
    elif page == "Detailed Finding":
        detailed_finding_page()
    elif page == "Report Preview":
        report_preview_page()
    elif page == "Legal Library":
        legal_library_page()
    elif page == "Settings":
        settings_page()


if __name__ == "__main__":
    main()
