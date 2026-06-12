from __future__ import annotations

import requests
import pandas as pd


def get_ml_metrics(keyword: str) -> dict:

    try:

        url = (
            "https://api.mercadolibre.com/sites/MLB/search"
            f"?q={keyword}"
            "&limit=50"
        )

        response = requests.get(
            url,
            timeout=20
        )

        data = response.json()

        results = data.get(
            "results",
            []
        )

        if not results:

            return {
                "ml_ads": 0,
                "ml_avg_price": 0,
                "ml_competition": 0,
            }

        prices = [
            item["price"]
            for item in results
            if item.get("price")
        ]

        avg_price = (
            sum(prices)
            / len(prices)
        )

        return {
            "ml_ads": len(results),
            "ml_avg_price": round(avg_price, 2),
            "ml_competition": len(results),
        }

    except Exception:

        return {
            "ml_ads": 0,
            "ml_avg_price": 0,
            "ml_competition": 0,
        }
