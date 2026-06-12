from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

OUTPUT = Path("outputs/radar_multifontes_output.csv")

st.set_page_config(page_title="Solidum3D Radar V5", layout="wide")
st.title("Solidum3D Radar V5 — Radar Multifontes")
st.caption("Radar de oportunidades para produtos 3D originais, premium e escaláveis.")

if not OUTPUT.exists():
    st.warning("Execute primeiro: python -m solidum_radar.run_pipeline")
    st.stop()

df = pd.read_csv(OUTPUT)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Oportunidades", len(df))
col2.metric("Score médio", round(df["opportunity_score"].mean(), 1))
col3.metric("Para testar", int((df["decision"] == "Testar").sum()))
col4.metric("Fontes", df["source"].nunique())

st.subheader("Top oportunidades")
st.dataframe(
    df[[
        "decision", "opportunity_score", "source", "keyword", "title", "price",
        "sales_30d", "competitors", "margin_pct", "trend_score", "url"
    ]],
    use_container_width=True,
)

st.subheader("Score por fonte")
fig = px.bar(
    df.groupby("source", as_index=False)["opportunity_score"].mean().sort_values("opportunity_score", ascending=False),
    x="source",
    y="opportunity_score",
    title="Score médio por fonte"
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Mapa de decisão")
fig2 = px.scatter(
    df,
    x="margin_pct",
    y="trend_score",
    size="opportunity_score",
    color="decision",
    hover_name="title",
    hover_data=["source", "price", "sales_30d", "competitors"],
    title="Margem x Tendência"
)
st.plotly_chart(fig2, use_container_width=True)
