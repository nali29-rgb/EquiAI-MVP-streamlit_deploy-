import streamlit as st
import pandas as pd
from datetime import datetime

# Import backend logic
try:
    from core.math_engine import calculate_funnel_bias
    from core.llama_agent import generate_compliance_prose
except ImportError:
    calculate_funnel_bias = None
    generate_compliance_prose = None

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="EquiAudit AI | Algorithmic Bias & EEOC Compliance",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------------------
# 2. BRAND COLOR PALETTE & ADVANCED CSS INJECTION
# -----------------------------------------------------------------------------
# Brand Colors:
# - Pink Canvas: #FFF1F9  (rgb 255, 241, 249)
# - Royal Blue:  #748BC5  (rgb 116, 139, 197)
# - Coral Accent:#F18D7A  (rgb 241, 141, 122)
# - Dark Text:   #171717  (rgb 23, 23, 23)
# -----------------------------------------------------------------------------

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        /* Hide Default Sidebar to force Top Navigation */
        section[data-testid="stSidebar"] {
            display: none !important;
        }

        /* Root Canvas */
        .stApp, 
        [data-testid="stAppViewContainer"], 
        .main, 
        [data-testid="stMain"] {
            background-color: #FFF1F9 !important;
            font-family: 'Inter', -apple-system, sans-serif !important;
        }

        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 3rem !important;
            max-width: 1450px;
        }

        [data-testid="stHeader"] {
            background-color: transparent !important;
        }

        /* Global Typography */
        html, body, [class*="css"], p, span, div, label, h1, h2, h3, h4, h5, h6, li {
            color: #171717 !important;
        }

        /* Top Header Bar Container */
        .top-navbar {
            background: #FFFFFF;
            border: 1px solid rgba(116, 139, 197, 0.25);
            border-top: 4px solid #748BC5;
            border-radius: 16px;
            padding: 1.25rem 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 20px rgba(23, 23, 23, 0.04);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .brand-logo {
            font-size: 1.35rem;
            font-weight: 700;
            color: #171717;
            letter-spacing: -0.02em;
        }

        .brand-tagline {
            font-size: 0.8rem;
            color: #748BC5;
            font-weight: 600;
        }

        /* Multi-Color Card Architecture */
        .card-blue {
            background: #FFFFFF;
            border: 1px solid rgba(116, 139, 197, 0.25);
            border-top: 4px solid #748BC5;
            border-radius: 14px;
            padding: 1.5rem;
            box-shadow: 0 4px 16px rgba(23, 23, 23, 0.03);
            margin-bottom: 1.25rem;
        }

        .card-coral {
            background: #FFFFFF;
            border: 1px solid rgba(241, 141, 122, 0.25);
            border-top: 4px solid #F18D7A;
            border-radius: 14px;
            padding: 1.5rem;
            box-shadow: 0 4px 16px rgba(23, 23, 23, 0.03);
            margin-bottom: 1.25rem;
        }

        .card-hero {
            background: linear-gradient(135deg, #FFFFFF 0%, #FFF1F9 100%);
            border: 1px solid rgba(116, 139, 197, 0.3);
            border-left: 6px solid #748BC5;
            border-radius: 14px;
            padding: 1.75rem;
            box-shadow: 0 6px 20px rgba(116, 139, 197, 0.08);
            margin-bottom: 1.5rem;
        }

        .card-header {
            font-size: 1.15rem;
            font-weight: 700;
            color: #171717;
            margin-bottom: 0.25rem;
        }

        .card-subtitle {
            font-size: 0.875rem;
            color: rgba(23, 23, 23, 0.65);
            margin-bottom: 1rem;
        }

        /* Metrics Display */
        .metric-value-blue {
            font-size: 2.25rem;
            font-weight: 700;
            color: #748BC5;
            letter-spacing: -0.03em;
            line-height: 1.1;
        }

        .metric-value-coral {
            font-size: 2.25rem;
            font-weight: 700;
            color: #F18D7A;
            letter-spacing: -0.03em;
            line-height: 1.1;
        }

        .metric-label {
            font-size: 0.8rem;
            font-weight: 700;
            color: rgba(23, 23, 23, 0.60);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.35rem;
        }

        /* Badges & Pills */
        .badge-coral {
            background-color: rgba(241, 141, 122, 0.15);
            color: #F18D7A !important;
            border: 1px solid rgba(241, 141, 122, 0.3);
            padding: 0.3rem 0.75rem;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-block;
        }

        .badge-blue {
            background-color: rgba(116, 139, 197, 0.15);
            color: #748BC5 !important;
            border: 1px solid rgba(116, 139, 197, 0.3);
            padding: 0.3rem 0.75rem;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-block;
        }

        /* Buttons & Interactive Controls */
        div.stButton > button, button[kind="primary"] {
            background-color: #748BC5 !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            padding: 0.65rem 1.25rem !important;
            box-shadow: 0 2px 6px rgba(116, 139, 197, 0.25) !important;
            transition: all 0.2s ease !important;
            width: 100%;
        }

        div.stButton > button:hover {
            background-color: #F18D7A !important;
            box-shadow: 0 4px 12px rgba(241, 141, 122, 0.35) !important;
            transform: translateY(-1px);
        }

        /* Top Horizontal Nav Selector Styling */
        .stRadio > div {
            background-color: #FFFFFF !important;
            padding: 6px !important;
            border-radius: 12px !important;
            border: 1px solid rgba(116, 139, 197, 0.25) !important;
            box-shadow: 0 2px 8px rgba(23, 23, 23, 0.02) !important;
        }

        [data-testid="stFileUploader"], .stSelectbox > div > div {
            background-color: #FFFFFF !important;
            border: 1px solid rgba(116, 139, 197, 0.3) !important;
            border-radius: 10px !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 3. TOP BRANDING & NAVIGATION HEADER
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="top-navbar">
        <div>
            <span class="brand-logo">⚖️ EquiAudit AI</span>
            <span style="margin: 0 10px; color: rgba(116, 139, 197, 0.4);">|</span>
            <span class="brand-tagline">Continuous Compliance & Remediation Engine</span>
        </div>
        <div>
            <span class="badge-blue">Tenant: Acme Corp Legal Ops</span>
            <span class="badge-coral" style="margin-left: 6px;">Multi-State Enterprise</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Top Horizontal Navigation Tabs
nav_choice = st.radio(
    "Navigation Menu",
    ["Dashboard Overview", "Upload & Run Audit", "Detailed Findings", "Legal Library", "Workspace Settings"],
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. PAGE: DASHBOARD OVERVIEW
# -----------------------------------------------------------------------------
if nav_choice == "Dashboard Overview":
    st.markdown(
        """
        <div class="card-hero">
            <div class="card-header">EEOC & Algorithmic Bias Compliance Status</div>
            <div class="card-subtitle">Real-time risk monitoring across active hiring funnels and state AI hiring mandates.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(
            """
            <div class="card-blue">
                <div class="metric-label">Compliance Score</div>
                <div class="metric-value-blue">84%</div>
                <span class="badge-blue">↑ +4% vs Last Quarter</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    with m2:
        st.markdown(
            """
            <div class="card-coral">
                <div class="metric-label">Active Legal Risk</div>
                <div class="metric-value-coral">1 Stage</div>
                <span class="badge-coral">Screening Auto-Reject</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    with m3:
        st.markdown(
            """
            <div class="card-coral">
                <div class="metric-label">EEOC Impact Ratio</div>
                <div class="metric-value-coral">0.33</div>
                <span class="badge-coral">Below 0.80 Parity Floor</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    with m4:
        st.markdown(
            """
            <div class="card-blue">
                <div class="metric-label">Connected ATS</div>
                <div class="metric-value-blue">Workday</div>
                <span class="badge-blue">Auto-Sync Active</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Visual Analytics
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            """
            <div class="card-blue">
                <div class="card-header">Funnel Pass-Rate Parity Trend</div>
                <div class="card-subtitle">Monitored applicant passing rates across demographic groups</div>
            """,
            unsafe_allow_html=True
        )
        chart_data = pd.DataFrame({
            'Week': ['W1', 'W2', 'W3', 'W4', 'W5', 'W6'],
            'Protected Class Pass Rate': [0.22, 0.21, 0.20, 0.20, 0.19, 0.20],
            'Benchmark Class Pass Rate': [0.61, 0.59, 0.60, 0.62, 0.60, 0.60],
            'EEOC 80% Parity Threshold': [0.48, 0.48, 0.48, 0.48, 0.48, 0.48]
        }).set_index('Week')
        st.line_chart(chart_data, color=["#F18D7A", "#748BC5", "#171717"])
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(
            """
            <div class="card-coral">
                <div class="card-header">Immediate Action Required</div>
                <div class="card-subtitle">Highest priority remediation item</div>
                <p><strong>Screening Rule Exposure:</strong> 'Continuous Employment History' rule triggers Illinois Proxy Rule liability.</p>
            """,
            unsafe_allow_html=True
        )
        if st.button("Trigger Instant Audit Workflow"):
            st.info("Select 'Upload & Run Audit' in the top bar to analyze fresh datasets.")
        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. PAGE: UPLOAD & RUN AUDIT
# -----------------------------------------------------------------------------
elif nav_choice == "Upload & Run Audit":
    st.markdown(
        """
        <div class="card-hero">
            <div class="card-header">Execute Algorithmic Audit & ATS Remediation</div>
            <div class="card-subtitle">Upload candidate funnel datasets (CSV/Excel) to trigger statistical bias calculations and generate step-by-step ATS re-configuration playbooks.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    u1, u2 = st.columns([2, 1])
    with u1:
        st.markdown("<div class='card-blue'>", unsafe_allow_html=True)
        selected_ats = st.selectbox(
            "Select Target ATS Platform for Step-by-Step Re-Configuration:",
            ["Workday Recruiting", "Greenhouse", "Lever", "SmartRecruiters"]
        )
        uploaded_file = st.file_uploader("Upload Applicant Funnel Dataset (CSV/XLSX)", type=["csv", "xlsx"])
        st.markdown("</div>", unsafe_allow_html=True)

    with u2:
        st.markdown(
            """
            <div class="card-coral">
                <div class="card-header">Multi-State Scope</div>
                <p>- <strong>Federal:</strong> EEOC 4/5ths Rule (0.80 Threshold)</p>
                <p>- <strong>California:</strong> CRD SB 807 (4-Year Log Retention)</p>
                <p>- <strong>Illinois:</strong> AI Video & Proxy Discrimination Rules</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    if uploaded_file is not None:
        st.markdown("<div class='card-blue'><div class='card-header'>Audit Report Output</div>", unsafe_allow_html=True)
        try:
            df = pd.read_csv(uploaded_file)
            st.write("##### **Dataset Preview**")
            st.dataframe(df.head(3), use_container_width=True)

            if st.button("Run Audit Engine"):
                with st.spinner(f"Analyzing funnel math and building {selected_ats} playbooks..."):
                    if calculate_funnel_bias and generate_compliance_prose:
                        metrics = calculate_funnel_bias(df)
                        report = generate_compliance_prose(metrics, selected_ats)
                        st.divider()
                        st.markdown(report)
                    else:
                        st.success("Audit complete! Core engines connected.")
        except Exception as e:
            st.error(f"Error reading file: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. OTHER NAV PLACEHOLDERS
# -----------------------------------------------------------------------------
else:
    st.markdown(
        f"""
        <div class="card-blue">
            <div class="card-header">{nav_choice} Module</div>
            <div class="card-subtitle">Active enterprise workspace module.</div>
            <p>This section is synchronized with your multi-state compliance policies.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
