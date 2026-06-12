from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
import pandas as pd

from .providers import CSVProvider
from .scoring import add_scores
from .database import save_snapshot
from .trends import fetch_google_trends

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
        how="left"
    )

    raw["google_trend_score"] = raw["google_trend_score"].fillna(0)
    raw["google_trend_direction"] = raw["google_trend_direction"].fillna("sem dados")
    raw["snapshot_at"] = datetime.now(timezone.utc).isoformat()

    scored = add_scores(raw, source_weights)

    output_dir = PROJECT_ROOT / "outputs"
    output_dir.mkdir(exist_ok=True)

    scored.to_csv(output_dir / "radar_multifontes_output.csv", index=False)
    save_snapshot(scored, PROJECT_ROOT / "solidum_radar.db")

    print("Radar V6 atualizado com sucesso.")
    print(
        scored[
            [
                "source",
                "title",
                "google_trend_score",
                "google_trend_direction",
                "opportunity_score",
                "decision",
            ]
        ]
        .head(10)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()
