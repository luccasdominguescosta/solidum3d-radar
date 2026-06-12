from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px

from src.solidum_radar.run_pipeline import main as run_pipeline

BASE_DIR = Path(__file__).parent
OUTPUT = BASE_DIR / "outputs" / "radar_multifontes_output.csv"

st.set_page_config(
    page_title="Solidum3D Radar V6",
    layout="wide"
)

st.title("🚀 Solidum3D Radar V6")
st.caption(
    "Radar multifontes com Google Trends para identificar oportunidades reais de produtos 3D."
)


def load_data() -> pd.DataFrame:
    needs_refresh = True

    if OUTPUT.exists():
        existing_df = pd.read_csv(OUTPUT)
        needs_refresh = (
            "launch_recommendation" not in existing_df.columns
            or "google_trend_score" not in existing_df.columns
            or "google_trend_direction" not in existing_df.columns
        )

    if needs_refresh:
        with st.spinner("Atualizando Radar Solidum3D V6..."):
            run_pipeline()

    return pd.read_csv(OUTPUT)


df = load_data()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Oportunidades", len(df))
col2.metric("Score Médio", round(df["opportunity_score"].mean(), 1))
col3.metric("Lançar Agora", int((df["launch_recommendation"] == "Lançar Agora").sum()))
col4.metric("Para Testar", int((df["decision"] == "Testar").sum()))
col5.metric("Fontes", df["source"].nunique())

st.divider()

st.subheader("🏆 Top Oportunidades")

top_cols = [
    "launch_recommendation",
    "decision",
    "opportunity_score",
    "google_trend_score",
    "google_trend_direction",
    "source",
    "keyword",
    "title",
    "price",
    "sales_30d",
    "margin_pct",
    "competitors",
]

st.dataframe(
    df[top_cols].sort_values("opportunity_score", ascending=False),
    use_container_width=True,
)

st.divider()

st.subheader("📈 Google Trends")

trends_df = (
    df[["keyword", "google_trend_score", "google_trend_direction"]]
    .drop_duplicates()
    .sort_values("google_trend_score", ascending=False)
)

st.dataframe(trends_df, use_container_width=True)

fig_trends = px.bar(
    trends_df.head(10),
    x="keyword",
    y="google_trend_score",
    title="Top Tendências do Google"
)

st.plotly_chart(fig_trends, use_container_width=True)

st.divider()

st.subheader("🌎 Score por Fonte")

source_df = (
    df.groupby("source", as_index=False)["opportunity_score"]
    .mean()
    .sort_values("opportunity_score", ascending=False)
)

fig_source = px.bar(
    source_df,
    x="source",
    y="opportunity_score",
    title="Score Médio por Fonte"
)

st.plotly_chart(fig_source, use_container_width=True)

st.divider()

st.subheader("🎯 Produtos para Lançar")

launch_df = df[df["launch_recommendation"] == "Lançar Agora"]

if len(launch_df) > 0:
    st.dataframe(
        launch_df[
            [
                "title",
                "source",
                "opportunity_score",
                "google_trend_score",
                "margin_pct",
            ]
        ],
        use_container_width=True,
    )
else:
    st.info("Nenhum produto atingiu nota para Lançar Agora.")

st.divider()

st.subheader("🧠 Mapa de Oportunidade")

fig_scatter = px.scatter(
    df,
    x="margin_pct",
    y="google_trend_score",
    size="opportunity_score",
    color="launch_recommendation",
    hover_name="title",
    hover_data=[
        "source",
        "price",
        "sales_30d",
        "competitors",
    ],
    title="Margem x Tendência Google"
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()

with st.expander("📄 Ver dados completos"):
    st.dataframe(
        df.sort_values("opportunity_score", ascending=False),
        use_container_width=True,
    )
