"""
PAGE 2 – Attrition by Job Level & Career Progression
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path


@st.cache_data
def load_data():
    try:
        df = pd.read_csv("employee_attrition_full.csv")
    except FileNotFoundError:
        train = pd.read_csv("train.csv")
        test = pd.read_csv("test.csv")
        df = pd.concat([train, test], ignore_index=True)
    df["Years at Company"] = df["Years at Company"].apply(lambda x: 41 if x > 41 else x)
    return df

def _rate_df(df, col):
    s = pd.crosstab(df[col], df["Attrition"])
    s["Total"] = s.sum(axis=1)
    s["Left_Rate"] = s["Left"] / s["Total"] * 100
    return s.reset_index()

def show():

    df = load_data()

    logo_path = Path(__file__).resolve().parent.parent / "kayfaio_logo.jpg"

    title_col, logo_col = st.columns([6, 1])
    with title_col:
        st.markdown("## Attrition by Job Level & Career Progression")
    
    with logo_col:
        if logo_path.exists():
            st.image(str(logo_path), width=200)

    st.markdown("""
    <div class="page-header">
        <h1>📈 Attrition by Job Level & Career Progression</h1>
        <p>How job level, promotions, income, and tenure shape an employee's decision to stay or leave.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Job Level KPI ──────────────────────────────────
    jl_df = _rate_df(df, "Job Level")
    entry = jl_df[jl_df["Job Level"]=="Entry"]["Left_Rate"].values[0]
    mid = jl_df[jl_df["Job Level"]=="Mid"]["Left_Rate"].values[0]
    senior = jl_df[jl_df["Job Level"]=="Senior"]["Left_Rate"].values[0]

    c1, c2, c3 = st.columns(3)
    for col, label, val, color in [
        (c1, "Entry-Level Attrition", entry, "#EF4444"),
        (c2, "Mid-Level Attrition", mid, "#F59E0B"),
        (c3, "Senior-Level Attrition", senior, "#22C55E"),
    ]:
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="border-top:4px solid {color}">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value" style="color:{color}">{val:.1f}%</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    feature = st.selectbox("🔍 Choose Analysis Feature",
        ["Job Level", "Promotions", "Monthly Income (Q4)", "Tenure (Q5)"], index=0, key="p2_selector_v3")

    # ── JOB LEVEL ─────────────────────────────────────
    if feature == "Job Level":
        col_l, col_r = st.columns([1.2, 1])
        with col_l:
            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>Attrition Rate by Job Level</div>", unsafe_allow_html=True)
            colors_jl = {"Entry":"#EF4444","Mid":"#F59E0B","Senior":"#22C55E"}
            order = ["Entry","Mid","Senior"]
            rates = {row["Job Level"]: row["Left_Rate"] for _, row in jl_df.iterrows()}
            fig = go.Figure(go.Bar(x=order, y=[rates.get(j,0) for j in order],
                marker_color=[colors_jl[j] for j in order],
                text=[f"{rates.get(j,0):.1f}%" for j in order], textposition="outside", width=0.45))
            fig.update_layout(yaxis=dict(range=[0,80], title="Left Rate (%)"), height=300)
            st.plotly_chart(fig, use_container_width=True, key="p2_job_bar")
            st.markdown("</div>", unsafe_allow_html=True)
        with col_r:
            st.markdown("<div class='section-card'><div class='section-title'>Key Insight</div>", unsafe_allow_html=True)
            st.markdown("""
            <div class="insight-box"><strong>Entry-level = 63.3%</strong> attrition — nearly 2 in 3 leave.</div>
            <div class="insight-box">Mid-level = 45.4%, Senior = 20.3%.</div>
            <div class="rec-box"><strong>Action:</strong> Fast-track growth for Entry staff.</div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # ── PROMOTIONS + Q8 ───────────────────────────────
    elif feature == "Promotions":
        promo_df = _rate_df(df, "Number of Promotions")
        col_l, col_r = st.columns([1.3, 1])
        with col_l:
            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>Q8: Attrition by Number of Promotions</div>", unsafe_allow_html=True)
            fig2 = px.bar(promo_df.sort_values("Number of Promotions"),
                x="Number of Promotions", y="Left_Rate",
                text=promo_df.sort_values("Number of Promotions")["Left_Rate"].map(lambda v: f"{v:.1f}%"),
                color="Left_Rate", color_continuous_scale=["#22C55E","#F59E0B","#EF4444"])
            fig2.update_traces(textposition="outside")
            fig2.update_layout(height=300, yaxis_title="Left Rate (%)", coloraxis_showscale=False)
            st.plotly_chart(fig2, use_container_width=True, key="p2_promo_bar")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_r:
            # Q8 calculation
            df['Stuck'] = (df['Number of Promotions']==0) & (df['Job Level'].isin(['Entry','Mid'])) & (df['Leadership Opportunities']=='No')
            stuck_rate = df[df['Stuck']]['Attrition'].eq('Left').mean()*100
            not_stuck_rate = df[~df['Stuck']]['Attrition'].eq('Left').mean()*100
            st.markdown("<div class='section-card'><div class='section-title'>Q8: Career Stagnation</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="insight-box"><strong>0 promotions = 49.3%</strong> attrition vs <strong>3+ promotions = 24.1%</strong>.</div>
            <div class="insight-box">Stuck employees (0 promo + Entry/Mid + No leadership) leave at <strong>{stuck_rate:.1f}%</strong> vs <strong>{not_stuck_rate:.1f}%</strong> for others.</div>
            <div class="rec-box"><strong>Action:</strong> Create transparent promotion paths at 18-24 months.</div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # ── MONTHLY INCOME + Q4 ───────────────────────────
    elif feature == "Monthly Income (Q4)":
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Q4: Does Higher Pay Reduce Attrition Within the Same Level?</div>", unsafe_allow_html=True)

        df['Pay_Q'] = df.groupby('Job Level')['Monthly Income'].transform(lambda x: pd.qcut(x, 4, labels=['Q1 Low','Q2','Q3','Q4 High']))
        q4 = df.groupby(['Job Level','Pay_Q'], observed=False).agg(Rate=('Attrition', lambda x: (x=='Left').mean()*100)).reset_index()
        q4_pivot = q4.pivot(index='Pay_Q', columns='Job Level', values='Rate')

        fig_q4 = px.imshow(q4_pivot, text_auto='.1f', aspect='auto', color_continuous_scale='RdYlGn_r',
                           labels=dict(color="Attrition %"))
        fig_q4.update_layout(height=320)
        st.plotly_chart(fig_q4, use_container_width=True, key="p2_q4_heat")

        st.markdown("""
        <div class="insight-box"><strong>Q4 Answer:</strong> No. Within the same level, pay barely moves the needle.
        Entry: 64.5% (Q1) → 62.5% (Q4) = -2.0pp. Mid: 46.6% → 45.4% = -1.2pp. Senior: 21.3% → 19.6% = -1.7pp.</div>
        <div class="rec-box"><strong>Action:</strong> Don't rely on raises alone — fix growth and workload.</div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── TENURE + Q5 ───────────────────────────────────
    else:
        col_l, col_r = st.columns([1.3, 1])
        with col_l:
            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>Q5: Retention Timeline by Years at Company</div>", unsafe_allow_html=True)
            ten = df.groupby('Years at Company').agg(Total=('Attrition','count'), Left=('Attrition', lambda x: (x=='Left').sum())).reset_index()
            ten['Rate'] = ten['Left']/ten['Total']*100
            fig5 = px.line(ten, x='Years at Company', y='Rate', markers=True)
            fig5.add_hline(y=df['Attrition'].eq('Left').mean()*100, line_dash="dash", annotation_text="Baseline 47.5%")
            fig5.update_layout(height=300, yaxis_title="Attrition %")
            st.plotly_chart(fig5, use_container_width=True, key="p2_q5_line")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_r:
            st.markdown("<div class='section-card'><div class='section-title'>Q5 Insight</div>", unsafe_allow_html=True)
            st.markdown("""
            <div class="insight-box"><strong>Years 1-9 = danger zone:</strong> 52-54% attrition (peaks at Year 5: 53.8%, Year 9: 53.9%).</div>
            <div class="insight-box"><strong>Year 10+ = stability:</strong> drops to 44.5% and stays 41-46%.</div>
            <div class="rec-box"><strong>Action:</strong> Implement 6-month, 1-year, and 3-year retention checkpoints.</div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)