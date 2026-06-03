import streamlit as st

st.set_page_config(
    page_title="Employee Attrition Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
:root {
    --blue-900: #0A2463; --blue-700: #1447A6; --blue-500: #2563EB;
    --blue-400: #3B82F6; --blue-100: #DBEAFE; --blue-50: #EFF6FF;
    --accent: #F59E0B; --white: #FFFFFF; --gray-50: #F8FAFC;
    --gray-100: #F1F5F9; --gray-200: #E2E8F0; --gray-600: #475569;
    --red-500: #EF4444; --green-500:#22C55E;
}
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; background-color: var(--white) !important; color: #1E293B; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, var(--blue-900) 0%, var(--blue-700) 100%) !important; border-right: none !important; }
[data-testid="stSidebar"] * { color: var(--white) !important; }
[data-testid="stSidebar"] .stRadio > label { font-weight: 600; letter-spacing: .03em; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,.2) !important; }
.main .block-container { padding: 2rem 2.5rem 3rem; max-width: 1300px; }
.page-header { background: linear-gradient(135deg, var(--blue-900) 0%, var(--blue-500) 100%); border-radius: 16px; padding: 2.2rem 2.5rem; margin-bottom: 2rem; color: white; position: relative; overflow: hidden; }
.page-header::after { content: ''; position: absolute; top: -60px; right: -60px; width: 220px; height: 220px; background: rgba(255,255,.06); border-radius: 50%; }
.page-header h1 { font-family:'Plus Jakarta Sans',sans-serif; font-size:1.9rem; font-weight:800; margin:0 0 .4rem; }
.page-header p { font-size:.95rem; opacity:.85; margin:0; }
.kpi-card { background: var(--white); border: 1px solid var(--gray-200); border-radius: 14px; padding: 1.4rem 1.6rem; box-shadow: 0 1px 6px rgba(0,0,0,.06); transition: transform .2s, box-shadow .2s; }
.kpi-card:hover { transform: translateY(-3px); box-shadow: 0 6px 20px rgba(0,0,.1); }
.kpi-label { font-size:.78rem; font-weight:600; text-transform:uppercase; letter-spacing:.08em; color:var(--gray-600); margin-bottom:.5rem; }
.kpi-value { font-family:'Plus Jakarta Sans',sans-serif; font-size:2.1rem; font-weight:800; color:var(--blue-900); line-height:1; }
.kpi-delta { font-size:.82rem; margin-top:.4rem; } .kpi-delta.up { color: var(--red-500); } .kpi-delta.down { color: var(--green-500); }
.section-card { background: var(--white); border: 1px solid var(--gray-200); border-radius: 14px; padding: 1.6rem 1.8rem; box-shadow: 0 1px 6px rgba(0,0,0,.05); margin-bottom: 1.4rem; }
.section-title { font-family:'Plus Jakarta Sans',sans-serif; font-size:1.05rem; font-weight:700; color:var(--blue-900); margin-bottom:1rem; padding-bottom:.6rem; border-bottom: 2px solid var(--blue-100); }
.insight-box { background: var(--blue-50); border-left: 4px solid var(--blue-500); border-radius: 0 10px 0; padding: .9rem 1.1rem; margin: .6rem 0; font-size:.88rem; line-height:1.55; }
.rec-box { background: #FFFBEB; border-left: 4px solid var(--accent); border-radius: 0 10px 10px 0; padding: .9rem 1.1rem; margin: .6rem 0; font-size:.88rem; line-height:1.55; }
.badge { display:inline-block; padding:.18rem .65rem; border-radius:999px; font-size:.75rem; font-weight:600; margin:0 .2rem; }
.badge-blue { background:var(--blue-100); color:var(--blue-700); } .badge-red { background:#FEE2E2; color:#B91C1C; }
.badge-green { background:#DCFCE7; color:#15803D; } .badge-amber { background:#FEF3C7; color:#92400E; }
.divider { height:1px; background:var(--gray-200); margin:1.6rem 0; border:none; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.sidebar.title("Kayfa")
    try: st.image("kayfa_logo.png", width='stretch')
    except Exception: st.markdown("### 🏢 Kayfa")
    st.markdown("---"); st.markdown("**NAVIGATION**")
    page = st.radio("Navigation", ["🏠  Overview","📈  Attrition by Job & Career","🏡  Workplace & Flexibility","🧑🤝🧑  Demographics","⚖   Work-Life & Wellbeing","🎯  Key Findings & Recommendations"], label_visibility="collapsed")
    st.markdown("---"); st.markdown("Employee Attrition Analysis  \n`Dataset: Train + Test merged`")

# ── CHANGED: pages. → views. ─────────────────────────────────────
if   "Overview"     in page: import views.page1_overview        as pg
elif "Job & Career" in page: import views.page2_job_career      as pg
elif "Workplace"    in page: import views.page3_workplace       as pg
elif "Demographics" in page: import views.page4_demographics    as pg
elif "Wellbeing"    in page: import views.page5_wellbeing       as pg
elif "Key Findings" in page: import views.page6_recommendations as pg
pg.show()