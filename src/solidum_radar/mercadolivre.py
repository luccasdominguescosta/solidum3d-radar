from __future__ import annotations

import time
import requests
import pandas as pd


def fetch_mercadolivre_metrics(keywords: pd.DataFrame) -> pd.DataFrame:
    rows = []

    for keyword in keywords["keyword"].dropna().unique():
        metrics = _fetch_keyword_metrics(keyword)

        rows.append(
            {
                "keyword": keyword,
                **metrics,
            }
        )

        time.sleep(0.5)

    return pd.DataFrame(rows)


def _fetch_keyword_metrics(keyword: str) -> dict:
    try:
        response = requests.get(
            "https://api.mercadolibre.com/sites/MLB/search",
            params={
                "q": keyword,
                "limit": 50,
            },
            timeout=20,
        )

        response.raise_for_status()
        data = response.json()

        results = data.get("results", [])

        if not results:
            return _empty_metrics()

        prices = [
            item.get("price")
            for item in results
            if item.get("price") is not None
        ]

        if not prices:
            return _empty_metrics()

        avg_price = sum(prices) / len(prices)

        return {
            "ml_ads": len(results),
            "ml_avg_price": round(avg_price, 2),
            "ml_min_price": round(min(prices), 2),
            "ml_max_price": round(max(prices), 2),
            "ml_competition": len(results),
            "ml_price_opportunity": round(_calculate_price_opportunity(prices), 1),
        }

    except Exception:
        return _empty_metrics()


def _calculate_price_opportunity(prices: list[float]) -> float:
    if not prices:
        return 0

    avg_price = sum(prices) / len(prices)
    spread = max(prices) - min(prices)

    score = min(avg_price / 2, 60) + min(spread / 5, 40)

    return min(score, 100)


def _empty_metrics() -> dict:
    return {
        "ml_ads": 0,
        "ml_avg_price": 0,
        "ml_min_price": 0,
        "ml_max_price": 0,
        "ml_competition": 0,
        "ml_price_opportunity": 0,
    }
