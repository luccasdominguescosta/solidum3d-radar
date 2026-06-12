from __future__ import annotations

import time
import pandas as pd
from pytrends.request import TrendReq


def fetch_google_trends(keywords: pd.DataFrame) -> pd.DataFrame:
    pytrends = TrendReq(hl="pt-BR", tz=180)

    rows = []

    for keyword in keywords["keyword"].dropna().unique():
        try:
            pytrends.build_payload(
                [keyword],
                cat=0,
                timeframe="today 3-m",
                geo="BR",
                gprop=""
            )

            data = pytrends.interest_over_time()

            if data.empty:
                trend_score = 0
                trend_direction = "sem dados"
            else:
                values = data[keyword].tail(12)
                recent = values.tail(4).mean()
                previous = values.head(4).mean()

                trend_score = round(float(recent), 1)

                if recent > previous * 1.15:
                    trend_direction = "alta"
                elif recent < previous * 0.85:
                    trend_direction = "queda"
                else:
                    trend_direction = "estavel"

            rows.append({
                "keyword": keyword,
                "google_trend_score": trend_score,
                "google_trend_direction": trend_direction
            })

            time.sleep(2)

        except Exception as e:
            rows.append({
                "keyword": keyword,
                "google_trend_score": 0,
                "google_trend_direction": f"erro: {str(e)[:60]}"
            })

    return pd.DataFrame(rows)
