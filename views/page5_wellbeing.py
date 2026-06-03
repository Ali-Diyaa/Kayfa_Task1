"""
PAGE 5 – Work-Life Balance & Wellbeing
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

    st.markdown("""
    <style>
 .page-header { margin-bottom: 20px; }
 .page-header h1 { font-size: 1.9rem; margin: 0; }
 .page-header p { color: #64748B; margin-top: 6px; }
 .kpi-card { background: white; padding: 16px 18px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
 .kpi-label { font-size: 0.85rem; color: #475569; margin-bottom: 6px; font-weight: 500; }
 .kpi-value { font-size: 1.9rem; font-weight: 700; line-height: 1.2; }
 .section-card { background: white; padding: 18px 20px; border-radius: 14px; box-shadow: 0 2px 10px rgba(0,0,0,0.06); margin-bottom: 16px; }
 .section-title { font-weight: 600; font-size: 1.1rem; margin-bottom: 12px; }
 .divider { height: 1px; background: #e2e8f0; margin: 24px 0; }
 .insight-box { background: #F8FAFC; border-left: 4px solid #2563EB; padding: 12px 14px; border-radius: 8px; margin-bottom: 8px; }
 .rec-box { background: #F0F9FF; border-left: 4px solid #0EA5E9; padding: 12px 14px; border-radius: 8px; margin-top: 8px; }
 .badge { padding: 2px 8px; border-radius: 6px; font-size: 0.8rem; margin-right: 4px; }
 .badge-red { background: #FEE2E2; color: #991B1B; }.badge-amber { background: #FEF3C7; color: #92400E; }
 .badge-green { background: #DCFCE7; color: #166534; }.badge-blue { background: #DBEAFE; color: #1E40AF; }
    </style>
    """, unsafe_allow_html=True)

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
            st.markdown(f"""
            <div class="kpi-card" style="border-top:4px solid {color}">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value" style="color:{color}">{val}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    feature = st.selectbox(
        "🔍 Choose Wellbeing Dimension",
        ["Work-Life Balance", "Employee Recognition", "Performance Rating", "Company Size"],
        index=0,
        key="page5_wlb_select"
    )

    if feature == "Work-Life Balance":
        col_l, col_r = st.columns([1.3, 1])
        with col_l:
            with st.container():
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Attrition Rate by Work-Life Balance</div>', unsafe_allow_html=True)
                order_wlb = ["Poor","Fair","Good","Excellent"]
                wlb_df["Work-Life Balance"] = pd.Categorical(wlb_df["Work-Life Balance"], categories=order_wlb, ordered=True)
                wlb_sorted = wlb_df.sort_values("Work-Life Balance")
                fig = go.Figure(go.Bar(
                    x=wlb_sorted["Work-Life Balance"].astype(str), y=wlb_sorted["Left_Rate"],
                    marker_color=["#EF4444","#F97316","#F59E0B","#22C55E"],
                    text=[f"{v:.1f}%" for v in wlb_sorted["Left_Rate"]], textposition="outside", width=0.45
                ))
                fig.update_layout(yaxis_title="Left Rate (%)", height=320, margin=dict(t=20,b=20,l=20,r=20), paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig, width='stretch', key="p5_wlb_bar")

                st.markdown('<div class="section-title">Bubble: WLB vs Income & Tenure</div>', unsafe_allow_html=True)
                wlb_sum = df.groupby("Work-Life Balance").agg(
                    Total=("Attrition","count"),
                    Left=("Attrition", lambda x: (x=="Left").sum()),
                    Avg_Income=("Monthly Income","mean"),
                    Avg_Tenure=("Years at Company","mean")
                ).reset_index()
                wlb_sum["Left_Rate"] = wlb_sum["Left"]/wlb_sum["Total"]*100
                fig_b = px.scatter(wlb_sum, x="Avg_Tenure", y="Avg_Income", size="Total", color="Left_Rate",
                    hover_name="Work-Life Balance", size_max=60,
                    color_continuous_scale=["#22C55E","#F59E0B","#EF4444"])
                fig_b.update_layout(height=300, xaxis_title="Avg Tenure (yrs)", yaxis_title="Avg Income")
                st.plotly_chart(fig_b, width='stretch', key="p5_wlb_bubble")
                st.markdown('</div>', unsafe_allow_html=True)

        with col_r:
            with st.container():
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Key Insight</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="insight-box">📉 WLB improves → attrition drops:
                <span class="badge badge-red">Poor {poor:.0f}%</span>
                <span class="badge badge-amber">Fair {fair:.0f}%</span>
                <span class="badge badge-green">Good {good:.0f}%</span>
                <span class="badge badge-blue">Excellent {exc:.0f}%</span></div>
                <div class="insight-box">🔥 Poor→Excellent = <strong>~{(poor-exc):.0f}pp</strong> reduction — highest-impact lever.</div>
                <div class="rec-box">💡 Implement flexible hours, no-meeting days, mental health days.</div>
                """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

    elif feature == "Employee Recognition":
        recog_df = _rate_df(df, "Employee Recognition").sort_values("Left_Rate", ascending=False)
        col_l, col_r = st.columns([1.3, 1])
        with col_l:
            with st.container():
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Attrition by Recognition Level</div>', unsafe_allow_html=True)
                fig2 = px.bar(recog_df, x="Employee Recognition", y="Left_Rate",
                    text=recog_df["Left_Rate"].map(lambda v: f"{v:.1f}%"),
                    color="Left_Rate", color_continuous_scale=["#22C55E","#F59E0B","#EF4444"])
                fig2.update_traces(textposition="outside")
                fig2.update_layout(height=300, yaxis_title="Left Rate (%)", coloraxis_showscale=False)
                st.plotly_chart(fig2, width='stretch', key="p5_recog_bar")

                st.markdown('<div class="section-title">Bubble: Recognition vs Promotions</div>', unsafe_allow_html=True)
                rec_sum = df.groupby("Employee Recognition").agg(
                    Total=("Attrition","count"),
                    Left=("Attrition", lambda x: (x=="Left").sum()),
                    Avg_Promos=("Number of Promotions","mean")
                ).reset_index()
                rec_sum["Left_Rate"] = rec_sum["Left"]/rec_sum["Total"]*100
                fig_rb = px.scatter(rec_sum, x="Employee Recognition", y="Avg_Promos", size="Total",
                    color="Left_Rate", size_max=60, color_continuous_scale=["#22C55E","#F59E0B","#EF4444"])
                fig_rb.update_layout(height=280, yaxis_title="Avg Promotions")
                st.plotly_chart(fig_rb, width='stretch', key="p5_recog_bubble")
                st.markdown('</div>', unsafe_allow_html=True)
        with col_r:
            with st.container():
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Key Insight</div>', unsafe_allow_html=True)
                st.markdown("""
                <div class="insight-box">🏅 Low recognition = higher attrition — feeling unseen drives exits.</div>
                <div class="rec-box">💡 Build monthly shout-outs and manager appreciation rituals.</div>
                """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

    elif feature == "Performance Rating":
        perf_df = _rate_df(df, "Performance Rating").sort_values("Performance Rating")
        col_l, col_r = st.columns([1.3, 1])
        with col_l:
            with st.container():
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Attrition by Performance Rating</div>', unsafe_allow_html=True)
                fig3 = px.line(perf_df, x="Performance Rating", y="Left_Rate", markers=True,
                    text=perf_df["Left_Rate"].map(lambda v: f"{v:.1f}%"))
                fig3.update_traces(line_color="#2563EB", marker=dict(size=10), textposition="top center")
                fig3.update_layout(height=300, yaxis_title="Left Rate (%)")
                st.plotly_chart(fig3, width='stretch', key="p5_perf_line")

                st.markdown('<div class="section-title">Bubble: Performance vs Income</div>', unsafe_allow_html=True)
                perf_sum = df.groupby("Performance Rating").agg(
                    Total=("Attrition","count"),
                    Left=("Attrition", lambda x: (x=="Left").sum()),
                    Avg_Income=("Monthly Income","mean")
                ).reset_index()
                perf_sum["Left_Rate"] = perf_sum["Left"]/perf_sum["Total"]*100
                fig_pb = px.scatter(perf_sum, x="Performance Rating", y="Avg_Income", size="Total",
                    color="Left_Rate", size_max=60, color_continuous_scale=["#22C55E","#F59E0B","#EF4444"])
                fig_pb.update_layout(height=280, yaxis_title="Avg Income")
                st.plotly_chart(fig_pb, width='stretch', key="p5_perf_bubble")
                st.markdown('</div>', unsafe_allow_html=True)
        with col_r:
            with st.container():
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Key Insight</div>', unsafe_allow_html=True)
                st.markdown("""
                <div class="insight-box">📊 Performance shows moderate effect — low performers leave more.</div>
                <div class="insight-box">⚠ High performers also leave if not recognized.</div>
                <div class="rec-box">💡 Track top-performer flight risk separately.</div>
                """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

    else:
        size_df = _rate_df(df, "Company Size")
        with st.container():
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Attrition by Company Size</div>', unsafe_allow_html=True)
            c_l, c_r = st.columns([1.3, 1])
            with c_l:
                fig4 = px.bar(size_df, x="Company Size", y="Left_Rate",
                    text=size_df["Left_Rate"].map(lambda v: f"{v:.1f}%"),
                    color="Left_Rate", color_continuous_scale=["#22C55E","#F59E0B","#EF4444"])
                fig4.update_traces(textposition="outside")
                fig4.update_layout(height=270, yaxis_title="Left Rate (%)", coloraxis_showscale=False)
                st.plotly_chart(fig4, width='stretch', key="p5_size_bar")
            with c_r:
                st.markdown("""
                <div class="insight-box" style="margin-top:1rem">🏢 Size shows minimal variation (~47-50% across all).</div>
                <div class="rec-box">💡 Culture > size for retention.</div>
                """, unsafe_allow_html=True)

            st.markdown('<div class="section-title">Bubble: Company Size Profile</div>', unsafe_allow_html=True)
            size_sum = df.groupby("Company Size").agg(
                Total=("Attrition","count"),
                Left=("Attrition", lambda x: (x=="Left").sum()),
                Avg_Distance=("Distance from Home","mean")
            ).reset_index()
            size_sum["Left_Rate"] = size_sum["Left"]/size_sum["Total"]*100
            fig_sb = px.scatter(size_sum, x="Company Size", y="Avg_Distance", size="Total",
                color="Left_Rate", size_max=60, color_continuous_scale=["#22C55E","#F59E0B","#EF4444"])
            fig_sb.update_layout(height=280, yaxis_title="Avg Distance from Home")
            st.plotly_chart(fig_sb, width='stretch', key="p5_size_bubble")
            st.markdown('</div>', unsafe_allow_html=True)
