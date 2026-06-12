from __future__ import annotations

import pandas as pd


def _clip(series: pd.Series, low: float = 0, high: float = 100) -> pd.Series:
    return series.clip(lower=low, upper=high)


def add_scores(df: pd.DataFrame, source_weights: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()

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

    result["gross_margin"] = (
        result["price"]
        - result["estimated_cost"]
    )

    result["margin_pct"] = (
        result["gross_margin"]
        / result["price"]
    )

    demand_score = _clip(
        (
            result["sales_30d"].fillna(0) / 5
        )
        + (
            result["reviews"].fillna(0) / 10
        ),
        0,
        100,
    )

    price_score = _clip(
        result["price"] / 1.2,
        0,
        100,
    )

    margin_score = _clip(
        result["margin_pct"] * 120,
        0,
        100,
    )

    competition_score = _clip(
        100
        - result["competitors"].fillna(0) * 1.4,
        0,
        100,
    )

    brand_score = (
        result["brand_fit"]
        .fillna(5)
        * 10
    )

    print_score = (
        result["printability"]
        .fillna(5)
        * 10
    )

    risk_penalty = (
        result["ip_risk"]
        .fillna(5)
        * 7
    )

    google_trend_score = (
        result["google_trend_score"]
        .fillna(0)
    )

    for col in [
    "ml_ads",
    "ml_avg_price",
    "ml_min_price",
    "ml_max_price",
    "ml_competition",
    "ml_price_opportunity",
]:
    if col not in result.columns:
        result[col] = 0

    ml_ads = (
        result["ml_ads"]
        .fillna(0)
    )

    ml_avg_price = (
        result["ml_avg_price"]
        .fillna(0)
    )

    ml_competition = (
        result["ml_competition"]
        .fillna(0)
    )

    ml_price_opportunity = (
        result["ml_price_opportunity"]
        .fillna(0)
    )

    trend_score = _clip(
        (
            demand_score * 0.55
        )
        + (
            competition_score * 0.25
        )
        + (
            result["reviews"].fillna(0) / 3
        ),
        0,
        100,
    )

    ml_market_score = _clip(
        (
            ml_ads * 1.2
        )
        + (
            ml_avg_price / 2
        )
        + (
            ml_price_opportunity * 0.8
        )
        - (
            ml_competition * 0.4
        ),
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

    result["decision"] = result["opportunity_score"].apply(
        _decision
    )

    result["launch_recommendation"] = result[
        "opportunity_score"
    ].apply(
        _launch_recommendation
    )

    result["ml_signal"] = ml_market_score.apply(
        _ml_signal
    )

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
