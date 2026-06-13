from __future__ import annotations

import pandas as pd


def _clip(series: pd.Series, low: float = 0, high: float = 100) -> pd.Series:
    return series.clip(lower=low, upper=high)


def _num(df: pd.DataFrame, col: str, default: float = 0) -> pd.Series:
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce").fillna(default)

    return pd.Series(default, index=df.index)


def add_scores(
    df: pd.DataFrame,
    source_weights: pd.DataFrame,
) -> pd.DataFrame:

    result = df.copy()
    result.columns = result.columns.str.strip()

    if "source" not in result.columns:
        result["source"] = "unknown"

    if "title" not in result.columns:
        result["title"] = ""

    if "keyword" not in result.columns:
        result["keyword"] = ""

    weights = dict(
        zip(
            source_weights["source"],
            source_weights["weight"],
        )
    )

    result["source_weight"] = (
        result["source"]
        .map(weights)
        .fillna(1.0)
    )

    price = _num(result, "price", 0)
    estimated_cost = _num(result, "estimated_cost", 0)
    sales_30d = _num(result, "sales_30d", 0)
    reviews = _num(result, "reviews", 0)
    competitors = _num(result, "competitors", 0)
    brand_fit = _num(result, "brand_fit", 5)
    printability = _num(result, "printability", 5)
    ip_risk = _num(result, "ip_risk", 5)

    google_trend_score = _num(result, "google_trend_score", 0)

    ml_ads = _num(result, "ml_ads", 0)
    ml_avg_price = _num(result, "ml_avg_price", 0)
    ml_competition = _num(result, "ml_competition", 0)
    ml_price_opportunity = _num(result, "ml_price_opportunity", 0)

    result["gross_margin"] = price - estimated_cost
    result["margin_pct"] = result["gross_margin"] / price.replace(0, 1)

    demand_score = _clip(
        (sales_30d / 5)
        + (reviews / 10),
        0,
        100,
    )

    price_score = _clip(
        price / 1.2,
        0,
        100,
    )

    margin_score = _clip(
        result["margin_pct"].fillna(0) * 120,
        0,
        100,
    )

    competition_score = _clip(
        100 - competitors * 1.4,
        0,
        100,
    )

    brand_score = brand_fit * 10
    print_score = printability * 10
    risk_penalty = ip_risk * 7

    trend_score = _clip(
        (demand_score * 0.55)
        + (competition_score * 0.25)
        + (reviews / 3),
        0,
        100,
    )

    ml_market_score = _clip(
        (ml_ads * 1.2)
        + (ml_avg_price / 2)
        + (ml_price_opportunity * 0.8)
        - (ml_competition * 0.4),
        0,
        100,
    )

    base_score = (
        demand_score * 0.16
        + price_score * 0.08
        + margin_score * 0.20
        + competition_score * 0.10
        + brand_score * 0.14
        + print_score * 0.11
        + trend_score * 0.05
        + google_trend_score * 0.08
        + ml_market_score * 0.14
        - risk_penalty * 0.12
    )

    result["demand_score"] = demand_score.round(1)
    result["trend_score"] = trend_score.round(1)
    result["google_trend_score"] = google_trend_score.round(1)
    result["ml_market_score"] = ml_market_score.round(1)

    result["opportunity_score"] = _clip(
        base_score * result["source_weight"],
        0,
        100,
    ).round(1)

    result["decision"] = result["opportunity_score"].apply(_decision)
    result["launch_recommendation"] = result["opportunity_score"].apply(
        _launch_recommendation
    )
    result["ml_signal"] = result["ml_market_score"].apply(_ml_signal)

    return result.sort_values(
        "opportunity_score",
        ascending=False,
    )


def _decision(score: float) -> str:
    if score >= 80:
        return "Testar"

    if score >= 60:
        return "Observar"

    return "Descartar"


def _launch_recommendation(score: float) -> str:
    if score >= 85:
        return "Lançar Agora"

    if score >= 75:
        return "Testar"

    if score >= 60:
        return "Observar"

    return "Descartar"


def _ml_signal(score: float) -> str:
    if score >= 80:
        return "Mercado forte"

    if score >= 60:
        return "Mercado promissor"

    if score >= 40:
        return "Mercado moderado"

    return "Mercado fraco"
