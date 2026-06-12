# Solidum3D Radar V5 — Radar Multifontes

Radar de oportunidades para a Solidum3D, pensado para identificar produtos, nichos e sinais de demanda em múltiplas fontes.

> Objetivo: encontrar oportunidades de produtos 3D originais, com boa margem, baixa saturação e alto fit com a marca Solidum3D.

## Fontes previstas

- Shopee
- Mercado Livre
- Elo7
- Etsy
- Amazon
- Pinterest
- MakerWorld
- Printables
- TikTok/Reels via entrada manual ou API autorizada

Nesta versão, os providers vêm em modo **mock/CSV** por segurança e estabilidade. A estrutura está pronta para conectar APIs oficiais ou serviços autorizados, sem depender de automação que burle login, captcha ou termos de uso.

## O que a V5 faz

- Lê palavras-chave estratégicas da Solidum3D
- Coleta oportunidades por múltiplas fontes
- Normaliza os dados em um formato único
- Salva histórico em SQLite
- Calcula score de oportunidade
- Detecta tendência por variação de vendas/engajamento
- Gera CSV final para análise
- Exibe dashboard em Streamlit
- Tem GitHub Actions para execução semanal

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Rodar coleta e score

```bash
python -m solidum_radar.run_pipeline
```

## Abrir dashboard

```bash
streamlit run app.py
```

## Arquivos principais

```text
config/keywords.csv              Palavras-chave monitoradas
config/source_weights.csv        Peso estratégico por fonte
data/mock_opportunities.csv      Base simulada multifontes
src/solidum_radar/providers.py   Providers plugáveis
src/solidum_radar/scoring.py     Motor de score Solidum3D
src/solidum_radar/database.py    SQLite
src/solidum_radar/run_pipeline.py Pipeline principal
app.py                           Dashboard Streamlit
```

## Score Solidum3D

O score considera:

- Demanda estimada
- Preço médio
- Concorrência
- Margem estimada
- Fit com a marca
- Facilidade de impressão
- Risco de marca/cópia
- Tendência recente
- Peso estratégico da fonte

Decisão automática:

- **Testar**: score >= 80
- **Observar**: score entre 60 e 79
- **Descartar**: score < 60

## Próximos passos recomendados

1. Conectar Mercado Livre via API autorizada.
2. Conectar Shopee Open Platform para dados próprios da loja.
3. Criar entrada semi-automática para Etsy/Elo7/Pinterest.
4. Adicionar análise com IA para classificar se o produto é imprimível em 3D.
5. Criar módulo de custo estimado por tempo, gramas e máquina.
6. Criar ranking específico por capacidade das máquinas: Vinci, Tesla, Euler, Gaudí e Turing.

## Aviso importante

Este projeto deve ser usado para identificar sinais de demanda e criar produtos originais da Solidum3D, não para copiar modelos protegidos, personagens licenciados, marcas ou designs de terceiros.
