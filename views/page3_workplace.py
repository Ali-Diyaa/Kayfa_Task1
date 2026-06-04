"""
PAGE 3 – Workplace & Flexibility
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
    <div class="page-header">
        <h1> Workplace & Flexibility</h1>
        <p>How remote work, overtime, company reputation, distance, and innovation culture drive attrition.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── GLOBAL FILTERS ───────────────────────────────────────────────────
    with st.expander("🎛 Interactive Filters", expanded=False):
        f1, f2, f3 = st.columns(3)
        with f1:
            job_sel = st.multiselect("Job Level", sorted(df["Job Level"].unique()),
                                     default=sorted(df["Job Level"].unique()),
                                     key="p3_job_filter")
        with f2:
            remote_sel = st.multiselect("Remote Work", df["Remote Work"].unique(),
                                        default=list(df["Remote Work"].unique()),
                                        key="p3_remote_filter")
        with f3:
            ot_sel = st.multiselect("Overtime", df["Overtime"].unique(),
                                    default=list(df["Overtime"].unique()),
                                    key="p3_ot_filter")

    df_f = df[df["Job Level"].isin(job_sel) &
              df["Remote Work"].isin(remote_sel) &
              df["Overtime"].isin(ot_sel)].copy()

    # ── KPI strip ────────────────────────────────────────────────────────
    rw = _rate_df(df_f, "Remote Work")
    ot = _rate_df(df_f, "Overtime")

    r_yes = rw[rw["Remote Work"]=="Yes"]["Left_Rate"].values[0] if "Yes" in rw["Remote Work"].values else 0
    r_no = rw[rw["Remote Work"]=="No"]["Left_Rate"].values[0] if "No" in rw["Remote Work"].values else 0
    o_yes = ot[ot["Overtime"]=="Yes"]["Left_Rate"].values[0] if "Yes" in ot["Overtime"].values else 0
    o_no = ot[ot["Overtime"]=="No"]["Left_Rate"].values[0] if "No" in ot["Overtime"].values else 0

    c1, c2, c3, c4 = st.columns(4)
    for col, label, val, color, tag in [
        (c1, "Remote – Left", f"{r_yes:.1f}%", "#22C55E", " Remote"),
        (c2, "On-site – Left", f"{r_no:.1f}%", "#EF4444", " On-site"),
        (c3, "Overtime – Left", f"{o_yes:.1f}%", "#EF4444", " With OT"),
        (c4, "No OT – Left", f"{o_no:.1f}%", "#22C55E", " No OT"),
    ]:
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="border-top:4px solid {color}">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value" style="color:{color}">{val}</div>
                <div class="kpi-delta">{tag}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── SELECTBOX ────────────────────────────────────────────────────────
    feature = st.selectbox(" Choose Workplace Factor",
        ["Remote Work", "Overtime", "Company Reputation", "Distance from Home", "Innovation & Leadership"],
        key="page3_feature_select")

    # ── REMOTE WORK ────────────────────────────────────────────────────
    if feature == "Remote Work":
        col_l, col_r = st.columns([1.2,1])
        with col_l:
            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>Attrition Rate: Remote vs On-site</div>", unsafe_allow_html=True)
            fig = go.Figure(go.Bar(x=["Remote (Yes)","On-site (No)"], y=[r_yes,r_no],
                marker_color=["#22C55E","#EF4444"], text=[f"{r_yes:.1f}%",f"{r_no:.1f}%"],
                textposition="outside", width=0.4))
            fig.update_layout(yaxis_title="Left Rate (%)", height=280, margin=dict(t=20,b=20,l=20,r=20),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, width='stretch', key="p3_remote_bar")

            st.markdown("<div class='section-title'>Attrition Split (Filtered)</div>", unsafe_allow_html=True)
            pie = px.pie(df_f, names="Attrition", hole=0.5,
                color="Attrition", color_discrete_map={"Stayed":"#22C55E","Left":"#EF4444"})
            pie.update_layout(height=250, margin=dict(t=10,b=10,l=10,r=10), paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(pie, width='stretch', key="p3_remote_pie")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_r:
            st.markdown("<div class='section-card'><div class='section-title'>Key Insight</div>", unsafe_allow_html=True)
            diff = abs(r_no - r_yes)
            st.markdown(f"""<div class="insight-box"> Remote workers have <strong>{diff:.1f} pp lower</strong> attrition — strongest workplace factor.</div>
            <div class="rec-box"> Expand hybrid policies, especially for >30km commuters.</div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-card'><div class='section-title'>Bubble: Remote vs Distance & Income</div>", unsafe_allow_html=True)
        bub = df_f.groupby("Remote Work").agg(
            Total=("Attrition","count"),
            Left=("Attrition", lambda x: (x=="Left").sum()),
            Avg_Dist=("Distance from Home","mean"),
            Avg_Inc=("Monthly Income","mean")).reset_index()
        bub["Left_Rate"] = bub["Left"]/bub["Total"]*100
        fig_b = px.scatter(bub, x="Avg_Dist", y="Avg_Inc", size="Total", color="Left_Rate",
            hover_name="Remote Work", size_max=80, color_continuous_scale=["#22C55E","#F59E0B","#EF4444"])
        fig_b.update_layout(height=320, xaxis_title="Avg Distance from Home (km)", yaxis_title="Avg Monthly Income ($)",
            coloraxis_showscale=False, paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_b, width='stretch', key="p3_remote_bubble")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── OVERTIME ───────────────────────────────────────────────────────
    elif feature == "Overtime":
        col_l, col_r = st.columns([1.2,1])
        with col_l:
            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>Attrition Rate: Overtime vs No Overtime</div>", unsafe_allow_html=True)
            fig2 = go.Figure(go.Bar(x=["Works Overtime","No Overtime"], y=[o_yes,o_no],
                marker_color=["#EF4444","#22C55E"], text=[f"{o_yes:.1f}%",f"{o_no:.1f}%"],
                textposition="outside", width=0.4))
            fig2.update_layout(yaxis_title="Left Rate (%)", height=280, margin=dict(t=20,b=20,l=20,r=20),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig2, width='stretch', key="p3_ot_bar")

            pie2 = px.pie(df_f, names="Overtime", hole=0.5, color_discrete_sequence=px.colors.qualitative.Set2)
            pie2.update_layout(title="Overtime Distribution (Filtered)", height=250, margin=dict(t=30,b=10))
            st.plotly_chart(pie2, width='stretch', key="p3_ot_pie")
            st.markdown("</div>", unsafe_allow_html=True)
        with col_r:
            st.markdown("<div class='section-card'><div class='section-title'>Key Insight</div>", unsafe_allow_html=True)
            st.markdown("""<div class="insight-box"> Overtime = significantly higher attrition — burnout signal.</div>
            <div class="rec-box"> Monitor OT by team, rebalance workload.</div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        bub2 = df_f.groupby(["Overtime","Job Level"]).agg(
            Total=("Attrition","count"),
            Left=("Attrition", lambda x:(x=="Left").sum())).reset_index()
        bub2["Left_Rate"] = bub2["Left"]/bub2["Total"]*100
        fig_b2 = px.scatter(bub2, x="Job Level", y="Left_Rate", size="Total", color="Overtime",
            size_max=60, color_discrete_map={"Yes":"#EF4444","No":"#22C55E"})
        fig_b2.update_layout(height=320, yaxis_title="Left Rate (%)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_b2, width='stretch', key="p3_ot_bubble")

    # ── COMPANY REPUTATION ─────────────────────────────────────────────
    elif feature == "Company Reputation":
        rep_df = _rate_df(df_f, "Company Reputation").sort_values("Left_Rate")
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Attrition by Company Reputation</div>", unsafe_allow_html=True)
        fig3 = px.bar(rep_df, x="Left_Rate", y="Company Reputation", orientation="h",
            text=rep_df["Left_Rate"].map(lambda v: f"{v:.1f}%"), color="Left_Rate",
            color_continuous_scale=["#22C55E","#F59E0B","#EF4444"])
        fig3.update_layout(height=300, xaxis_title="Left Rate (%)", coloraxis_showscale=False,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig3, width='stretch', key="p3_rep_bar")

        c1,c2 = st.columns(2)
        with c1:
            pie3 = px.pie(df_f, names="Company Reputation", hole=0.4)
            pie3.update_layout(title="Reputation Mix", height=300)
            st.plotly_chart(pie3, width='stretch', key="p3_rep_pie")
        with c2:
            bub3 = df_f.groupby("Company Reputation").agg(
                Total=("Attrition","count"),
                Left=("Attrition", lambda x:(x=="Left").sum()),
                Avg_Inc=("Monthly Income","mean")).reset_index()
            bub3["Left_Rate"]=bub3["Left"]/bub3["Total"]*100
            fig_b3 = px.scatter(bub3, x="Company Reputation", y="Left_Rate", size="Total", color="Avg_Inc",
                size_max=60, color_continuous_scale="Blues")
            fig_b3.update_layout(height=300, yaxis_title="Left Rate (%)")
            st.plotly_chart(fig_b3, width='stretch', key="p3_rep_bubble")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── DISTANCE ───────────────────────────────────────────────────────
    elif feature == "Distance from Home":
        df_f["Distance Category"] = pd.cut(df_f["Distance from Home"],
            bins=[0,10,30,50,100], labels=["1-10 km","10-30 km","30-50 km","50-100 km"])
        dist_df = _rate_df(df_f, "Distance Category")
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Attrition by Distance</div>", unsafe_allow_html=True)
        fig4 = px.line(dist_df, x="Distance Category", y="Left_Rate", markers=True,
            text=dist_df["Left_Rate"].map(lambda v: f"{v:.1f}%"))
        fig4.update_traces(line_color="#2563EB", marker=dict(size=10, color="#EF4444"), textposition="top center")
        fig4.update_layout(height=300, yaxis_title="Left Rate (%)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig4, width='stretch', key="p3_dist_line")

        pie4 = px.pie(df_f, names="Distance Category", hole=0.4)
        bub4 = df_f.groupby("Distance Category", observed=False).agg(
            Total=("Attrition","count"),
            Left=("Attrition", lambda x:(x=="Left").sum())).reset_index()
        bub4["Left_Rate"]=bub4["Left"]/bub4["Total"]*100
        fig_b4 = px.scatter(bub4, x="Distance Category", y="Left_Rate", size="Total", color="Left_Rate",
            size_max=70, color_continuous_scale=["#22C55E","#F59E0B","#EF4444"])
        c1,c2 = st.columns(2)
        with c1: st.plotly_chart(pie4, width='stretch', key="p3_dist_pie")
        with c2: st.plotly_chart(fig_b4, width='stretch', key="p3_dist_bubble")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── INNOVATION & LEADERSHIP ──────────────────────────────────────
    else:
        inn_df = _rate_df(df_f, "Innovation Opportunities")
        lead_df = _rate_df(df_f, "Leadership Opportunities")
        col1,col2 = st.columns(2)
        with col1:
            fig5 = px.bar(inn_df, x="Innovation Opportunities", y="Left_Rate",
                text=inn_df["Left_Rate"].map(lambda v: f"{v:.1f}%"),
                color="Left_Rate", color_continuous_scale=["#22C55E","#EF4444"])
            fig5.update_layout(height=280, showlegend=False, paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig5, width='stretch', key="p3_innov_bar")
        with col2:
            fig6 = px.bar(lead_df, x="Leadership Opportunities", y="Left_Rate",
                text=lead_df["Left_Rate"].map(lambda v: f"{v:.1f}%"),
                color="Left_Rate", color_continuous_scale=["#22C55E","#EF4444"])
            fig6.update_layout(height=280, showlegend=False, paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig6, width='stretch', key="p3_lead_bar")

        combo = df_f.groupby(["Innovation Opportunities","Leadership Opportunities"]).agg(
            Total=("Attrition","count"),
            Left=("Attrition", lambda x:(x=="Left").sum())).reset_index()
        combo["Left_Rate"]=combo["Left"]/combo["Total"]*100
        fig_b5 = px.scatter(combo, x="Innovation Opportunities", y="Leadership Opportunities",
            size="Total", color="Left_Rate", size_max=60,
            color_continuous_scale=["#22C55E","#F59E0B","#EF4444"],
            hover_data={"Left_Rate":":.1f"})
        fig_b5.update_layout(height=350, title="Bubble: Innovation vs Leadership Impact")
        st.plotly_chart(fig_b5, width='stretch', key="p3_innov_lead_bubble")

