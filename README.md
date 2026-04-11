# E-Commerce Analytics Pipeline

End-to-end data pipeline on real e-commerce data (100K+ orders from a Brazilian marketplace), from raw ingestion to analytical dashboards.

Built to demonstrate production-grade data engineering practices: medallion architecture, automated transformations, data quality testing, orchestration, and BI reporting.

---

## Architecture
Olist CSV (Kaggle)
│
▼
[Python Ingestion] ──→ Snowflake RAW (bronze)
│
[Airflow DAG]
│
▼
Snowflake STAGING (silver)
via dbt models
│
▼
Snowflake MARTS (gold)
star schema + KPIs
/           
▼             ▼
Metabase      Power BI
dashboards    dashboards

GitHub Actions CI/CD (dbt test, SQL lint)

---

## Tech Stack

| Layer           | Tool                        | Why                                                    |
|-----------------|-----------------------------|---------------------------------------------------------|
| Source          | Kaggle (Olist dataset)       | Real e-commerce data, 9 tables, 550K+ rows             |
| Warehouse      | Snowflake                    | Scalable cloud DWH, free trial, native dbt support     |
| Ingestion      | Python + pandas              | Lightweight, full control over CSV-to-Snowflake load   |
| Transformation | dbt Core                     | SQL-based, testable, documented, industry standard     |
| Orchestration  | Airflow (Docker)             | DAG-based scheduling, retries, alerting                |
| BI             | Metabase + Power BI          | Metabase for reproducibility, Power BI for DAX depth   |
| CI/CD          | GitHub Actions               | Automated dbt test + SQLFluff lint on every PR         |
| Quality        | dbt tests                    | not_null, unique, relationships, custom business rules |

---

## Data Model

### Medallion Architecture

- **Bronze (RAW)** — Raw CSV data loaded as-is into Snowflake
- **Silver (STAGING)** — Cleaned, typed, deduplicated, tested
- **Gold (MARTS)** — Star schema and business-ready aggregations

### Star Schema (Gold Layer)

**Fact table:**
- `fct_orders` — one row per order line item (order, product, seller, payment, review)

**Dimension tables:**
- `dim_customers` — customer demographics and location
- `dim_products` — product details and category
- `dim_sellers` — seller info and location
- `dim_dates` — date spine for time intelligence

**Data marts:**
- `mart_customer_ltv` — customer lifetime value
- `mart_cohort_retention` — monthly cohort retention analysis
- `mart_sales_performance` — seller and category performance

---

## Dataset

[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) — real anonymized orders from 2016-2018.

| Table             | Rows      | Description                    |
|-------------------|-----------|--------------------------------|
| orders            | 99,441    | Order header (status, dates)   |
| customers         | 99,441    | Customer location              |
| order_items       | 112,650   | Line items per order           |
| payments          | 103,886   | Payment methods per order      |
| reviews           | 99,224    | Customer reviews and scores    |
| products          | 32,951    | Product catalog                |
| sellers           | 3,095     | Seller information             |
| geolocation       | 1,000,163 | Zip code coordinates           |
| category_translation | 71     | Category name PT → EN          |

---

## Project Progress

- [x] Week 1 — Project setup, Snowflake config, raw data ingestion (550K+ rows)
- [ ] Week 2 — Airflow orchestration + dbt staging models
- [ ] Week 3 — Star schema modeling (gold layer)
- [ ] Week 4 — Data marts + Metabase dashboards
- [ ] Week 5 — Power BI dashboards + CI/CD + documentation

---

## How to Reproduce

### Prerequisites
- Python 3.12+
- Snowflake account ([free trial](https://signup.snowflake.com))
- Docker & Docker Compose (for Airflow + Metabase)

### Setup

```bash
git clone https://github.com/achraf-boua/olist-analytics-pipeline.git
cd olist-analytics-pipeline
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configure credentials

```bash
cp .env.example .env
# Edit .env with your Snowflake credentials
```

### Download data

Download the [Olist dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) and extract CSVs into `data/olist/`.

### Run ingestion

```bash
python3 ingestion/load_to_snowflake.py
```

---

## Author

**Achraf Boua** — Data Engineer

- LinkedIn: [linkedin.com/in/achraf-boua](https://linkedin.com/in/achraf-boua)