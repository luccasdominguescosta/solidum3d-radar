from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px

BASE_DIR = Path(__file__).parent
OUTPUT = BASE_DIR / "outputs" / "radar_multifontes_output.csv"

st.set_page_config(
    page_title="Solidum3D Radar V7",
    layout="wide"
)

st.title("🚀 Solidum3D Radar V7")
st.caption(
    "Radar multifontes com Google Trends e Mercado Livre Intelligence para identificar oportunidades reais de produtos 3D."
)

if not OUTPUT.exists():
    st.warning(
        "Arquivo de dados não encontrado. Rode o workflow no GitHub Actions para gerar o CSV."
    )
    st.stop()

df = pd.read_csv(OUTPUT)

required_columns = [
    "launch_recommendation",
    "google_trend_score",
    "google_trend_direction",
    "ml_ads",
    "ml_avg_price",
    "ml_min_price",
    "ml_max_price",
    "ml_competition",
    "ml_price_opportunity",
    "ml_market_score",
    "ml_signal",
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.error(
        "O CSV ainda não está atualizado para a V7. Rode novamente o workflow no GitHub Actions."
    )
    st.write("Colunas faltando:", missing_columns)
    st.stop()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Oportunidades", len(df))
col2.metric("Score Médio", round(df["opportunity_score"].mean(), 1))
col3.metric("Lançar Agora", int((df["launch_recommendation"] == "Lançar Agora").sum()))
col4.metric("Preço Médio ML", f"R$ {df['ml_avg_price'].mean():.2f}")
col5.metric("Fontes", df["source"].nunique())

st.divider()

st.subheader("🔥 Produtos Recomendados para Solidum3D")

recommended_df = df[
    df["launch_recommendation"].isin(
        ["Lançar Agora", "Testar"]
    )
].sort_values(
    "opportunity_score",
    ascending=False
)

st.dataframe(
    recommended_df[
        [
            "launch_recommendation",
            "opportunity_score",
            "ml_signal",
            "ml_market_score",
            "google_trend_score",
            "source",
            "keyword",
            "title",
            "price",
            "ml_avg_price",
            "ml_ads",
            "margin_pct",
        ]
    ],
    use_container_width=True,
)

st.divider()

st.subheader("🟡 Mercado Livre Intelligence")

ml_cols = [
    "keyword",
    "ml_ads",
    "ml_avg_price",
    "ml_min_price",
    "ml_max_price",
    "ml_competition",
    "ml_price_opportunity",
    "ml_market_score",
    "ml_signal",
]

ml_df = (
    df[ml_cols]
    .drop_duplicates()
    .sort_values(
        "ml_market_score",
        ascending=False
    )
)

st.dataframe(
    ml_df,
    use_container_width=True
)

fig_ml = px.bar(
    ml_df.head(10),
    x="keyword",
    y="ml_market_score",
    title="Score de Mercado — Mercado Livre",
)

st.plotly_chart(
    fig_ml,
    use_container_width=True
)

st.divider()

st.subheader("📈 Google Trends")

trends_df = (
    df[
        [
            "keyword",
            "google_trend_score",
            "google_trend_direction",
        ]
    ]
    .drop_duplicates()
    .sort_values(
        "google_trend_score",
        ascending=False
    )
)

st.dataframe(
    trends_df,
    use_container_width=True
)

fig_trends = px.bar(
    trends_df.head(10),
    x="keyword",
    y="google_trend_score",
    title="Top Tendências do Google"
)

st.plotly_chart(
    fig_trends,
    use_container_width=True
)

st.divider()

st.subheader("🏆 Top Oportunidades")

top_cols = [
    "launch_recommendation",
    "decision",
    "opportunity_score",
    "ml_signal",
    "ml_market_score",
    "google_trend_score",
    "google_trend_direction",
    "source",
    "keyword",
    "title",
    "price",
    "ml_avg_price",
    "ml_ads",
    "sales_30d",
    "margin_pct",
    "competitors",
]

st.dataframe(
    df[top_cols].sort_values(
        "opportunity_score",
        ascending=False
    ),
    use_container_width=True,
)

st.divider()

st.subheader("🌎 Score por Fonte")

source_df = (
    df.groupby(
        "source",
        as_index=False
    )["opportunity_score"]
    .mean()
    .sort_values(
        "opportunity_score",
        ascending=False
    )
)

fig_source = px.bar(
    source_df,
    x="source",
    y="opportunity_score",
    title="Score Médio por Fonte"
)

st.plotly_chart(
    fig_source,
    use_container_width=True
)

st.divider()

st.subheader("🧠 Mapa de Oportunidade")

fig_scatter = px.scatter(
    df,
    x="ml_market_score",
    y="google_trend_score",
    size="opportunity_score",
    color="launch_recommendation",
    hover_name="title",
    hover_data=[
        "source",
        "price",
        "ml_avg_price",
        "ml_ads",
        "margin_pct",
    ],
    title="Mercado Livre x Google Trends"
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)

st.divider()

with st.expander("📄 Ver dados completos"):
    st.dataframe(
        df.sort_values(
            "opportunity_score",
            ascending=False
        ),
        use_container_width=True,
    )
