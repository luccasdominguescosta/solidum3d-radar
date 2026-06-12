# Arquitetura — Solidum3D Radar V5

```text
Palavras-chave Solidum3D
        ↓
Providers multifontes
        ↓
Normalização dos dados
        ↓
SQLite histórico
        ↓
Motor de score
        ↓
Dashboard + CSV + GitHub Actions
```

## Providers

Cada fonte deve entregar as mesmas colunas:

- source
- keyword
- title
- price
- sales_30d
- reviews
- competitors
- estimated_cost
- brand_fit
- printability
- ip_risk
- url

## Fontes prioritárias

1. Shopee
2. Mercado Livre
3. Elo7
4. Etsy
5. Pinterest
6. MakerWorld
7. Printables
8. Amazon
9. TikTok/Reels

## Regras de segurança

- Usar API oficial ou autorizada sempre que possível.
- Não automatizar login protegido.
- Não burlar captcha.
- Não copiar modelos protegidos.
- Usar sinais de demanda para criar designs originais.
