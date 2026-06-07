"""
PAGE 6 – Key Findings & Recommendations
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from pathlib import Path
FINDINGS = [
    {
        "rank": 1,
        "icon": "🏆",
        "factor": "Job Level",
        "impact": "Very High",
        "impact_color": "#EF4444",
        "insight": "Entry-level employees leave at 63%, mid at 45%, senior at only 20%. Career stage is the single strongest predictor of attrition.",
        "recommendation": "Build structured career ladders, fast-track programs, and mentorship for entry-level employees. Define clear promotion criteria.",
        "badge_class": "badge-red",
    },
    {
        "rank": 2,
        "icon": "⚖️",
        "factor": "Work-Life Balance",
        "impact": "Very High",
        "impact_color": "#EF4444",
        "insight": "Poor WLB → 60% attrition. Excellent WLB → 35%. A ~25 pp gap — one of the strongest levers available.",
        "recommendation": "Implement flexible hours, no-meeting blocks, mental health leave, and manager training on sustainable workloads.",
        "badge_class": "badge-red",
    },
    {
        "rank": 3,
        "icon": "🏡",
        "factor": "Remote Work",
        "impact": "High",
        "impact_color": "#F59E0B",
        "insight": "Remote workers show up to 28 pp lower attrition vs on-site employees — the top workplace-policy driver.",
        "recommendation": "Expand hybrid/remote options company-wide. Prioritize long-commute employees (50+ km) for remote eligibility first.",
        "badge_class": "badge-amber",
    },
    {
        "rank": 4,
        "icon": "⏰",
        "factor": "Overtime",
        "impact": "High",
        "impact_color": "#F59E0B",
        "insight": "Employees working overtime show significantly higher attrition — a clear burnout signal.",
        "recommendation": "Monitor team-level overtime KPIs. Redistribute work, hire where needed, and compensate extra effort fairly.",
        "badge_class": "badge-amber",
    },
    {
        "rank": 5,
        "icon": "🚀",
        "factor": "Promotion Frequency",
        "impact": "High",
        "impact_color": "#F59E0B",
        "insight": "Employees with 0 promotions have the highest attrition. Each promotion is associated with a meaningful drop in exit rate.",
        "recommendation": "Create a transparent, documented promotion system with defined timelines for each role level.",
        "badge_class": "badge-amber",
    },
    {
        "rank": 6,
        "icon": "⏱️",
        "factor": "Employee Tenure",
        "impact": "High",
        "impact_color": "#F59E0B",
        "insight": "Attrition is concentrated in the first 5 years. Long-tenured employees are highly stable.",
        "recommendation": "Design 90-day, 1-year, and 3-year structured check-in and milestone programs for early-tenure employees.",
        "badge_class": "badge-amber",
    },
    {
        "rank": 7,
        "icon": "💍",
        "factor": "Marital Status",
        "impact": "Moderate",
        "impact_color": "#2563EB",
        "insight": "Single employees leave at 66% vs 36% for married employees — a strong behavioral gap.",
        "recommendation": "Target early-career single employees with community-building, team events, and social engagement programs.",
        "badge_class": "badge-blue",
    },
    {
        "rank": 8,
        "icon": "🏢",
        "factor": "Company Reputation",
        "impact": "Moderate",
        "impact_color": "#2563EB",
        "insight": "Poor perception of company reputation drives higher attrition — organizational brand matters internally.",
        "recommendation": "Run pulse surveys on employer brand. Act visibly on feedback. Celebrate wins and showcase employee impact.",
        "badge_class": "badge-blue",
    },
    {
        "rank": 9,
        "icon": "🚗",
        "factor": "Distance from Home",
        "impact": "Moderate",
        "impact_color": "#2563EB",
        "insight": "Employees living 50-100 km away show ~52% attrition. Commute burden erodes satisfaction.",
        "recommendation": "Offer remote or hybrid arrangements specifically for employees with commutes over 30 km.",
        "badge_class": "badge-blue",
    },
    {
        "rank": 10,
        "icon": "💰",
        "factor": "Monthly Income",
        "impact": "Moderate",
        "impact_color": "#2563EB",
        "insight": "Lower income correlates with higher attrition but is not the dominant factor — career growth matters more.",
        "recommendation": "Review entry-level salary benchmarks against market. Ensure pay equity across roles and genders.",
        "badge_class": "badge-blue",
    },
]

LOW_IMPACT = [
    ("🎓", "Education Level",     "PhD holders show lower attrition (~24%) but overall variation is low. Not a primary focus area."),
    ("⚧",  "Gender",              "Female attrition ~53% vs male ~45% — small gap, likely confounded by job level/OT distribution."),
    ("📊", "Performance Rating",  "Moderate effect. Important to track high-performer flight risk separately."),
    ("🌱", "Innovation Opps",     "~2% difference — supporting innovation helps engagement but isn't a primary retention lever."),
    ("👑", "Leadership Opps",     "~3% difference — valuable for culture, but not a standalone retention solution."),
    ("🏭", "Company Size",        "Small vs large difference is minimal (~3 pp). Size is not a meaningful predictor."),
]

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("employee_attrition_full.csv")
    except FileNotFoundError:
        train = pd.read_csv("train.csv")
        test = pd.read_csv("test.csv")
        df = pd.concat([train, test], ignore_index=True)
    return df

def show():
    df = load_data()
    logo_path = Path(__file__).resolve().parent.parent / "kayfaio_logo.jpg"

    title_col, logo_col = st.columns([6, 2])
    with title_col:
        st.markdown("## Key Findings & Recommendations")
    
    with logo_col:
        if logo_path.exists():
            st.image(str(logo_path), width=300)

    baseline = (df["Attrition"] == "Left").mean() * 100

    st.markdown("""
    <div class="page-header">
        <h1>🎯 Key Findings & Recommendations</h1>
        <p>A prioritized action roadmap for HR based on the strongest attrition drivers in this dataset.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Q9 & Q10 MANAGER ANSWERS ────────────────────
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Q9 & Q10: Direct Manager Questions</div>", unsafe_allow_html=True)

    col_q9, col_q10 = st.columns(2)

    with col_q9:
        # Q9 calculation
        q9 = df.groupby(['Overtime','Number of Promotions']).agg(
            Total=('Attrition','count'),
            Left=('Attrition', lambda x: (x=='Left').sum())
        ).reset_index()
        q9['Rate'] = q9['Left']/q9['Total']*100
        q9['Lift'] = q9['Rate'] - baseline
        q9_top = q9.sort_values('Rate', ascending=False).iloc[0]

        st.markdown(f"""
        <div class="insight-box" style="border-left-color:#EF4444">
            <strong>Q9 – Highest-Risk Profile:</strong><br>
            <strong>Overtime = Yes AND Promotions = 0</strong><br>
            • Attrition: <strong>{q9_top['Rate']:.1f}%</strong> (vs {baseline:.1f}% baseline)<br>
            • Lift: <strong>+{q9_top['Lift']:.1f} pp</strong><br>
            • Population: <strong>{int(q9_top['Total']):,} employees</strong> ({int(q9_top['Left']):,} left)
        </div>
        """, unsafe_allow_html=True)

    with col_q10:
        # Q10 calculation - top 3 drivers
        drivers = []
        for col in ['Marital Status', 'Years at Company', 'Remote Work', 'Overtime']:
            tmp = df.groupby(col).agg(Total=('Attrition','count'), Left=('Attrition', lambda x: (x=='Left').sum())).reset_index()
            tmp['Rate'] = tmp['Left']/tmp['Total']*100
            tmp['Lift'] = tmp['Rate'] - baseline
            tmp['Driver'] = col
            tmp = tmp.rename(columns={col: 'Value'})
            drivers.append(tmp[['Driver','Value','Total','Rate','Lift']])
        q10 = pd.concat(drivers)
        q10 = q10[q10['Total'] >= 300].sort_values('Lift', ascending=False).head(3)

        q10_html = "<div class='insight-box' style='border-left-color:#F59E0B'><strong>Q10 – Top 3 Drivers:</strong><br>"
        for i, row in q10.iterrows():
            q10_html += f"{int(i+1)}. <strong>{row['Driver']} = {row['Value']}</strong> → {row['Rate']:.1f}% (+{row['Lift']:.1f}pp)<br>"
        q10_html += "</div>"
        st.markdown(q10_html, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── YOUR ORIGINAL IMPACT CHART ─────────────────
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Top Attrition Drivers — Impact Summary</div>", unsafe_allow_html=True)

    labels = [f["factor"] for f in FINDINGS[:8]]
    scores = [5,5,4,4,4,4,3,3]
    colors = [f["impact_color"] for f in FINDINGS[:8]]

    fig = go.Figure(go.Bar(y=labels[::-1], x=scores[::-1], orientation="h",
        marker_color=colors[::-1],
        text=["Very High","Very High","High","High","High","High","Moderate","Moderate"][::-1],
        textposition="inside"))
    fig.update_layout(xaxis=dict(visible=False), height=300, margin=dict(t=10,b=10,l=10,r=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True, key="p6_impact_chart")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── KEEP ALL YOUR ORIGINAL FINDINGS CARDS ───────
    st.markdown("""<div class="section-title" style="font-family:'Plus Jakarta Sans',sans-serif;
         font-size:1.15rem;font-weight:700;color:#0A2463;margin-bottom:1.2rem">📋 Prioritized Action Cards</div>""", unsafe_allow_html=True)

    for i in range(0, len(FINDINGS), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j >= len(FINDINGS): break
            f = FINDINGS[i + j]
            with col:
                st.markdown(f"""
                <div class="section-card" style="border-top:4px solid {f['impact_color']}; margin-bottom:1rem">
                    <div style="display:flex;align-items:center;gap:.6rem;margin-bottom:.8rem">
                        <span style="font-size:1.5rem">{f['icon']}</span>
                        <div><div style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;
                             font-size:1rem;color:#0A2463">{f['rank']}. {f['factor']}</div>
                            <span class="badge {f['badge_class']}">{f['impact']} Impact</span></div></div>
                    <div class="insight-box" style="margin-bottom:.5rem"><strong>Insight:</strong> {f['insight']}</div>
                    <div class="rec-box"><strong>Action:</strong> {f['recommendation']}</div>
                </div>""", unsafe_allow_html=True)

    # ── KEEP LOW IMPACT ─────────────────────────────
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-card'><div class='section-title'>Low-Impact Factors — Context Only</div>", unsafe_allow_html=True)
    cols6 = st.columns(3)
    for idx, (icon, label, note) in enumerate(LOW_IMPACT):
        with cols6[idx % 3]:
            st.markdown(f"""<div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;
                 padding:.9rem 1rem;margin-bottom:.6rem"><div style="font-size:1.2rem">{icon}</div>
                <div style="font-weight:700;font-size:.9rem;color:#0A2463">{label}</div>
                <div style="font-size:.82rem;color:#64748B">{note}</div></div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Executive Summary ───────────────────────────
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0A2463 0%,#1447A6 100%);border-radius:16px;padding:2rem 2.5rem;color:white">
        <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1.2rem;font-weight:800;margin-bottom:1rem">Executive Summary</div>
        <p style="opacity:.9;line-height:1.7;font-size:.93rem">The strongest levers are <strong style="color:#FCD34D">Job Level</strong>, <strong style="color:#FCD34D">Work-Life Balance</strong>, <strong style="color:#FCD34D">Remote Work</strong>, <strong style="color:#FCD34D">Promotions</strong>, <strong style="color:#FCD34D">Overtime</strong>, and <strong style="color:#FCD34D">Marital Status (Single)</strong>.</p>
    </div>""", unsafe_allow_html=True)