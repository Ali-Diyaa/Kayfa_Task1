"""
PAGE 5 – Work-Life Balance & Wellbeing
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

    title_col, logo_col = st.columns([6, 2])
    with title_col:
        st.markdown("## Work-Life Balance & Wellbeing")
    
    with logo_col:
        if logo_path.exists():
            st.image(str(logo_path), width=300)

    st.markdown("""
    <div class="page-header">
        <h1>⚖ Work-Life Balance & Wellbeing</h1>
        <p>Examining how work-life balance, performance recognition, and employee engagement shape retention.</p>
    </div>
    """, unsafe_allow_html=True)

    wlb_df = _rate_df(df, "Work-Life Balance")
    wlb_map = {row["Work-Life Balance"]: row["Left_Rate"] for _, row in wlb_df.iterrows()}
    poor, fair, good, exc = wlb_map.get("Poor",0), wlb_map.get("Fair",0), wlb_map.get("Good",0), wlb_map.get("Excellent",0)

    c1, c2, c3, c4 = st.columns(4)
    for col, label, val, color in [
        (c1, "Poor WLB – Attrition", f"{poor:.1f}%", "#EF4444"),
        (c2, "Fair WLB – Attrition", f"{fair:.1f}%", "#F97316"),
        (c3, "Good WLB – Attrition", f"{good:.1f}%", "#F59E0B"),
        (c4, "Excellent WLB – Attrition", f"{exc:.1f}%", "#22C55E"),
    ]:
        with col:
            st.markdown(f"""<div class="kpi-card" style="border-top:4px solid {color}">
                <div class="kpi-label">{label}</div><div class="kpi-value" style="color:{color}">{val}</div></div>""", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    feature = st.selectbox("🔍 Choose Wellbeing Dimension",
        ["Work-Life Balance (Q6)", "Employee Recognition", "Performance Rating", "Company Size"], index=0, key="page5_wlb_select")

    if "Work-Life" in feature:
        col_l, col_r = st.columns([1.3, 1])
        with col_l:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Attrition Rate by Work-Life Balance</div>', unsafe_allow_html=True)
            order_wlb = ["Poor","Fair","Good","Excellent"]
            wlb_df["Work-Life Balance"] = pd.Categorical(wlb_df["Work-Life Balance"], categories=order_wlb, ordered=True)
            wlb_sorted = wlb_df.sort_values("Work-Life Balance")
            fig = go.Figure(go.Bar(x=wlb_sorted["Work-Life Balance"].astype(str), y=wlb_sorted["Left_Rate"],
                marker_color=["#EF4444","#F97316","#F59E0B","#22C55E"],
                text=[f"{v:.1f}%" for v in wlb_sorted["Left_Rate"]], textposition="outside", width=0.45))
            fig.update_layout(yaxis_title="Left Rate (%)", height=280, margin=dict(t=20,b=20,l=20,r=20))
            st.plotly_chart(fig, use_container_width=True, key="p5_wlb_bar")

            # ── Q6 HEATMAP ──────────────────────────
            st.markdown('<div class="section-title">Q6: Job Satisfaction × Work-Life Balance</div>', unsafe_allow_html=True)
            q6 = df.groupby(['Job Satisfaction','Work-Life Balance'], observed=False).agg(Rate=('Attrition', lambda x: (x=='Left').mean()*100)).reset_index()
            q6_pivot = q6.pivot(index='Job Satisfaction', columns='Work-Life Balance', values='Rate')
            q6_pivot = q6_pivot.reindex(index=['Low','Medium','High','Very High'], columns=order_wlb)
            fig_q6 = px.imshow(q6_pivot, text_auto='.1f', aspect='auto', color_continuous_scale='RdYlGn_r', labels=dict(color="Attrition %"))
            fig_q6.update_layout(height=340, margin=dict(t=20,b=20))
            st.plotly_chart(fig_q6, use_container_width=True, key="p5_q6_heat")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_r:
            st.markdown('<div class="section-card"><div class="section-title">Key Insights</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="insight-box">WLB improves → attrition drops:
            <span class="badge badge-red">Poor {poor:.0f}%</span>
            <span class="badge badge-amber">Fair {fair:.0f}%</span>
            <span class="badge badge-green">Good {good:.0f}%</span>
            <span class="badge badge-blue">Excellent {exc:.0f}%</span></div>
            <div class="insight-box"><strong>Q6 Answer – Worst combo:</strong> Low Satisfaction + Poor WLB = <strong>67.0%</strong> attrition. Even Very High Satisfaction + Poor WLB = 64.9%.</div>
            <div class="insight-box"><strong>Best combo:</strong> High Satisfaction + Excellent WLB = <strong>32.7%</strong>.</div>
            <div class="rec-box">Poor WLB overrides satisfaction — fix workload before perks.</div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    elif feature == "Employee Recognition":
        # ... keep your existing code unchanged ...
        recog_df = _rate_df(df, "Employee Recognition").sort_values("Left_Rate", ascending=False)
        col_l, col_r = st.columns([1.3, 1])
        with col_l:
            st.markdown('<div class="section-card"><div class="section-title">Attrition by Recognition Level</div>', unsafe_allow_html=True)
            fig2 = px.bar(recog_df, x="Employee Recognition", y="Left_Rate", text=recog_df["Left_Rate"].map(lambda v: f"{v:.1f}%"),
                color="Left_Rate", color_continuous_scale=["#22C55E","#F59E0B","#EF4444"])
            fig2.update_traces(textposition="outside")
            fig2.update_layout(height=300, yaxis_title="Left Rate (%)", coloraxis_showscale=False)
            st.plotly_chart(fig2, use_container_width=True, key="p5_recog_bar")
            st.markdown('</div>', unsafe_allow_html=True)
        with col_r:
            st.markdown('<div class="section-card"><div class="section-title">Key Insight</div>', unsafe_allow_html=True)
            st.markdown("""<div class="insight-box">Low recognition = higher attrition — feeling unseen drives exits.</div>
            <div class="rec-box">Build monthly shout-outs and manager appreciation rituals.</div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    elif feature == "Performance Rating":
        perf_df = _rate_df(df, "Performance Rating").sort_values("Performance Rating")
        col_l, col_r = st.columns([1.3, 1])
        with col_l:
            st.markdown('<div class="section-card"><div class="section-title">Attrition by Performance Rating</div>', unsafe_allow_html=True)
            fig3 = px.line(perf_df, x="Performance Rating", y="Left_Rate", markers=True, text=perf_df["Left_Rate"].map(lambda v: f"{v:.1f}%"))
            fig3.update_traces(line_color="#2563EB", textposition="top center")
            fig3.update_layout(height=300, yaxis_title="Left Rate (%)")
            st.plotly_chart(fig3, use_container_width=True, key="p5_perf_line")
            st.markdown('</div>', unsafe_allow_html=True)
        with col_r:
            st.markdown('<div class="section-card"><div class="section-title">Key Insight</div>', unsafe_allow_html=True)
            st.markdown("""<div class="insight-box">Low performers leave most (57.1%), but high performers also leave if not recognized.</div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        size_df = _rate_df(df, "Company Size")
        st.markdown('<div class="section-card"><div class="section-title">Attrition by Company Size</div>', unsafe_allow_html=True)
        fig4 = px.bar(size_df, x="Company Size", y="Left_Rate", text=size_df["Left_Rate"].map(lambda v: f"{v:.1f}%"),
            color="Left_Rate", color_continuous_scale=["#22C55E","#F59E0B","#EF4444"])
        fig4.update_traces(textposition="outside")
        fig4.update_layout(height=270, yaxis_title="Left Rate (%)", coloraxis_showscale=False)
        st.plotly_chart(fig4, use_container_width=True, key="p5_size_bar")
        st.markdown('</div>', unsafe_allow_html=True)