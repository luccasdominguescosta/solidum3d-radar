from __future__ import annotations

import pandas as pd
from pathlib import Path
from typing import Protocol


class Provider(Protocol):
    name: str

    def fetch(self, keywords: pd.DataFrame) -> pd.DataFrame:
        ...


class CSVProvider:
    """Provider seguro para MVP: lê dados mockados ou exportações CSV.

    Para produção, crie providers autorizados por fonte, por exemplo:
    - MercadoLivreAPIProvider
    - ShopeeOpenPlatformProvider
    - EtsyAPIProvider

    Evite scraping com login, captcha ou bypass de proteção.
    """

    name = "CSV"

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def fetch(self, keywords: pd.DataFrame) -> pd.DataFrame:
        df = pd.read_csv(self.path)
        allowed_keywords = set(keywords["keyword"].str.lower())
        return df[df["keyword"].str.lower().isin(allowed_keywords)].copy()


class ShopeeProviderPlaceholder:
    name = "Shopee"

    def fetch(self, keywords: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError(
            "Conecte aqui a Shopee Open Platform ou uma API autorizada. "
            "Não use automação que burle login, captcha ou termos da plataforma."
        )


class MercadoLivreProviderPlaceholder:
    name = "Mercado Livre"

    def fetch(self, keywords: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError(
            "Conecte aqui a API oficial/autorizada do Mercado Livre."
        )
