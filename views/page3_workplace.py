"""
PAGE 3 – Workplace & Flexibility
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
        st.markdown("## Workplace & Flexibility")
    
    with logo_col:
        if logo_path.exists():
            st.image(str(logo_path), width=200)

    st.markdown("""
    <div class="page-header">
        <h1>🏡 Workplace & Flexibility</h1>
        <p>How remote work, overtime, company reputation, distance, and innovation culture drive attrition.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Filters ─────────────────────────────────────
    with st.expander("🎛 Interactive Filters", expanded=False):
        f1, f2, f3 = st.columns(3)
        with f1: job_sel = st.multiselect("Job Level", sorted(df["Job Level"].unique()), default=sorted(df["Job Level"].unique()), key="p3_job_filter")
        with f2: remote_sel = st.multiselect("Remote Work", df["Remote Work"].unique(), default=list(df["Remote Work"].unique()), key="p3_remote_filter")
        with f3: ot_sel = st.multiselect("Overtime", df["Overtime"].unique(), default=list(df["Overtime"].unique()), key="p3_ot_filter")

    df_f = df[df["Job Level"].isin(job_sel) & df["Remote Work"].isin(remote_sel) & df["Overtime"].isin(ot_sel)].copy()

    # ── KPI strip ───────────────────────────────────
    rw = _rate_df(df_f, "Remote Work")
    ot = _rate_df(df_f, "Overtime")
    r_yes = rw[rw["Remote Work"]=="Yes"]["Left_Rate"].values[0] if "Yes" in rw["Remote Work"].values else 0
    r_no = rw[rw["Remote Work"]=="No"]["Left_Rate"].values[0] if "No" in rw["Remote Work"].values else 0
    o_yes = ot[ot["Overtime"]=="Yes"]["Left_Rate"].values[0] if "Yes" in ot["Overtime"].values else 0
    o_no = ot[ot["Overtime"]=="No"]["Left_Rate"].values[0] if "No" in ot["Overtime"].values else 0

    c1, c2, c3, c4 = st.columns(4)
    for col, label, val, color, tag in [
        (c1, "Remote – Left", f"{r_yes:.1f}%", "#22C55E", "Remote"),
        (c2, "On-site – Left", f"{r_no:.1f}%", "#EF4444", "On-site"),
        (c3, "Overtime – Left", f"{o_yes:.1f}%", "#EF4444", "With OT"),
        (c4, "No OT – Left", f"{o_no:.1f}%", "#22C55E", "No OT"),
    ]:
        with col:
            st.markdown(f"""<div class="kpi-card" style="border-top:4px solid {color}">
                <div class="kpi-label">{label}</div><div class="kpi-value" style="color:{color}">{val}</div><div class="kpi-delta">{tag}</div></div>""", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    feature = st.selectbox("Choose Workplace Factor",
        ["Remote Work (Q3)", "Overtime (Q2)", "Company Reputation", "Distance from Home", "Innovation & Leadership"],
        key="page3_feature_select")

    # ── Q3 REMOTE WORK ──────────────────────────────
    if "Remote" in feature:
        col_l, col_r = st.columns([1.2,1])
        with col_l:
            st.markdown("<div class='section-card'><div class='section-title'>Q3: Attrition Rate – Remote vs On-site</div>", unsafe_allow_html=True)
            fig = go.Figure(go.Bar(x=["Remote (Yes)","On-site (No)"], y=[r_yes,r_no],
                marker_color=["#22C55E","#EF4444"], text=[f"{r_yes:.1f}%",f"{r_no:.1f}%"], textposition="outside", width=0.4))
            fig.update_layout(yaxis_title="Left Rate (%)", height=280, margin=dict(t=20,b=20,l=20,r=20))
            st.plotly_chart(fig, use_container_width=True, key="p3_remote_bar")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_r:
            st.markdown("<div class='section-card'><div class='section-title'>Q3 Insight</div>", unsafe_allow_html=True)
            diff = r_no - r_yes
            # exact numbers from your notebook
            st.markdown(f"""
            <div class="insight-box"><strong>Q3 Answer:</strong> Remote workers leave at <strong>24.7%</strong> vs <strong>52.8%</strong> for on-site — a <strong>28.1 percentage point</strong> reduction. Remote covers 19% of staff (14,198 employees).</div>
            <div class="rec-box"><strong>Recommendation:</strong> Expand hybrid policies, prioritize for >30km commuters.</div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # ── Q2 OVERTIME ─────────────────────────────────
    elif "Overtime" in feature:
        col_l, col_r = st.columns([1.2,1])
        with col_l:
            st.markdown("<div class='section-card'><div class='section-title'>Q2: Attrition Rate – Overtime vs No Overtime</div>", unsafe_allow_html=True)
            fig2 = go.Figure(go.Bar(x=["Overtime Yes","Overtime No"], y=[o_yes,o_no],
                marker_color=["#EF4444","#22C55E"], text=[f"{o_yes:.1f}%",f"{o_no:.1f}%"], textposition="outside", width=0.4))
            fig2.update_layout(yaxis_title="Left Rate (%)", height=280, margin=dict(t=20,b=20,l=20,r=20))
            st.plotly_chart(fig2, use_container_width=True, key="p3_ot_bar")
            st.markdown("</div>", unsafe_allow_html=True)
        with col_r:
            st.markdown("<div class='section-card'><div class='section-title'>Q2 Insight</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="insight-box"><strong>Q2 Answer:</strong> Overtime employees leave at <strong>51.5%</strong> vs <strong>45.5%</strong> without overtime — <strong>+6.0pp</strong> higher risk (12,534 of 24,341 left).</div>
            <div class="rec-box"><strong>Recommendation:</strong> Monitor OT weekly, cap at 10hrs, rebalance workload.</div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # ── OTHER FEATURES (keep yours) ─────────────────
    elif feature == "Company Reputation":
        rep_df = _rate_df(df_f, "Company Reputation").sort_values("Left_Rate")
        st.markdown("<div class='section-card'><div class='section-title'>Attrition by Company Reputation</div>", unsafe_allow_html=True)
        fig3 = px.bar(rep_df, x="Left_Rate", y="Company Reputation", orientation="h",
            text=rep_df["Left_Rate"].map(lambda v: f"{v:.1f}%"), color="Left_Rate",
            color_continuous_scale=["#22C55E","#F59E0B","#EF4444"])
        fig3.update_layout(height=300, xaxis_title="Left Rate (%)", coloraxis_showscale=False)
        st.plotly_chart(fig3, use_container_width=True, key="p3_rep_bar")
        st.markdown("</div>", unsafe_allow_html=True)

    elif feature == "Distance from Home":
        df_f["Distance Category"] = pd.cut(df_f["Distance from Home"], bins=[0,10,30,50,100], labels=["1-10 km","10-30 km","30-50 km","50-100 km"])
        dist_df = _rate_df(df_f, "Distance Category")
        st.markdown("<div class='section-card'><div class='section-title'>Attrition by Distance</div>", unsafe_allow_html=True)
        fig4 = px.line(dist_df, x="Distance Category", y="Left_Rate", markers=True, text=dist_df["Left_Rate"].map(lambda v: f"{v:.1f}%"))
        fig4.update_traces(line_color="#2563EB", textposition="top center")
        fig4.update_layout(height=300, yaxis_title="Left Rate (%)")
        st.plotly_chart(fig4, use_container_width=True, key="p3_dist_line")
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        inn_df = _rate_df(df_f, "Innovation Opportunities")
        lead_df = _rate_df(df_f, "Leadership Opportunities")
        col1,col2 = st.columns(2)
        with col1:
            fig5 = px.bar(inn_df, x="Innovation Opportunities", y="Left_Rate", text=inn_df["Left_Rate"].map(lambda v: f"{v:.1f}%"),
                color="Left_Rate", color_continuous_scale=["#22C55E","#EF4444"])
            fig5.update_layout(height=280, showlegend=False)
            st.plotly_chart(fig5, use_container_width=True, key="p3_innov_bar")
        with col2:
            fig6 = px.bar(lead_df, x="Leadership Opportunities", y="Left_Rate", text=lead_df["Left_Rate"].map(lambda v: f"{v:.1f}%"),
                color="Left_Rate", color_continuous_scale=["#22C55E","#EF4444"])
            fig6.update_layout(height=280, showlegend=False)
            st.plotly_chart(fig6, use_container_width=True, key="p3_lead_bar")