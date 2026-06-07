"""
PAGE 1 – Overview
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
        try:
            train = pd.read_csv("train.csv")
            test  = pd.read_csv("test.csv")
            df    = pd.concat([train, test], ignore_index=True)
        except FileNotFoundError:
            st.error("⚠ Please place `employee_attrition_full.csv` (or train/test CSVs) in the app folder.")
            st.stop()
    df["Years at Company"] = df["Years at Company"].apply(lambda x: 41 if x > 41 else x)
    return df

def show():
    df = load_data()
    logo_path = Path(__file__).resolve().parent.parent / "kayfaio_logo.jpg"

    title_col, logo_col = st.columns([6, 2])
    with title_col:
        st.markdown("## Week #1 Task: Employee Attrition Intelligence Dashboard")
    
    with logo_col:
        if logo_path.exists():
            st.image(str(logo_path), width=300)

    # ── CSS ─────────────────────────────────────────
    st.markdown("""
    <style>
   .page-header { margin-bottom: 20px; }
   .page-header h1 { font-size: 1.9rem; margin: 0; }
   .page-header p { color: #FFFFFF; margin-top: 6px; }
   .kpi-card { background: white; padding: 16px 18px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
   .kpi-label { font-size: 0.85rem; color: #475569; margin-bottom: 6px; font-weight: 500; }
   .kpi-value { font-size: 1.9rem; font-weight: 700; line-height: 1.2; }
   .kpi-delta { font-size: 0.8rem; color: #64748B; margin-top: 4px; }
   .section-card { background: white; padding: 18px 20px; border-radius: 14px; box-shadow: 0 2px 10px rgba(0,0,0,0.06); margin-bottom: 16px; }
   .section-title { font-weight: 600; font-size: 1.1rem; margin-bottom: 12px; }
   .divider { height: 1px; background: #e2e8f0; margin: 24px 0; }
   .insight-box { background: #F8FAFC; border-left: 4px solid #2563EB; padding: 14px 18px; border-radius: 8px; margin-top: 16px; }
    </style>
    """, unsafe_allow_html=True)

    total = len(df)
    left_n = (df["Attrition"] == "Left").sum()
    stayed_n = (df["Attrition"] == "Stayed").sum()
    left_pct = left_n / total * 100
    stayed_pct = stayed_n / total * 100
    avg_income = df["Monthly Income"].mean()
    avg_tenure = df["Years at Company"].mean()

    # --- Q1 CALCULATIONS ---
    role_stats = df.groupby("Job Role").agg(
        Total=('Attrition','count'),
        Left=('Attrition', lambda x: (x=='Left').sum())
    ).reset_index()
    role_stats['Rate'] = role_stats['Left'] / role_stats['Total'] * 100
    role_stats = role_stats.sort_values('Rate', ascending=False)
    top_role = role_stats.iloc[0]

    # ── Header ──────────────────────────────────────
    st.markdown("""
    <div class="page-header">
        <h1>📊 Employee Attrition Dashboard</h1>
        <p>A comprehensive analysis of workforce attrition patterns to guide HR retention strategy.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── KPIs ────────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)
    kpis = [
        (c1, "Total Employees", f"{total:,}", "#2563EB", "Full dataset"),
        (c2, "Attrition Rate", f"{left_pct:.1f}%", "#EF4444", f"{left_n:,} left"),
        (c3, "Retention Rate", f"{stayed_pct:.1f}%", "#22C55E", f"{stayed_n:,} stayed"),
        (c4, "Avg Monthly Income", f"${avg_income:,.0f}", "#F59E0B", "All employees"),
        (c5, "Avg Tenure", f"{avg_tenure:.1f} yrs", "#6366F1", "Years at company"),
    ]
    for col, label, val, color, delta in kpis:
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="border-top:4px solid {color}">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value" style="color:{color}">{val}</div>
                <div class="kpi-delta">{delta}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── Charts ──────────────────────────────────────
    col_l, col_r = st.columns([1, 1.6])

    with col_l:
        
        st.markdown('<div class="section-title">Attrition Split</div>', unsafe_allow_html=True)
        fig_pie = go.Figure(go.Pie(
            labels=["Stayed", "Left"],
            values=[stayed_n, left_n],
            hole=0.62,
            marker=dict(colors=["#2563EB", "#EF4444"]),
            textinfo="label+percent"
        ))
        fig_pie.add_annotation(text=f"<b>{left_pct:.1f}%</b><br>Left", x=0.5, y=0.5, showarrow=False, font=dict(size=18))
        fig_pie.update_layout(margin=dict(t=10,b=10,l=10,r=10), height=280, showlegend=True)
        st.plotly_chart(fig_pie, use_container_width=True, key="p1_pie")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        
        st.markdown('<div class="section-title">Q1: Attrition by Job Role</div>', unsafe_allow_html=True)
        # highlight top role in red
        colors = ['#EF4444' if r == top_role['Job Role'] else '#93C5FD' for r in role_stats['Job Role']]
        fig_bar = go.Figure(go.Bar(
            x=role_stats['Rate'],
            y=role_stats['Job Role'],
            orientation="h",
            marker_color=colors,
            text=[f"{v:.1f}%" for v in role_stats['Rate']],
            textposition="outside"
        ))
        fig_bar.update_layout(xaxis_title="Attrition Rate (%)", height=300,
            margin=dict(t=10,b=10,l=10,r=40), yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_bar, use_container_width=True, key="p1_q1")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Age & Tenure ────────────────────────────────
    col_a, col_b = st.columns(2)
    with col_a:
        
        st.markdown('<div class="section-title">Age Distribution</div>', unsafe_allow_html=True)
        fig_age = px.histogram(df, x="Age", color="Attrition", nbins=25, barmode="overlay", opacity=0.7,
            color_discrete_map={"Stayed": "#2563EB", "Left": "#EF4444"})
        fig_age.update_layout(height=240, margin=dict(t=10,b=10,l=10,r=10), showlegend=False)
        st.plotly_chart(fig_age, use_container_width=True, key="p1_age")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        
        st.markdown('<div class="section-title">Tenure Distribution</div>', unsafe_allow_html=True)
        fig_ten = px.histogram(df, x="Years at Company", color="Attrition", nbins=20, barmode="overlay", opacity=0.7,
            color_discrete_map={"Stayed": "#2563EB", "Left": "#EF4444"})
        fig_ten.update_layout(height=240, margin=dict(t=10,b=10,l=10,r=10), showlegend=False)
        st.plotly_chart(fig_ten, use_container_width=True, key="p1_tenure")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Q1 INSIGHT ──────────────────────────────────
    st.markdown(f"""
    <div class="insight-box">
         <strong>Q1 – The Headline:</strong> Overall, <strong>{left_pct:.1f}%</strong> of employees have left ({left_n:,} out of {total:,}).
         The highest-risk role is <strong>{top_role['Job Role']}</strong> with <strong>{top_role['Rate']:.1f}% attrition</strong>
         ({int(top_role['Left']):,} left out of {int(top_role['Total']):,}).
         This is the first place HR should investigate for role-specific retention actions.
    </div>
    """, unsafe_allow_html=True)
