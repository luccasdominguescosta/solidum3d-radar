from dataclasses import dataclass


@dataclass
class Opportunity:
    source: str
    keyword: str
    title: str
    price: float
    sales_30d: int
    reviews: int
    competitors: int
    estimated_cost: float
    brand_fit: int
    printability: int
    ip_risk: int
    url: str
