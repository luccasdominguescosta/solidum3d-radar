from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
import pandas as pd

from .providers import CSVProvider
from .scoring import add_scores
from .database import save_snapshot
from .trends import fetch_google_trends
from .mercadolivre import fetch_mercadolivre_metrics

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    keywords = pd.read_csv(PROJECT_ROOT / "config" / "keywords.csv")
    source_weights = pd.read_csv(PROJECT_ROOT / "config" / "source_weights.csv")

    provider = CSVProvider(PROJECT_ROOT / "data" / "mock_opportunities.csv")
    raw = provider.fetch(keywords)

    trends = fetch_google_trends(keywords)

    raw = raw.merge(
        trends,
        on="keyword",
        how="left",
    )

    raw["google_trend_score"] = raw.get("google_trend_score", 0)
    raw["google_trend_direction"] = raw.get("google_trend_direction", "sem dados")

    ml_metrics = fetch_mercadolivre_metrics(keywords)

    required_ml_columns = [
        "keyword",
        "ml_ads",
        "ml_avg_price",
        "ml_min_price",
        "ml_max_price",
        "ml_competition",
        "ml_price_opportunity",
    ]

    for col in required_ml_columns:
        if col not in ml_metrics.columns:
            ml_metrics[col] = 0

    raw = raw.merge(
        ml_metrics,
        on="keyword",
        how="left",
    )

    for col in [
        "ml_ads",
        "ml_avg_price",
        "ml_min_price",
        "ml_max_price",
        "ml_competition",
        "ml_price_opportunity",
    ]:
        if col not in raw.columns:
            raw[col] = 0

        raw[col] = raw[col].fillna(0)

    raw["google_trend_score"] = raw["google_trend_score"].fillna(0)
    raw["google_trend_direction"] = raw["google_trend_direction"].fillna("sem dados")
    raw["snapshot_at"] = datetime.now(timezone.utc).isoformat()

    scored = add_scores(raw, source_weights)

    output_dir = PROJECT_ROOT / "outputs"
    output_dir.mkdir(exist_ok=True)

    scored.to_csv(
        output_dir / "radar_multifontes_output.csv",
        index=False,
    )

    save_snapshot(
        scored,
        PROJECT_ROOT / "solidum_radar.db",
    )

    print("Radar V7 atualizado com sucesso.")
    print("Colunas finais:")
    print(scored.columns.tolist())

    print(
        scored[
            [
                "source",
                "title",
                "google_trend_score",
                "google_trend_direction",
                "ml_ads",
                "ml_avg_price",
                "ml_market_score",
                "opportunity_score",
                "decision",
            ]
        ]
        .head(10)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()
