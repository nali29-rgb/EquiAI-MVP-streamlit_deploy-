import streamlit as st
import pandas as pd

# Import your backend engines from the core folder
from core.math_engine import calculate_funnel_bias
from core.llama_agent import generate_compliance_prose
from datetime import datetime


st.set_page_config(page_title="EquiAudit AI", page_icon="⚖️", layout="wide")

# -----------------------------------------------------------------------------
# EXACT BRAND COLOR PALETTE (RGB)
# -----------------------------------------------------------------------------
PRIMARY = "rgb(116, 139, 197)"      # Hex: #748BC5
SECONDARY = "rgb(241, 141, 122)"   # Hex: #F18D7A
BACKGROUND = "rgb(255, 241, 249)"  # Hex: #FFF1F9
TEXT = "rgb(23, 23, 23)"           # Hex: #171717
SURFACE = "#FFFFFF"                 # Crisp white cards for high readability
BORDER = "rgba(116, 139, 197, 0.20)"

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
        "accent_color": PRIMARY,
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
# Custom Modern CSS & Layout Engine
# -----------------------------------------------------------------------------

def render_css():
    st.markdown(
        f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
            
            :root {{
                color-scheme: light;
            }}
            
            html, body, [class*="css"] {{
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
                color: {TEXT} !important;
            }}

            .stApp {{
                background-color: {BACKGROUND} !important;
            }}

            /* Spacing & Layout */
            .block-container {{
                padding-top: 1.5rem !important;
                padding-bottom: 2.5rem !important;
                max-width: 1450px;
            }}

            /* Sidebar Restyling */
            [data-testid="stSidebar"] {{
                background-color: {SURFACE} !important;
                border-right: 1px solid {BORDER} !important;
            }}

            /* Primary Button Component */
            .stButton > button {{
                background: {PRIMARY} !important;
                color: #FFFFFF !important;
                border: none !important;
                border-radius: 10px !important;
                padding: 0.65rem 1.25rem !important;
                font-weight: 600 !important;
                box-shadow: 0 2px 4px rgba(116, 139, 197, 0.25) !important;
                transition: all 0.2s ease !important;
            }}

            .stButton > button:hover {{
                background: {SECONDARY} !important;
                box-shadow: 0 4px 12px rgba(241, 141, 122, 0.35) !important;
                transform: translateY(-1px);
            }}

            /* Container Cards */
            .card {{
                background: {SURFACE};
                border: 1px solid {BORDER};
                border-radius: 16px;
                padding: 1.5rem;
                box-shadow: 0 4px 20px rgba(23, 23, 23, 0.03);
                margin-bottom: 1.25rem;
            }}

            .card-compact {{
                background: {SURFACE};
                border: 1px solid {BORDER};
                border-radius: 12px;
                padding: 1.2rem;
                box-shadow: 0 2px 10px rgba(23, 23, 23, 0.02);
            }}

            .card-hero {{
                background: linear-gradient(135deg, {SURFACE} 0%, {BACKGROUND} 100%);
                border: 1px solid {BORDER};
                border-radius: 18px;
                padding: 1.75rem;
                box-shadow: 0 4px 20px rgba(116, 139, 197, 0.12);
            }}

            /* Section & Typography Styling */
            .section-title {{
                font-size: 1.15rem;
                font-weight: 700;
                color: {TEXT};
                margin-bottom: 0.35rem;
            }}

            .small-muted {{
                color: rgba(23, 23, 23, 0.65);
                font-size: 0.9rem;
            }}

            .metric-title {{
                color: rgba(23, 23, 23, 0.65);
                font-size: 0.875rem;
                font-weight: 500;
                margin-bottom: 0.25rem;
            }}

            .metric-value {{
                font-size: 2rem;
                font-weight: 700;
                color: {TEXT};
                letter-spacing: -0.02em;
                margin-bottom: 0.25rem;
            }}

            .metric-note {{
                font-size: 0.85rem;
                color: {PRIMARY};
                font-weight: 600;
            }}

            /* Risk Status Badges */
            .risk-badge {{
                display: inline-flex;
                align-items: center;
                padding: 0.3rem 0.75rem;
                border-radius: 999px;
                font-size: 0.8rem;
                font-weight: 600;
            }}
            .badge-low {{ background: rgba(116, 139, 197, 0.15); color: {PRIMARY}; border: 1px solid rgba(116, 139, 197, 0.3); }}
            .badge-medium {{ background: rgba(241, 141, 122, 0.15); color: {SECONDARY}; border: 1px solid rgba(241, 141, 122, 0.3); }}
            .badge-high {{ background: #FFEBEB; color: #D93838; border: 1px solid #FFC2C2; }}

            /* Table Formatting */
            .table-card {{
                width: 100%;
                border-collapse: collapse;
            }}
            .table-card th {{
                text-align: left;
                padding: 0.85rem 0.75rem;
                color: {TEXT};
                font-size: 0.85rem;
                font-weight: 700;
                border-bottom: 1px solid {BORDER};
            }}
            .table-card td {{
                padding: 0.85rem 0.75rem;
                border-bottom: 1px solid rgba(23, 23, 23, 0.05);
                font-size: 0.9rem;
            }}

            /* Top Nav Styling */
            .top-nav__pill {{
                background: {SECONDARY};
                color: #FFFFFF;
                padding: 0.45rem 0.85rem;
                border-radius: 999px;
                font-size: 0.85rem;
                font-weight: 600;
            }}

            /* Dropzone Customization */
            [data-testid="stFileUploader"] {{
                background-color: {SURFACE} !important;
                border: 2px dashed {BORDER} !important;
                border-radius: 12px !important;
                padding: 1rem !important;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_top_navigation(page_name: str):
    left, middle, right = st.columns([3, 3, 2], gap="large")
    with left:
        st.markdown(f"<div style='padding-top: 0.5rem;'><strong>{SETTINGS['workspace_name']}</strong></div>", unsafe_allow_html=True)
    with middle:
        query = st.text_input("Search workspace", placeholder="Search reports, keywords, laws...", key="top_search", label_visibility="collapsed")
        if query:
            st.info(f"Search results for: {query}")
    with right:
        st.markdown(
            "<div style='display:flex; gap:0.5rem; justify-content:flex-end; padding-top: 0.25rem;'>"
            "<span class='top-nav__pill'>Notifications</span>"
            "<span class='top-nav__pill'>Profile</span>"
            "</div>",
            unsafe_allow_html=True,
        )
    st.markdown("<hr style='border:none; border-top:1px solid rgba(116, 139, 197, 0.2); margin:1rem 0 1.5rem 0;' />", unsafe_allow_html=True)


def render_sidebar():
    st.sidebar.markdown("## Navigation")
    page = st.sidebar.radio("", PAGE_OPTIONS, index=0)
    st.sidebar.markdown("---")
    st.sidebar.markdown("## Quick actions")
    st.sidebar.button("Start compliance review")
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
# Page Renderers
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

    st.write(" ")
    st.markdown("<div class='card'> <div class='section-title'>Risk trend analysis</div>", unsafe_allow_html=True)
    st.line_chart(RISK_TREND)
    st.markdown("</div>", unsafe_allow_html=True)

    st.write(" ")
    left, right = st.columns([2, 1], gap="large")
    with left:
        render_section("Recent analyses", "Latest compliance and bias audit reports")
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
            <table class='table-card'>
                <thead><tr><th>Analysis</th><th>Date</th><th>Score</th><th>Status</th><th>Risk</th></tr></thead>
                <tbody>
            """
            + table_rows +
            "</tbody></table></div>",
            unsafe_allow_html=True,
        )
    with right:
        render_section("Quick actions", "Launch or share findings")
        st.markdown(
            "<div class='card'>"
            "<div style='display:grid; gap:0.75rem'>"
            "<button class='stButton'>Upload hiring dataset</button>"
            "<button class='stButton'>Review bias finding</button>"
            "<button class='stButton'>Export report preview</button>"
            "</div></div>",
            unsafe_allow_html=True,
        )


def upload_analysis_page():
    render_top_navigation("Upload Analysis")
    st.markdown("<div class='card-hero'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Upload hiring datasets</div>", unsafe_allow_html=True)
    st.write("Drag CSV or Excel applicant files into the stage below to trigger automated bias and legal compliance checks.")
    
    selected_ats = st.selectbox(
        "Target ATS Platform:", 
        ["Greenhouse", "Workday Recruiting"]
    )
    
    uploaded_files = st.file_uploader("Upload applicant data", type=["csv", "xlsx", "json"], accept_multiple_files=True)
    
    if uploaded_files:
        st.success(f"{len(uploaded_files)} file(s) uploaded and staged for analysis.")
        for f in uploaded_files:
            st.markdown(f"- **{f.name}** · *{round(f.size / 1024, 1)} KB*")
        
        if st.button("Analyze dataset", key="start_analysis"):
            with st.spinner("Running Math Engine & querying Llama Compliance Engine..."):
                target_file = uploaded_files[0]
                df = pd.read_csv(target_file)
                
                metrics = calculate_funnel_bias(df)
                report = generate_compliance_prose(metrics, selected_ats)
                
                st.divider()
                st.markdown(report)
    else:
        st.info("Drop a supported dataset or click to browse files.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.write(" ")
    settings_card = st.columns([2, 1], gap="large")
    with settings_card[0]:
        render_section("Analysis settings", "Customize the audit before execution")
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.selectbox("Review scope", ["All departments", "Customer support", "Engineering", "Sales"], index=0)
        st.selectbox("Compliance profile", ["Standard bias audit", "AI regulation deep scan", "EEOC readiness check"], index=0)
        st.checkbox("Include legal references in output", value=True)
        st.select_slider("Confidence threshold", options=["70%", "75%", "80%", "85%", "90%", "95%"], value="85%")
        st.markdown("</div>", unsafe_allow_html=True)
    with settings_card[1]:
        render_section("Upload guide", "Supported inputs")
        st.markdown(
            "<div class='card'>"
            "<ul style='padding-left:1.15rem; color:rgb(23, 23, 23);'>"
            "<li>CSV, Excel, JSON exports</li>"
            "<li>Candidate stage outcomes</li>"
            "<li>Demographic metadata</li>"
            "<li>Instant batch processing</li>"
            "</ul>"
            "</div>",
            unsafe_allow_html=True,
        )


def analysis_progress_page():
    render_top_navigation("Analysis Progress")
    render_section("Analysis in progress", "Data pipeline workflow")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.progress(0.76)
    st.write("**76% complete — estimated 90 seconds remaining**")
    steps = [
        ("Reading applicant files", True),
        ("Cleaning demographic data", True),
        ("Identifying proxy keywords", True),
        ("Calculating EEOC impact ratios", True),
        ("Querying multi-jurisdictional legal engine", False),
        ("Generating ATS configuration steps", False),
        ("Rendering final audit report", False),
    ]
    for label, done in steps:
        icon = "✅" if done else "⏳"
        st.markdown(f"- {icon} **{label}**")
    st.markdown("</div>", unsafe_allow_html=True)


def results_dashboard_page():
    render_top_navigation("Results Dashboard")
    top_metrics = st.columns(4, gap="large")
    stats = [
        ("Overall risk score", "78/100", "Moderate priority review needed"),
        ("Compliance score", "84%", "Aligned with EEOC benchmarks"),
        ("Critical findings", "3", "Items requiring policy fixes"),
        ("Legal references", "12", "Statutes checked in scan"),
    ]
    for index, info in enumerate(stats):
        with top_metrics[index]:
            render_summary_card(info[0], info[1], info[2])

    st.write(" ")
    left, right = st.columns([2, 1], gap="large")
    with left:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Overall risk status</div>", unsafe_allow_html=True)
        st.markdown("<div style='height: 200px; display:flex; align-items:center; justify-content:center;'>"
                    "<div style='width: 85%; height: 16px; background: rgba(116, 139, 197, 0.2); border-radius: 999px; overflow:hidden;'>"
                    "<div style='width: 78%; height: 100%; background: rgb(116, 139, 197);'></div>"
                    "</div></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Key findings</div>", unsafe_allow_html=True)
        st.write("- Screening leak concentrated in early availability rules.")
        st.write("- Legal exposure identified for continuous career history proxies.")
        st.write("- Immediate ATS scorecard re-configuration recommended.")
        st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("Potential biases detected", expanded=True):
        bias_tabs = st.columns(3, gap="large")
        bias_scores = [
            ("Gender bias", "High", "Review criteria for gendered language."),
            ("Age bias", "Medium", "Assess requirements penalizing career gaps."),
            ("Education bias", "Low", "Replace prestige cues with skills tests."),
        ]
        for index, item in enumerate(bias_scores):
            with bias_tabs[index]:
                render_summary_card(item[0], item[1], item[2])
                
    with st.expander("Detected keywords", expanded=False):
        keywords = pd.DataFrame([
            {"Keyword": "On-site availability", "Count": 26, "Severity": "High"},
            {"Keyword": "College prestige", "Count": 18, "Severity": "Medium"},
            {"Keyword": "Parenting gap", "Count": 12, "Severity": "High"},
        ])
        st.table(keywords)


def detailed_finding_page():
    render_top_navigation("Detailed Finding")
    title = st.selectbox("Choose flagged issue", [item["keyword"] for item in DETAILED_FINDINGS])
    issue = next(item for item in DETAILED_FINDINGS if item["keyword"] == title)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>{issue['keyword']}</div>", unsafe_allow_html=True)
    left, right = st.columns(2, gap="large")
    with left:
        st.markdown(f"<div class='metric-title'>Frequency</div><div class='metric-value'>{issue['frequency']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-title'>Accepted %</div><div class='metric-value'>{issue['accepted']}</div>", unsafe_allow_html=True)
    with right:
        st.markdown(f"<div class='metric-title'>Confidence</div><div class='metric-value'>{issue['confidence']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-title'>Category</div><div class='metric-value'>{issue['category']}</div>", unsafe_allow_html=True)
    st.markdown("<hr style='border:none; border-top:1px solid rgba(116, 139, 197, 0.2); margin:1rem 0;' />", unsafe_allow_html=True)
    st.markdown(f"**Explanation:** {issue['explanation']}")
    st.markdown("**Legal references:**")
    for ref in issue["legal_refs"]:
        st.markdown(f"- {ref}")
    st.markdown(f"**Suggested fix:** {issue['suggestion']}")
    st.markdown("</div>", unsafe_allow_html=True)


def report_preview_page():
    render_top_navigation("Report Preview")
    top = st.columns([3, 1], gap="large")
    with top[0]:
        render_section("Report preview", "PDF layout preview")
    with top[1]:
        st.button("Export PDF")

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Executive Summary</div>", unsafe_allow_html=True)
    st.write("**Overall risk score:** 78/100")
    st.write("**Compliance score:** 84%")
    st.write("EquiAudit AI identified priority bias signals in candidate screening and keyword-based filtering.")
    st.markdown("</div>", unsafe_allow_html=True)


def legal_library_page():
    render_top_navigation("Legal Library")
    search_term = st.text_input("Search legal references", placeholder="Search federal, state, EEOC, NIST rules")
    filtered = [law for law in LEGAL_LIBRARY if not search_term or search_term.lower() in law["title"].lower()]
    for law in filtered:
        st.markdown(
            f"<div class='card'>"
            f"<div class='section-title'>{law['title']} — <span style='color:{PRIMARY}; font-size:0.9rem;'>{law['category']}</span></div>"
            f"<p style='margin-bottom:0.5rem;'>{law['summary']}</p>"
            f"<small style='color:rgba(23,23,23,0.7);'>{law['details']}</small>"
            f"</div>",
            unsafe_allow_html=True,
        )


def settings_page():
    render_top_navigation("Settings")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Workspace settings</div>", unsafe_allow_html=True)
    st.text_input("Workspace name", value=SETTINGS["workspace_name"])
    st.text_input("Primary notification email", value=SETTINGS["email"])
    st.checkbox("Weekly summary emails", value=SETTINGS["notifications"]["weekly_summary"])
    st.checkbox("Report ready alerts", value=SETTINGS["notifications"]["report_ready"])
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
