"""
PAGE 4 – Demographics
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
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="page-header">
        <h1>🧑🤝🧑 Demographics & Employee Profile</h1>
        <p>Exploring how age, gender, marital status, and education level correlate with attrition.</p>
    </div>
    """, unsafe_allow_html=True)

    mar_df = _rate_df(df, "Marital Status")
    s_r = mar_df[mar_df["Marital Status"]=="Single"]["Left_Rate"].values[0] if "Single" in mar_df["Marital Status"].values else 0
    m_r = mar_df[mar_df["Marital Status"]=="Married"]["Left_Rate"].values[0] if "Married" in mar_df["Marital Status"].values else 0
    a_u30 = (df[df["Age"] < 30]["Attrition"]=="Left").mean()*100
    a_30p = (df[df["Age"] >= 30]["Attrition"]=="Left").mean()*100

    c1, c2, c3, c4 = st.columns(4)
    for col, label, val, color in [
        (c1, "Single – Attrition", f"{s_r:.1f}%", "#EF4444"),
        (c2, "Married – Attrition", f"{m_r:.1f}%", "#22C55E"),
        (c3, "Under-30 Attrition", f"{a_u30:.1f}%", "#F59E0B"),
        (c4, "30+ Attrition", f"{a_30p:.1f}%", "#2563EB"),
    ]:
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="border-top:4px solid {color}">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value" style="color:{color}">{val}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    feature = st.selectbox(
        "🔍 Choose Demographic Dimension",
        ["Marital Status", "Age", "Education Level", "Gender"],
        index=0,
        key="page4_demo_select"
    )

    if feature == "Marital Status":
        col_l, col_r = st.columns([1.2, 1])
        with col_l:
            with st.container():
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Attrition Rate by Marital Status</div>', unsafe_allow_html=True)
                order_m = mar_df.sort_values("Left_Rate", ascending=False)
                fig = go.Figure(go.Bar(
                    x=order_m["Marital Status"], y=order_m["Left_Rate"],
                    marker_color=["#EF4444","#F59E0B","#22C55E"][:len(order_m)],
                    text=[f"{v:.1f}%" for v in order_m["Left_Rate"]],
                    textposition="outside", width=0.4
                ))
                fig.update_layout(yaxis_title="Left Rate (%)", height=300,
                    margin=dict(t=20,b=20,l=20,r=20), paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig, width='stretch', key="p4_marital_bar")

                st.markdown('<div class="section-title">Bubble: Marital Status Profile</div>', unsafe_allow_html=True)
                mar_sum = df.groupby("Marital Status").agg(
                    Total=("Attrition","count"),
                    Left=("Attrition", lambda x: (x=="Left").sum()),
                    Avg_Income=("Monthly Income","mean"),
                    Avg_Age=("Age","mean")
                ).reset_index()
                mar_sum["Left_Rate"] = mar_sum["Left"]/mar_sum["Total"]*100
                fig_b = px.scatter(mar_sum, x="Avg_Age", y="Avg_Income", size="Total",
                    color="Left_Rate", hover_name="Marital Status", size_max=60,
                    color_continuous_scale=["#22C55E","#F59E0B","#EF4444"])
                fig_b.update_layout(height=300, xaxis_title="Avg Age", yaxis_title="Avg Income")
                st.plotly_chart(fig_b, width='stretch', key="p4_marital_bubble")
                st.markdown('</div>', unsafe_allow_html=True)

        with col_r:
            with st.container():
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Key Insight</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="insight-box"> <strong>Single ({s_r:.0f}%)</strong> leave at nearly double the rate of married ({m_r:.0f}%).</div>
                <div class="insight-box"> Family stability creates stronger commitment.</div>
                <div class="rec-box"> Target young singles with mentorship & social programs.</div>
                """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

    elif feature == "Age":
        col_l, col_r = st.columns([1.3, 1])
        with col_l:
            with st.container():
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Age Distribution by Attrition</div>', unsafe_allow_html=True)
                fig2 = px.histogram(df, x="Age", color="Attrition", nbins=20, barmode="overlay", opacity=0.7,
                    color_discrete_map={"Stayed":"#2563EB","Left":"#EF4444"})
                fig2.update_layout(height=320, margin=dict(t=10,b=10,l=10,r=10), paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig2, width='stretch', key="p4_age_hist")
                st.markdown('</div>', unsafe_allow_html=True)
        with col_r:
            with st.container():
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Attrition by Age Band</div>', unsafe_allow_html=True)
                df_ab = df.copy()
                df_ab["Age Band"] = pd.cut(df_ab["Age"], bins=[17,24,29,39,49,60], labels=["18-24","25-29","30-39","40-49","50+"])
                ab_df = pd.crosstab(df_ab["Age Band"], df_ab["Attrition"])
                ab_df["Left_Rate"] = ab_df["Left"] / ab_df.sum(axis=1) * 100
                ab_df = ab_df.reset_index()
                fig3 = px.bar(ab_df, x="Age Band", y="Left_Rate", text=ab_df["Left_Rate"].map(lambda v: f"{v:.1f}%"),
                    color="Left_Rate", color_continuous_scale=["#22C55E","#F59E0B","#EF4444"])
                fig3.update_traces(textposition="outside")
                fig3.update_layout(height=320, yaxis_title="Left Rate (%)", coloraxis_showscale=False)
                st.plotly_chart(fig3, width='stretch', key="p4_age_band")
                st.markdown('</div>', unsafe_allow_html=True)

        with st.container():
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Bubble: Age Band Risk Profile</div>', unsafe_allow_html=True)
            age_sum = df_ab.groupby("Age Band", observed=False).agg(
                Total=("Attrition","count"),
                Left=("Attrition", lambda x: (x=="Left").sum()),
                Avg_Tenure=("Years at Company","mean")
            ).reset_index()
            age_sum["Left_Rate"] = age_sum["Left"]/age_sum["Total"]*100
            fig_age_b = px.scatter(age_sum, x="Age Band", y="Avg_Tenure", size="Total", color="Left_Rate",
                size_max=60, color_continuous_scale=["#22C55E","#F59E0B","#EF4444"])
            fig_age_b.update_layout(height=300, yaxis_title="Avg Tenure (yrs)")
            st.plotly_chart(fig_age_b, width='stretch', key="p4_age_bubble")
            st.markdown('</div>', unsafe_allow_html=True)

    elif feature == "Education Level":
        edu_df = _rate_df(df, "Education Level").sort_values("Left_Rate", ascending=False)
        with st.container():
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Attrition Rate by Education Level</div>', unsafe_allow_html=True)
            fig4 = px.bar(edu_df, x="Education Level", y="Left_Rate",
                text=edu_df["Left_Rate"].map(lambda v: f"{v:.1f}%"),
                color="Left_Rate", color_continuous_scale=["#22C55E","#F59E0B","#EF4444"])
            fig4.update_traces(textposition="outside")
            fig4.update_layout(height=300, yaxis_title="Left Rate (%)", coloraxis_showscale=False)
            st.plotly_chart(fig4, width='stretch', key="p4_edu_bar")

            st.markdown('<div class="section-title">Bubble: Education vs Income</div>', unsafe_allow_html=True)
            edu_sum = df.groupby("Education Level").agg(
                Total=("Attrition","count"),
                Left=("Attrition", lambda x: (x=="Left").sum()),
                Avg_Income=("Monthly Income","mean")
            ).reset_index()
            edu_sum["Left_Rate"] = edu_sum["Left"]/edu_sum["Total"]*100
            fig_edu_b = px.scatter(edu_sum, x="Education Level", y="Avg_Income", size="Total",
                color="Left_Rate", size_max=60, color_continuous_scale=["#22C55E","#F59E0B","#EF4444"])
            fig_edu_b.update_layout(height=300, yaxis_title="Avg Monthly Income")
            st.plotly_chart(fig_edu_b, width='stretch', key="p4_edu_bubble")
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        gen_df = _rate_df(df, "Gender")
        col_l, col_r = st.columns([1, 1.4])
        with col_l:
            with st.container():
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Attrition by Gender</div>', unsafe_allow_html=True)
                fig5 = go.Figure(go.Bar(
                    x=gen_df["Gender"], y=gen_df["Left_Rate"],
                    marker_color=["#2563EB","#F59E0B"][:len(gen_df)],
                    text=[f"{v:.1f}%" for v in gen_df["Left_Rate"]],
                    textposition="outside", width=0.35
                ))
                fig5.update_layout(height=280, yaxis_title="Left Rate (%)")
                st.plotly_chart(fig5, width='stretch', key="p4_gender_bar")
                st.markdown('</div>', unsafe_allow_html=True)
        with col_r:
            with st.container():
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Bubble: Gender Profile</div>', unsafe_allow_html=True)
                gen_sum = df.groupby("Gender").agg(
                    Total=("Attrition","count"),
                    Left=("Attrition", lambda x: (x=="Left").sum()),
                    Avg_Overtime=("Overtime", lambda x: (x=="Yes").mean()*100),
                    Avg_Distance=("Distance from Home","mean")
                ).reset_index()
                gen_sum["Left_Rate"] = gen_sum["Left"]/gen_sum["Total"]*100
                fig_g = px.scatter(gen_sum, x="Avg_Distance", y="Avg_Overtime", size="Total",
                    color="Left_Rate", hover_name="Gender", size_max=70,
                    color_continuous_scale=["#22C55E","#F59E0B","#EF4444"])
                fig_g.update_layout(height=280, xaxis_title="Avg Distance (km)", yaxis_title="% with Overtime")
                st.plotly_chart(fig_g, width='stretch', key="p4_gender_bubble")
                st.markdown('</div>', unsafe_allow_html=True)

