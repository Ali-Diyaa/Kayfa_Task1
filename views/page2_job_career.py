"""
PAGE 2 – Attrition by Job Level & Career Progression
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
        <h1>📈 Attrition by Job Level & Career Progression</h1>
        <p>How job level, promotions, income, and tenure shape an employee's decision to stay or leave.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Job Level KPI strip ──────────────────────────────────────────────────
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

    # ── SELECT BOX ───────────────────────────────────────────
    feature = st.selectbox(
        "🔍 Choose Analysis Feature",
        ["Job Level", "Promotions", "Monthly Income", "Tenure"],
        index=0,
        key="p2_selector_v3"
    )

    # ── Job Level ────────────────────────────────────────────────────────────
    if feature == "Job Level":
        col_l, col_r = st.columns([1.2, 1])

        with col_l:
            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>Attrition Rate by Job Level</div>", unsafe_allow_html=True)

            colors_jl = {"Entry":"#EF4444","Mid":"#F59E0B","Senior":"#22C55E"}
            order = ["Entry","Mid","Senior"]
            rates = {row["Job Level"]: row["Left_Rate"] for _, row in jl_df.iterrows()}
            fig = go.Figure(go.Bar(
                x=order, y=[rates.get(j,0) for j in order],
                marker_color=[colors_jl[j] for j in order],
                text=[f"{rates.get(j,0):.1f}%" for j in order],
                textposition="outside", width=0.45
            ))
            fig.update_layout(yaxis=dict(range=[0,80], title="Left Rate (%)"),
                xaxis_title="Job Level", margin=dict(t=20,b=20,l=20,r=20), height=300,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(family="DM Sans"))
            st.plotly_chart(fig, width='stretch', key="p2_job_bar")

            # Bubble
            st.markdown("<div class='section-title' style='margin-top:10px'>Bubble: Headcount vs Avg Income</div>", unsafe_allow_html=True)
            jl_summary = df.groupby("Job Level").agg(
                Total=("Attrition","count"),
                Left=("Attrition", lambda x: (x=="Left").sum()),
                Avg_Income=("Monthly Income","mean")
            ).reset_index()
            jl_summary["Left_Rate"] = jl_summary["Left"]/jl_summary["Total"]*100

            fig_bub = px.scatter(jl_summary, x="Job Level", y="Avg_Income",
                size="Total", color="Left_Rate", hover_name="Job Level",
                size_max=70, color_continuous_scale=["#22C55E","#F59E0B","#EF4444"])
            fig_bub.update_layout(height=300, margin=dict(t=10,b=10,l=10,r=10),
                yaxis_title="Avg Monthly Income ($)", coloraxis_showscale=False,
                paper_bgcolor="rgba(0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_bub, width='stretch', key="p2_job_bubble")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_r:
            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>Key Insight</div>", unsafe_allow_html=True)
            st.markdown("""
            <div class="insight-box">🔴 <strong>Entry-level employees are the most at-risk</strong> — nearly <strong>2 out of 3</strong> leave.</div>
            <div class="insight-box">🟡 Mid-level attrition at <strong>45%</strong> — still a significant challenge.</div>
            <div class="insight-box">🟢 Senior employees are stable — only <strong>1 in 5</strong> leaves.</div>
            <div class="rec-box">💡 <strong>Recommendation:</strong> Invest in onboarding, mentorship, and fast-track paths for entry-level.</div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # ── Promotions ───────────────────────────────────────────────────────────
    elif feature == "Promotions":
        promo_df = _rate_df(df, "Number of Promotions")
        col_l, col_r = st.columns([1.3, 1])
        with col_l:
            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>Attrition Rate by Number of Promotions</div>", unsafe_allow_html=True)
            fig2 = px.bar(promo_df.sort_values("Number of Promotions"),
                x="Number of Promotions", y="Left_Rate",
                text=promo_df.sort_values("Number of Promotions")["Left_Rate"].map(lambda v: f"{v:.1f}%"),
                color="Left_Rate", color_continuous_scale=["#22C55E","#F59E0B","#EF4444"])
            fig2.update_traces(textposition="outside")
            fig2.update_layout(yaxis_title="Left Rate (%)", xaxis_title="Number of Promotions",
                coloraxis_showscale=False, margin=dict(t=20,b=20,l=20,r=20), height=300,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(family="DM Sans"))
            st.plotly_chart(fig2, width='stretch', key="p2_promo_bar")

            # Bubble
            st.markdown("<div class='section-title' style='margin-top:10px'>Bubble: Promotions vs Tenure</div>", unsafe_allow_html=True)
            promo_sum = df.groupby("Number of Promotions").agg(
                Total=("Attrition","count"),
                Left=("Attrition", lambda x: (x=="Left").sum()),
                Avg_Tenure=("Years at Company","mean")
            ).reset_index()
            promo_sum["Left_Rate"] = promo_sum["Left"]/promo_sum["Total"]*100
            fig_bub2 = px.scatter(promo_sum, x="Number of Promotions", y="Avg_Tenure",
                size="Total", color="Left_Rate", size_max=70,
                color_continuous_scale=["#22C55E","#F59E0B","#EF4444"])
            fig_bub2.update_layout(height=300, margin=dict(t=10,b=10,l=10,r=10),
                yaxis_title="Avg Years at Company", coloraxis_showscale=False,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_bub2, width='stretch', key="p2_promo_bubble")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_r:
            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>Key Insight</div>", unsafe_allow_html=True)
            st.markdown("""
            <div class="insight-box">📉 <strong>0 promotions</strong> = highest attrition — stagnation breeds turnover.</div>
            <div class="insight-box">📈 Each promotion drops attrition meaningfully.</div>
            <div class="rec-box">💡 <strong>Recommendation:</strong> Transparent, merit-based promotion framework.</div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # ── Monthly Income ───────────────────────────────────────────────────────
    elif feature == "Monthly Income":
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Monthly Income Distribution: Stayed vs Left</div>", unsafe_allow_html=True)
        fig3 = px.histogram(df, x="Monthly Income", color="Attrition", nbins=30,
            barmode="overlay", opacity=0.72,
            color_discrete_map={"Stayed":"#2563EB","Left":"#EF4444"})
        fig3.update_layout(xaxis_title="Monthly Income ($)", yaxis_title="Number of Employees",
            legend_title_text="", margin=dict(t=10,b=10,l=10,r=10), height=300,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(family="DM Sans"))
        st.plotly_chart(fig3, width='stretch', key="p2_income_hist")

        # Bubble
        st.markdown("<div class='section-title' style='margin-top:10px'>Bubble: Income Bins vs Attrition Rate</div>", unsafe_allow_html=True)
        df["Income_Bin"] = pd.cut(df["Monthly Income"], bins=12)
        inc_sum = df.groupby("Income_Bin", observed=False).agg(
            Total=("Attrition","count"),
            Left=("Attrition", lambda x: (x=="Left").sum()),
            Avg_Income=("Monthly Income","mean")
        ).reset_index()
        inc_sum["Left_Rate"] = inc_sum["Left"]/inc_sum["Total"]*100
        fig_bub3 = px.scatter(inc_sum, x="Avg_Income", y="Left_Rate",
            size="Total", color="Left_Rate", size_max=60,
            color_continuous_scale=["#22C55E","#F59E0B","#EF4444"])
        fig_bub3.update_layout(height=300, xaxis_title="Avg Income in Bin ($)",
            yaxis_title="Left Rate (%)", coloraxis_showscale=False,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_bub3, width='stretch', key="p2_income_bubble")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="insight-box">💰 Lower-income shows higher leave tendency, but effect is <strong>moderate</strong> — not decisive.</div>
        <div class="rec-box">💡 <strong>Recommendation:</strong> Benchmark entry-level salaries and close gaps.</div>
        """, unsafe_allow_html=True)

    # ── Tenure ───────────────────────────────────────────────────────────────
    else:
        col_l, col_r = st.columns([1.3, 1])
        with col_l:
            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>Tenure Distribution: Stayed vs Left</div>", unsafe_allow_html=True)
            fig4 = px.histogram(df, x="Years at Company", color="Attrition", nbins=20,
                barmode="overlay", opacity=0.72,
                color_discrete_map={"Stayed":"#2563EB","Left":"#EF4444"})
            fig4.update_layout(xaxis_title="Years at Company", yaxis_title="Count",
                legend_title_text="", margin=dict(t=10,b=10,l=10,r=10), height=300,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(family="DM Sans"))
            st.plotly_chart(fig4, width='stretch', key="p2_tenure_hist")

            # Bubble
            st.markdown("<div class='section-title' style='margin-top:10px'>Bubble: Tenure Risk Profile</div>", unsafe_allow_html=True)
            ten_sum = df.groupby("Years at Company").agg(
                Total=("Attrition","count"),
                Left=("Attrition", lambda x: (x=="Left").sum()),
                Avg_Income=("Monthly Income","mean")
            ).reset_index()
            ten_sum["Left_Rate"] = ten_sum["Left"]/ten_sum["Total"]*100
            fig_bub4 = px.scatter(ten_sum, x="Years at Company", y="Avg_Income",
                size="Total", color="Left_Rate", size_max=50,
                color_continuous_scale=["#22C55E","#F59E0B","#EF4444"],
                hover_data={"Left_Rate":":.1f"})
            fig_bub4.update_layout(height=300, yaxis_title="Avg Income ($)",
                coloraxis_showscale=False, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_bub4, width='stretch', key="p2_tenure_bubble")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_r:
            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>Key Insight</div>", unsafe_allow_html=True)
            st.markdown("""
            <div class="insight-box">⏱ Attrition concentrated in <strong>first 5 years</strong>.</div>
            <div class="insight-box">🔒 Past 5 years = much higher retention.</div>
            <div class="rec-box">💡 <strong>Recommendation:</strong> 90-day, 1-year, 3-year check-ins.</div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

