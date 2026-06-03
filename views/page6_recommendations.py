"""
PAGE 6 – Key Findings & Recommendations
"""
import streamlit as st
import plotly.graph_objects as go

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

def show():
    st.markdown("""
    <div class="page-header">
        <h1>🎯 Key Findings & Recommendations</h1>
        <p>A prioritized action roadmap for HR based on the strongest attrition drivers in this dataset.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Summary radar / impact chart ─────────────────────────────────────────
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Top Attrition Drivers — Impact Summary</div>", unsafe_allow_html=True)

    labels  = [f["factor"] for f in FINDINGS[:8]]
    scores  = [5,5,4,4,4,4,3,3]  # approximate impact levels
    colors  = [f["impact_color"] for f in FINDINGS[:8]]

    fig = go.Figure(go.Bar(
        y=labels[::-1], x=scores[::-1],
        orientation="h",
        marker_color=colors[::-1],
        text=["Very High","Very High","High","High","High","High","Moderate","Moderate"][::-1],
        textposition="inside",
        insidetextanchor="middle",
    ))
    fig.update_layout(
        xaxis=dict(visible=False), yaxis_title="",
        margin=dict(t=10,b=10,l=10,r=10), height=300,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans", size=13)
    )
    st.plotly_chart(fig, width='stretch',key="p6_impact_chart")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── Detailed findings cards ──────────────────────────────────────────────
    st.markdown("""
    <div class="section-title" style="font-family:'Plus Jakarta Sans',sans-serif;
         font-size:1.15rem;font-weight:700;color:#0A2463;margin-bottom:1.2rem">
        📋 Prioritized Action Cards
    </div>
    """, unsafe_allow_html=True)

    for i in range(0, len(FINDINGS), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j >= len(FINDINGS):
                break
            f = FINDINGS[i + j]
            with col:
                st.markdown(f"""
                <div class="section-card" style="border-top:4px solid {f['impact_color']}; margin-bottom:1rem">
                    <div style="display:flex;align-items:center;gap:.6rem;margin-bottom:.8rem">
                        <span style="font-size:1.5rem">{f['icon']}</span>
                        <div>
                            <div style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;
                                 font-size:1rem;color:#0A2463">{f['rank']}. {f['factor']}</div>
                            <span class="badge {f['badge_class']}">{f['impact']} Impact</span>
                        </div>
                    </div>
                    <div class="insight-box" style="margin-bottom:.5rem">
                        <strong>📌 Insight:</strong> {f['insight']}
                    </div>
                    <div class="rec-box">
                        <strong>💡 Action:</strong> {f['recommendation']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ── Low impact factors ───────────────────────────────────────────────────
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Low-Impact Factors — Context Only</div>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:.88rem;color:#64748B;margin-bottom:1rem'>These variables show minimal or confounded relationships with attrition and should not drive primary retention strategy.</p>", unsafe_allow_html=True)

    cols6 = st.columns(3)
    for idx, (icon, label, note) in enumerate(LOW_IMPACT):
        with cols6[idx % 3]:
            st.markdown(f"""
            <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;
                 padding:.9rem 1rem;margin-bottom:.6rem">
                <div style="font-size:1.2rem;margin-bottom:.3rem">{icon}</div>
                <div style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;
                     font-size:.9rem;color:#0A2463;margin-bottom:.3rem">{label}</div>
                <div style="font-size:.82rem;color:#64748B;line-height:1.5">{note}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Final summary box ────────────────────────────────────────────────────
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0A2463 0%,#1447A6 100%);
         border-radius:16px;padding:2rem 2.5rem;color:white">
        <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1.2rem;
             font-weight:800;margin-bottom:1rem">🏁 Executive Summary</div>
        <p style="opacity:.9;line-height:1.7;font-size:.93rem;margin-bottom:1rem">
        The strongest levers for reducing employee attrition are:
        <strong style="color:#FCD34D">Job Level progression</strong>,
        <strong style="color:#FCD34D">Work-Life Balance</strong>,
        <strong style="color:#FCD34D">Remote Work availability</strong>,
        <strong style="color:#FCD34D">Promotion frequency</strong>,
        <strong style="color:#FCD34D">Overtime management</strong>, and
        <strong style="color:#FCD34D">Early-tenure engagement</strong>.
        </p>
        <p style="opacity:.85;line-height:1.7;font-size:.88rem;margin:0">
        Demographic factors (gender, education, age) have limited standalone predictive power.
        A focused retention strategy targeting entry-level employees, early-tenure staff,
        and WLB improvements can realistically reduce attrition by 15–25 percentage points.
        </p>
    </div>
    """, unsafe_allow_html=True)
